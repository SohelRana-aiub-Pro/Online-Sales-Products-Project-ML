import sqlite3, pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

conn = sqlite3.connect("data/sales.db")
df = pd.read_sql("SELECT s.*, p.price, c.age, strftime('%m', s.date) as month \
                  FROM sales s JOIN products p ON s.product_id=p.product_id \
                  JOIN customers c ON s.customer_id=c.customer_id", conn)
conn.close()

X = df[["quantity", "price", "age", "month"]].astype(float)
y = df["revenue"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {"Linear Regression": LinearRegression(),
          "Random Forest": RandomForestRegressor()}

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    print(f"{name} RMSE (Online Sales Products Project): {rmse:.2f}")

best_model = RandomForestRegressor()
best_model.fit(X_train, y_train)

joblib.dump(best_model, "models/best_model.pkl")