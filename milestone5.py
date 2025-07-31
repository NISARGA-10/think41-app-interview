from flask import Flask, jsonify, abort
import sqlite3

app = Flask(__name__)

DATABASE = 'products.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # For dict-like row access
    return conn

# --------- Product APIs ---------

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.name, p.brand, p.category, p.cost, p.retail_price, p.sku, p.distribution_center_id,
               d.id as department_id, d.name as department_name
        FROM products p
        JOIN departments d ON p.department_id = d.id
        LIMIT 100
    """)
    products = cursor.fetchall()
    conn.close()

    data = []
    for p in products:
        data.append({
            "id": p["id"],
            "name": p["name"],
            "brand": p["brand"],
            "category": p["category"],
            "cost": p["cost"],
            "retail_price": p["retail_price"],
            "sku": p["sku"],
            "distribution_center_id": p["distribution_center_id"],
            "department": {
                "id": p["department_id"],
                "name": p["department_name"]
            }
        })
    return jsonify({"status": "success", "data": data}), 200

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.name, p.brand, p.category, p.cost, p.retail_price, p.sku, p.distribution_center_id,
               d.id as department_id, d.name as department_name
        FROM products p
        JOIN departments d ON p.department_id = d.id
        WHERE p.id = ?
    """, (product_id,))
    p = cursor.fetchone()
    conn.close()

    if p is None:
        return jsonify({"status": "error", "message": f"Product with ID {product_id} not found"}), 404

    product = {
        "id": p["id"],
        "name": p["name"],
        "brand": p["brand"],
        "category": p["category"],
        "cost": p["cost"],
        "retail_price": p["retail_price"],
        "sku": p["sku"],
        "distribution_center_id": p["distribution_center_id"],
        "department": {
            "id": p["department_id"],
            "name": p["department_name"]
        }
    }
    return jsonify({"status": "success", "data": product}), 200

# --------- Department APIs ---------

@app.route('/api/departments', methods=['GET'])
def get_departments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM departments")
    departments = cursor.fetchall()
    conn.close()

    if not departments:
        return jsonify({"status": "error", "message": "No departments found"}), 404

    data = [{"id": d["id"], "name": d["name"]} for d in departments]
    return jsonify({"status": "success", "data": data}), 200

@app.route('/api/departments/<int:department_id>', methods=['GET'])
def get_department(department_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM departments WHERE id = ?", (department_id,))
    department = cursor.fetchone()
    conn.close()

    if department is None:
        return jsonify({"status": "error", "message": f"Department with ID {department_id} not found"}), 404

    data = {"id": department["id"], "name": department["name"]}
    return jsonify({"status": "success", "data": data}), 200

@app.route('/api/departments/<int:department_id>/products', methods=['GET'])
def get_products_by_department(department_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check department exists
    cursor.execute("SELECT id FROM departments WHERE id = ?", (department_id,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({"status": "error", "message": f"Department with ID {department_id} not found"}), 404

    cursor.execute("""
        SELECT id, name, brand, category, cost, retail_price, sku, distribution_center_id
        FROM products
        WHERE department_id = ?
        LIMIT 100
    """, (department_id,))
    products = cursor.fetchall()
    conn.close()

    data = []
    for p in products:
        data.append({
            "id": p["id"],
            "name": p["name"],
            "brand": p["brand"],
            "category": p["category"],
            "cost": p["cost"],
            "retail_price": p["retail_price"],
            "sku": p["sku"],
            "distribution_center_id": p["distribution_center_id"]
        })
    return jsonify({"status": "success", "data": data}), 200

# --------- Run the app ---------

if __name__ == '__main__':
    app.run(debug=True)
