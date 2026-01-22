import streamlit as st
from src.kpi_utils import load_data, calculate_kpis

st.title("📊 Online Sales KPI Dashboard")

df = load_data()
total, monthly, category = calculate_kpis(df)

st.metric("Total Revenue", f"${total:,.2f}")
st.bar_chart(monthly)
st.bar_chart(category)