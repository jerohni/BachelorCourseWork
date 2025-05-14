import sqlite3
import csv
from datetime import datetime

# Підключення до SQLite
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# Створення таблиці продуктів
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    section TEXT
)
''')

# Створення таблиці партій
cursor.execute('''
CREATE TABLE IF NOT EXISTS batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    expiration DATE NOT NULL,
    FOREIGN KEY(product_id) REFERENCES products(id)
)
''')

# Парсинг поля ДАТА у форматі: 08/25(2), 07/26(4)
def parse_batches(raw):
    results = []
    if not raw.strip():
        return results
    parts = raw.split(',')
    for part in parts:
        try:
            date_str, qty = part.strip().split('(')
            qty = int(qty.replace(')', ''))
            month, year = date_str.strip().split('/')
            expiration = datetime.strptime(f"{year}-{month}-01", "%y-%m-%d").date()
            results.append((expiration, qty))
        except Exception as e:
            print(f"⚠️ Проблема з партією '{part}': {e}")
            continue
    return results

# Читання з CSV
with open('data/price_list.csv', newline='', encoding='utf-8') as file:
    next(file)  # пропускаємо перший рядок із заголовком "ПРАЙС-ЛИСТ"
    reader = csv.DictReader(file)

    for row in reader:
        try:
            code = row['КОД'].strip()
            name = row['НАЗВА'].strip()
            price = float(row['ЦІНА грн.'].strip())
            section = row['СЕКЦІЯ'].strip()

            # Пропустити рядки без коду (наприклад: заголовки секцій)
            if not code.isdigit():
                continue

            # Додати товар
            cursor.execute('''
                INSERT INTO products (code, name, price, section)
                VALUES (?, ?, ?, ?)
            ''', (code, name, price, section))

            product_id = cursor.lastrowid

            # Обробка партій
            for expiration, qty in parse_batches(row['ДАТА']):
                cursor.execute('''
                    INSERT INTO batches (product_id, quantity, expiration)
                    VALUES (?, ?, ?)
                ''', (product_id, qty, expiration))

        except Exception as e:
            print(f"⚠️ Пропущено рядок через помилку: {e}")
            continue

# Завершення
conn.commit()
conn.close()

print("✅ SQLite база даних успішно створена та заповнена.")
