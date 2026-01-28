document.addEventListener('DOMContentLoaded', () => {
    // Initial Load
    getLocation();
    loadPricePrediction();
    loadSchemes();
    
    // Setup Language Selector
    const langSelect = document.getElementById('lang-select');
    langSelect.addEventListener('change', (e) => {
        SpeechEngine.setLanguage(e.target.value);
    });
});

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            updateWeather(lat, lon);
            updateMarkets(lat, lon);
        }, error => {
            console.error("Geo error:", error);
            updateWeather(28.61, 77.20); // Default to Delhi
        });
    }
}

async function updateWeather(lat, lon) {
    const weatherEl = document.getElementById('weather-info');
    try {
        const response = await fetch(`/api/weather?lat=${lat}&lon=${lon}`);
        const data = await response.json();
        
        weatherEl.innerHTML = `
            <div class="card ${data.risk !== 'Safe' ? 'alert' : ''}">
                <h2>🌡️ Weather & Risk</h2>
                <p>Temperature: ${data.temp}°C</p>
                <p>Condition: ${data.description}</p>
                <p><strong>${data.risk}</strong></p>
                <button class="btn-voice" onclick="SpeechEngine.speak('Current temperature is ${data.temp} degrees with ${data.description}. Status is ${data.risk}')">
                    🔊 Listen Alert
                </button>
            </div>
        `;
        OfflineStore.save('weather', data);
    } catch (e) {
        const cached = OfflineStore.get('weather');
        if (cached) weatherEl.innerHTML = `<p>Offline: ${cached.temp}°C - ${cached.risk}</p>`;
    }
}

async function loadPricePrediction() {
    const crop = document.getElementById('crop-select').value;
    const container = document.getElementById('price-info');
    
    const response = await fetch(`/api/predict-price?crop=${crop}`);
    const data = await response.json();
    
    const trendClass = data.trend === 'up' ? 'prediction-up' : 'prediction-down';
    const trendText = data.trend === 'up' ? 'Increasing 📈' : 'Decreasing 📉';

    container.innerHTML = `
        <div class="card">
            <h2>💰 Price Forecast</h2>
            <p>Current Market Price: ₹${data.current_price}</p>
            <p>Predicted (Next Month): <span class="${trendClass}">₹${data.predicted_price}</span></p>
            <p>Trend: ${trendText} (${data.confidence} confidence)</p>
            <button class="btn-voice" onclick="SpeechEngine.speak('Price for ${crop} is expected to be ${data.predicted_price} rupees next month, which is ${data.trend}')">
                🔊 Listen Advice
            </button>
        </div>
    `;
}

async function loadSuggestions() {
    const soil = document.getElementById('soil-select').value;
    const season = document.getElementById('season-select').value;
    const container = document.getElementById('suggestion-info');
    
    const response = await fetch(`/api/recommend-crop?soil=${soil}&season=${season}`);
    const data = await response.json();
    
    let html = '<div class="card"><h2>🌱 Crop Advice</h2>';
    data.forEach(item => {
        html += `
            <div class="scheme-item">
                <strong>${item.crop}</strong> - ${item.reason}<br>
                <small>Profit: ${item.profit_potential}</small>
            </div>
        `;
    });
    html += '</div>';
    container.innerHTML = html;
}

async function updateMarkets(lat, lon) {
    const container = document.getElementById('market-info');
    const response = await fetch(`/api/markets?lat=${lat}&lon=${lon}`);
    const data = await response.json();
    
    let html = '<div class="card"><h2>🏪 Nearby Markets</h2>';
    data.slice(0, 3).forEach(m => {
        html += `
            <div class="scheme-item">
                <strong>${m.name}</strong> (${m.distance} km away)<br>
                📞 ${m.contact}
            </div>
        `;
    });
    html += '</div>';
    container.innerHTML = html;
}

async function loadSchemes() {
    const container = document.getElementById('scheme-info');
    const response = await fetch(`/api/schemes`);
    const data = await response.json();
    
    let html = '<div class="card"><h2>📜 Govt Schemes</h2>';
    data.forEach(s => {
        html += `
            <div class="scheme-item">
                <strong>${s.name}</strong><br>
                <small>${s.benefit}</small><br>
                <a href="${s.link}" target="_blank">Apply Here</a>
            </div>
        `;
    });
    html += '</div>';
    container.innerHTML = html;
}
