import os
import sqlite3, random
from faker import Faker

fake = Faker()
conn = sqlite3.connect("data/sales.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT, category TEXT, price REAL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT, location TEXT, age INTEGER)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY,
    product_id INTEGER, customer_id INTEGER,
    date TEXT, quantity INTEGER, revenue REAL,
    FOREIGN KEY(product_id) REFERENCES products(product_id),
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id))""")

# Insert synthetic products
categories = ["Electronics","Fashion","Home","Sports","Books"]
for _ in range(50):
    cursor.execute("INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
                   (fake.word(), random.choice(categories), round(random.uniform(10, 500), 2)))

# Insert synthetic customers
for _ in range(200):
    cursor.execute("INSERT INTO customers (name, location, age) VALUES (?, ?, ?)",
                   (fake.name(), fake.city(), random.randint(18, 65)))

# Insert synthetic sales
for _ in range(1000):
    product_id = random.randint(1, 50)
    customer_id = random.randint(1, 200)
    quantity = random.randint(1, 5)
    price = cursor.execute("SELECT price FROM products WHERE product_id=?", (product_id,)).fetchone()[0]
    revenue = price * quantity
    cursor.execute("INSERT INTO sales (product_id, customer_id, date, quantity, revenue) VALUES (?, ?, ?, ?, ?)",
                   (product_id, customer_id, fake.date_between(start_date='-1y', end_date='today'), quantity, revenue))

conn.commit()
conn.close()