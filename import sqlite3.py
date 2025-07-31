import sqlite3
import pandas as pd

# Step 1: Load CSV
csv_path = 'products.csv'  # Make sure this file exists in the same directory
df = pd.read_csv(csv_path)

# Step 2: Connect to SQLite database
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# Step 3: Create 'products' table with your actual columns
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    cost REAL,
    category TEXT,
    name TEXT,
    brand TEXT,
    retail_price REAL,
    department TEXT,
    sku TEXT,
    distribution_center_id INTEGER
)
''')

# Step 4: Load CSV data into the table
df.to_sql('products', conn, if_exists='replace', index=False)

# Step 5: Verify the load - print first 10 rows
print("✅ First 10 products loaded into the database:")
cursor.execute('SELECT * FROM products LIMIT 10')
for row in cursor.fetchall():
    print(row)

# Step 6: Print total row count
cursor.execute('SELECT COUNT(*) FROM products')
count = cursor.fetchone()[0]
print(f"\n✅ Total number of products in the database: {count}")

# Step 7: Close connection
conn.close()
