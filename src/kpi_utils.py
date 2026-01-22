import sqlite3
import pandas as pd

def load_data(db_path="data/sales.db"):
    conn = sqlite3.connect(db_path)
    df_sales = pd.read_sql("SELECT * FROM sales", conn)
    df_products = pd.read_sql("SELECT * FROM products", conn)
    df_customers = pd.read_sql("SELECT * FROM customers", conn)
    conn.close()

    # Merge into one DataFrame
    df = (
        df_sales
        .merge(df_products, on="product_id", how="left")
        .merge(df_customers, on="customer_id", how="left")
    )

    # Ensure 'date' column exists and is parsed
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["month"] = df["date"].dt.month
    else:
        raise ValueError("❌ 'date' column not found in sales table")

    return df


def calculate_kpis(df):
    # Total revenue
    total_revenue = df["revenue"].sum()

    # Monthly revenue (safe check)
    if "month" in df.columns:
        monthly_revenue = df.groupby("month")["revenue"].sum()
    else:
        monthly_revenue = pd.Series(dtype="float64")

    # Category revenue (safe check)
    if "category" in df.columns:
        category_revenue = df.groupby("category")["revenue"].sum()
    else:
        category_revenue = pd.Series(dtype="float64")

    return total_revenue, monthly_revenue, category_revenue