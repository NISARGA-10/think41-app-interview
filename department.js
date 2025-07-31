function getDeptIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

const deptId = getDeptIdFromURL();

if (deptId) {
    // Get department info
    fetch(`/api/departments/${deptId}`)
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                document.getElementById('departmentTitle').textContent = `${data.data.name} Products`;
            } else {
                document.getElementById('departmentTitle').textContent = "Invalid Department";
            }
        });

    // Get products
    fetch(`/api/departments/${deptId}/products`)
        .then(res => res.json())
        .then(data => {
            const ul = document.getElementById('departmentProducts');
            ul.innerHTML = "";

            if (data.data.length === 0) {
                ul.innerHTML = "<li>No products in this department.</li>";
                return;
            }

            data.data.forEach(p => {
                const li = document.createElement('li');
                li.textContent = `${p.name} (${p.brand}) - ₹${p.retail_price}`;
                ul.appendChild(li);
            });
        });
} else {
    document.getElementById('departmentTitle').textContent = "Department Not Found";
}
