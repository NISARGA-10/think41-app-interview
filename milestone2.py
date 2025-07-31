from flask import Flask, jsonify, abort
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATABASE = 'products.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()

    data = [dict(row) for row in products]
    return jsonify({'status': 'success', 'data': data})

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()

    if product is None:
        return jsonify({'status': 'error', 'message': 'Product not found'}), 404

    return jsonify({'status': 'success', 'data': dict(product)})

if __name__ == '__main__':
    app.run(debug=True)
