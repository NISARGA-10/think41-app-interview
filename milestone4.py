import sqlite3

def migrate():
    conn = sqlite3.connect('products.db')
    cur = conn.cursor()

    # 1. Create departments table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        manager TEXT
    )
    ''')

    # 2. Extract unique departments from products table
    cur.execute('SELECT DISTINCT department FROM products')
    departments = cur.fetchall()

    # 3. Insert unique departments into departments table
    for (dept,) in departments:
        cur.execute('INSERT OR IGNORE INTO departments (name) VALUES (?)', (dept,))

    conn.commit()

    # 4. Add department_id column to products (if not already exists)
    try:
        cur.execute('ALTER TABLE products ADD COLUMN department_id INTEGER')
    except sqlite3.OperationalError:
        # Column already exists
        pass

    # 5. Update department_id in products based on departments table
    cur.execute('''
    UPDATE products SET department_id = (
        SELECT id FROM departments WHERE departments.name = products.department
    )
    ''')

    conn.commit()

    # 6. (Optional) Recreate products table without old department column
    # Note: SQLite does not support DROP COLUMN directly
    # So here’s how you can do it safely:

    # Create new table without 'department' column
    cur.execute('''
    CREATE TABLE IF NOT EXISTS products_new (
        id INTEGER PRIMARY KEY,
        cost REAL,
        category TEXT,
        name TEXT,
        brand TEXT,
        retail_price REAL,
        sku TEXT,
        distribution_center_id INTEGER,
        department_id INTEGER,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    )
    ''')

    # Copy data from old products to new (excluding 'department' text column)
    cur.execute('''
    INSERT OR IGNORE INTO products_new (id, cost, category, name, brand, retail_price, sku, distribution_center_id, department_id)
    SELECT id, cost, category, name, brand, retail_price, sku, distribution_center_id, department_id FROM products
    ''')

    conn.commit()

    # Drop old products table
    cur.execute('DROP TABLE products')

    # Rename new table to products
    cur.execute('ALTER TABLE products_new RENAME TO products')

    conn.commit()
    conn.close()
    print("Migration completed successfully.")

if __name__ == "__main__":
    migrate()
