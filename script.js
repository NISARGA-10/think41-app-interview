// Check if we are on index.html
if (window.location.pathname.endsWith("index.html") || window.location.pathname === "/") {
    fetch("http://127.0.0.1:5000/api/products")
        .then(response => response.json())
        .then(json => {
            if (json.status === "success") {
                const container = document.getElementById("product-list");
                json.data.forEach(product => {
                    const card = document.createElement("div");
                    card.className = "product-card";
                    card.innerHTML = `
              <h3>${product.name}</h3>
              <p><strong>Brand:</strong> ${product.brand}</p>
              <p><strong>Category:</strong> ${product.category}</p>
              <a href="product.html?id=${product.id}">View Details</a>
            `;
                    container.appendChild(card);
                });
            } else {
                document.getElementById("product-list").textContent = "No products found.";
            }
        })
        .catch(error => {
            console.error("Failed to fetch products:", error);
            document.getElementById("product-list").textContent = "Failed to load products.";
        });
}

// Check if we are on product.html
if (window.location.pathname.endsWith("product.html")) {
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    if (!id) {
        document.getElementById("product-detail").textContent = "Invalid product ID.";
    } else {
        fetch(`http://127.0.0.1:5000/api/products/${id}`)
            .then(response => {
                if (!response.ok) throw new Error("Product not found");
                return response.json();
            })
            .then(json => {
                if (json.status === "success") {
                    const product = json.data;
                    const container = document.getElementById("product-detail");
                    container.innerHTML = `
              <h3>${product.name}</h3>
              <p><strong>Brand:</strong> ${product.brand}</p>
              <p><strong>Category:</strong> ${product.category}</p>
              <p><strong>Cost:</strong> ${product.cost}</p>
              <p><strong>Retail Price:</strong> ${product.retail_price}</p>
              <p><strong>Department:</strong> ${product.department}</p>
              <p><strong>SKU:</strong> ${product.sku}</p>
              <p><strong>Distribution Center:</strong> ${product.distribution_center_id}</p>
              <a href="index.html">← Back to Products</a>
            `;
                } else {
                    document.getElementById("product-detail").textContent = "Product not found.";
                }
            })
            .catch(error => {
                console.error(error);
                document.getElementById("product-detail").textContent = "Error loading product.";
            });
    }
}
