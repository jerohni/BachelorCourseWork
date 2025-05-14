document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("product-table");

  fetch("http://localhost:3000/products")
    .then(res => res.json())
    .then(data => {
      let html = `
        <table>
          <thead>
            <tr>
              <th>Код</th>
              <th>Назва</th>
              <th>Ціна</th>
              <th>Секція</th>
              <th>Залишок</th>
              <th>Партії (термін / кількість)</th>
            </tr>
          </thead>
          <tbody>
      `;

      data.forEach(product => {
        const totalQty = product.batches.reduce((sum, b) => sum + b.quantity, 0);
        const batchList = product.batches.map(b => `${b.expiration} (${b.quantity})`).join('<br>');

        html += `
          <tr>
            <td>${product.code}</td>
            <td>${product.name}</td>
            <td>${product.price}</td>
            <td>${product.section}</td>
            <td>${totalQty}</td>
            <td>${batchList}</td>
          </tr>
        `;
      });

      html += `</tbody></table>`;
      container.innerHTML = html;
    })
    .catch(error => {
      console.error("❌ Помилка при завантаженні:", error);
      container.innerHTML = "<p>Не вдалося завантажити дані.</p>";
    });
});
