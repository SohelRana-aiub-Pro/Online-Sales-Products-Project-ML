import streamlit as st, sqlite3, pandas as pd, matplotlib.pyplot as plt

conn = sqlite3.connect("data/sales.db")
df = pd.read_sql("SELECT * FROM sales", conn)
conn.close()

st.title("📊 Online Sales Products Project Dashboard")

st.metric("Total Revenue", f"${df['revenue'].sum():,.2f}")
st.metric("Total Sales", len(df))

fig, ax = plt.subplots()

df.groupby(pd.to_datetime(df['date']).dt.month)["revenue"].sum().plot(ax=ax)
ax.set_title("Monthly Revenue Trend (Online Sales Products Project)")
st.pyplot(fig)