# 🌦️Weather App 🌦
A Python and Streamlit-based web application that provides current weather conditions and a 5-day forecast based on user-selected locations.

---

## 1: 📌 About the Project:
This project is a weather forecasting tool built with Python and Streamlit.
It allows users to:
- Search for locations (city, ZIP, GPS coordinates, landmarks).
- View current weather (temperature, humidity, condition, wind speed).
- See a 5-day forecast displayed in a structured table.
- Keep a history of recent searches.
- Persist queries (location + date range) in a database with CRUD support (In Progress)
- The app integrates with the Open-Meteo API for geocoding and weather data, and uses SQLite for persistence.

---

## 2: 🔍 Featured Concepts:
1. API Integration
   - Open-Meteo Geocoding API 
     - Converts user input (city, ZIP, GPS, etc.) into latitude and longitude.
   - Open-Meteo Forecast API
     - Fetches current conditions and daily forecasts (temperature, precipitation, humidity, weather codes).
2. Current Weather Dashboard
   - Displays key metrics with Streamlit’s `st.metric`:
     - Temperature (°F/°C)
     - Humidity (%)
     - Condition (mapped from weather codes)
     - Wind Speed (mph)
3. 5-Day Forecast
   - Tabular forecast using st.dataframe. 
   - Shows date, high/low temperature, precipitation, probability, and condition.
4. Search History & State
   - Uses Streamlit session state to store recent searches in sidebar
5. Streamlit-Powered UI
   - Simple, responsive, interactive, and modular UI.
    
---

## 3: 🚀 Running the Project:
### 🔗 Public Link
- Streamlit Link: [Project Link](https://jswartzweatherapp.streamlit.app)

### 🎥 Project Demo
- Screencast: [Project Demo](https://youtu.be/x4iXwUUqWkw)
---

## 4: 🛠 Technologies & Resources Used:
1. Python 3.9.6
   - core programming language
2. Streamlit
   - frontend and deployment
3. Open-Meteo APIs 
   - → geocoding + forecast data
4. SQLite (sqlite3)
   - persistence layer for CRUD operations

---


