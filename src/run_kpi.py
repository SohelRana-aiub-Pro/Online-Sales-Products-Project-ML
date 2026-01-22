from src.kpi_utils import load_data, calculate_kpis

df = load_data()
total, monthly, category = calculate_kpis(df)




print("✅ Total Revenue:", total)
print("\n📅 Monthly Revenue:\n", monthly)
print("\n📦 Category Revenue:\n", category)