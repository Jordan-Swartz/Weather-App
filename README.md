# 🌦️Weather App 🌦
A Python and Streamlit-based web application that provides current weather conditions and a 5-day forecast based on user-selected locations.

---

## 1: 📌 About the Project:
A Python and Streamlit-based web application that recommends the most relevant job candidates based on a provided job description. The engine uses modern NLP techniques to generate semantic embeddings of resumes and job descriptions, then computes similarity scores to rank candidates. 

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
- Streamlit Link: [Project Link](https://jordan-swartz-candidate-recommendation-app-qmui0u.streamlit.app/)

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


