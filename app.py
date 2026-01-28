import os
from flask import Flask, render_template, jsonify, request
from ml.price_predictor import price_predictor
from ml.crop_recommender import crop_recommender
from database.models import init_db, get_markets, get_schemes
import requests
from math import radians, cos, sin, asin, sqrt

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_key_123")

# Initialize Database on startup
init_db()

# Haversine formula for Market Finder
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers
    return c * r

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather')
def get_weather():
    lat = request.args.get('lat', 28.6139) # Defaults to Delhi
    lon = request.args.get('lon', 77.2090)
    api_key = os.getenv("OPENWEATHER_API_KEY", "b3986a10052d9217646a506509a25b2a") # Public fallback
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url).json()
        description = response['weather'][0]['description']
        temp = response['main']['temp']
        risk = "Safe"
        if "rain" in description.lower() or "storm" in description.lower():
            risk = "Alert: High moisture expected"
        elif temp > 35:
            risk = "Alert: Heatwave risk"
            
        return jsonify({
            "temp": temp,
            "description": description,
            "risk": risk
        })
    except Exception as e:
        return jsonify({"error": "Weather unavailable", "details": str(e)}), 500

@app.route('/api/predict-price')
def predict_price():
    crop = request.args.get('crop', 'Wheat')
    prediction = price_predictor.predict_next_month(crop)
    return jsonify(prediction)

@app.route('/api/recommend-crop')
def recommend_crop():
    soil = request.args.get('soil', 'Loamy')
    season = request.args.get('season', 'Winter')
    suggestions = crop_recommender.suggest(soil, season)
    return jsonify(suggestions)

@app.route('/api/markets')
def markets():
    user_lat = float(request.args.get('lat', 0))
    user_lon = float(request.args.get('lon', 0))
    all_markets = get_markets()
    
    for m in all_markets:
        m['distance'] = round(haversine(user_lon, user_lat, m['lon'], m['lat']), 2)
    
    # Sort by distance
    sorted_markets = sorted(all_markets, key=lambda x: x['distance'])
    return jsonify(sorted_markets)

@app.route('/api/schemes')
def schemes():
    return jsonify(get_schemes())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
