// Load products
function loadAllProducts() {
    fetch('/api/products')
        .then(res => res.json())
        .then(data => {
            const ul = document.getElementById('productList');
            ul.innerHTML = "";
            data.data.forEach(p => {
                const li = document.createElement('li');
                li.textContent = `${p.name} (${p.brand}) - ₹${p.retail_price}`;
                ul.appendChild(li);
            });
        });
}

// Load departments for dropdown
fetch('/api/departments')
    .then(res => res.json())
    .then(data => {
        const select = document.getElementById('departmentDropdown');
        data.data.forEach(d => {
            const option = document.createElement('option');
            option.value = d.id;
            option.textContent = d.name;
            select.appendChild(option);
        });
    });

// Dropdown navigation
document.getElementById('departmentDropdown').addEventListener('change', function () {
    const id = this.value;
    if (id) {
        window.location.href = `department.html?id=${id}`;
    }
});

loadAllProducts();
