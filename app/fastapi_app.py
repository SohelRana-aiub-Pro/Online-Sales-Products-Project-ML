from fastapi import FastAPI
from fastapi.responses import FileResponse
import joblib, numpy as np
import os

app = FastAPI(title="Online Sales Products Project API")
model = joblib.load("models/best_model.pkl")

@app.get("/")
def read_root():
    return {"message": "Welcome to Online Sales Products Project API. Use /predict to get revenue predictions."}

@app.get("/predict")
def predict(quantity: int, price: float, age: int, month: int):
    features = np.array([[quantity, price, age, month]])
    prediction = model.predict(features)[0]
    return {"predicted_revenue": prediction}

# Optional: serve a favicon to stop 404
@app.get("/favicon.ico")
def favicon():
    # If you have an icon file, serve it
    icon_path = os.path.join("data", "outputs", "favicon.ico")
    if os.path.exists(icon_path):
        return FileResponse(icon_path)
    # Otherwise return nothing
    return {"message": "No favicon set"}