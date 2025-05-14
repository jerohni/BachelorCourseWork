const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(cors());

const db = new sqlite3.Database('./products.db');

// GET /products — повертає всі товари з партіями
app.get('/products', (req, res) => {
  const sql = `
    SELECT p.code, p.name, p.price, p.section,
           b.quantity, b.expiration
    FROM products p
    LEFT JOIN batches b ON p.id = b.product_id
    ORDER BY p.code, b.expiration
  `;

  db.all(sql, [], (err, rows) => {
    if (err) {
      console.error("❌ DB Error:", err.message);
      return res.status(500).json({ error: 'Internal Server Error' });
    }

    const result = {};

    rows.forEach(row => {
      if (!result[row.code]) {
        result[row.code] = {
          code: row.code,
          name: row.name,
          price: row.price,
          section: row.section,
          batches: []
        };
      }

      if (row.expiration) {
        result[row.code].batches.push({
          quantity: row.quantity,
          expiration: row.expiration
        });
      }
    });

    res.json(Object.values(result));
  });
});

// ВАЖЛИВО: запуск сервера
app.listen(PORT, () => {
  console.log(`✅ Сервер запущено: http://localhost:${PORT}`);
});
