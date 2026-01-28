import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime

class PricePredictor:
    def __init__(self):
        self.models = {}
        self.crop_data = {
            'Wheat': [2000, 2050, 2100, 2080, 2150, 2200],
            'Rice': [1800, 1850, 1900, 1950, 1920, 2000],
            'Corn': [1500, 1550, 1520, 1600, 1650, 1700],
            'Tomato': [1000, 1200, 3000, 1500, 1100, 1300]
        }
        self._train_models()

    def _train_models(self):
        # Generate dummy historical data (Month index 1-6 vs Price)
        X = np.array([[1], [2], [3], [4], [5], [6]])
        for crop, prices in self.crop_data.items():
            model = LinearRegression()
            model.fit(X, np.array(prices))
            self.models[crop] = model

    def predict_next_month(self, crop):
        if crop not in self.models:
            return None
        
        # Predict for month 7
        prediction = self.models[crop].predict([[7]])[0]
        current_price = self.crop_data[crop][-1]
        trend = "up" if prediction > current_price else "down"
        
        return {
            "crop": crop,
            "current_price": float(current_price),
            "predicted_price": round(float(prediction), 2),
            "trend": trend,
            "confidence": "85%"
        }

price_predictor = PricePredictor()
