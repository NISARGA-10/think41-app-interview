from flask import Flask, jsonify, request, make_response, abort
import sqlite3

app = Flask(__name__)
DB_PATH = 'products.db'


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def success_response(data, status=200):
    return make_response(jsonify({
        "status": "success",
        "data": data
    }), status)


def error_response(message, status=400):
    return make_response(jsonify({
        "status": "error",
        "message": message
    }), status)


# ✅ GET /api/products — List products (with optional pagination and filtering)
@app.route('/api/products', methods=['GET'])
def get_all_products():
    try:
        conn = get_db_connection()

        # Optional filters
        category = request.args.get('category')
        brand = request.args.get('brand')
        page = request.args.get('page', default=1, type=int)
        per_page = 20
        offset = (page - 1) * per_page

        query = "SELECT * FROM products"
        filters = []
        values = []

        if category:
            filters.append("category = ?")
            values.append(category)

        if brand:
            filters.append("brand = ?")
            values.append(brand)

        if filters:
            query += " WHERE " + " AND ".join(filters)

        query += " LIMIT ? OFFSET ?"
        values.extend([per_page, offset])

        products = conn.execute(query, values).fetchall()
        conn.close()

        return success_response([dict(row) for row in products])

    except Exception as e:
        return error_response(str(e), 500)


# ✅ GET /api/products/<id> — Get product by ID
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        conn = get_db_connection()
        product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        conn.close()

        if product is None:
            return error_response("Product not found", 404)

        return success_response(dict(product))

    except Exception as e:
        return error_response(str(e), 500)


# ✅ Custom 404 error handler
@app.errorhandler(404)
def not_found(e):
    return error_response("Resource not found", 404)


# ✅ Custom 400 error handler
@app.errorhandler(400)
def bad_request(e):
    return error_response("Bad request", 400)


# ✅ Run the API
if __name__ == '__main__':
    app.run(debug=True)
