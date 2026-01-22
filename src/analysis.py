import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure outputs folder exists
os.makedirs("data/outputs", exist_ok=True)

# Connect to SQLite database
conn = sqlite3.connect("data/sales.db")

# Load tables
df_sales = pd.read_sql("SELECT * FROM sales", conn)
df_products = pd.read_sql("SELECT * FROM products", conn)
df_customers = pd.read_sql("SELECT * FROM customers", conn)

conn.close()

# Merge tables into one DataFrame
df = (
    df_sales
    .merge(df_products, on="product_id", how="left")
    .merge(df_customers, on="customer_id", how="left")
)

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month

# --- Revenue by category ---
plt.figure(figsize=(8, 6))
sns.barplot(x="category", y="revenue", data=df, estimator=sum, ci=None)
plt.title("Revenue by Product Category (Online Sales Products Project)")
plt.xlabel("Product Category")
plt.ylabel("Total Revenue")
plt.tight_layout()
plt.savefig("data/outputs/revenue_by_category.jpg")
plt.close()

# --- Monthly revenue trend ---
monthly_rev = df.groupby("month")["revenue"].sum()


plt.figure(figsize=(8, 6))
monthly_rev.plot(kind="line", marker="o")
plt.title("Monthly Revenue Trend (Online Sales Products Project)")
plt.xlabel("Month")
plt.ylabel("Total Revenue")
plt.grid(True)
plt.tight_layout()
plt.savefig("data/outputs/monthly_revenue.jpg")
plt.close()