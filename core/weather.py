from __future__ import annotations
import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd

BASE_URL = "https://api.open-meteo.com/v1/forecast"

# --- One-time client setup: cache + retry ---
_cache = requests_cache.CachedSession(".cache", expire_after=3600)  # 1h cache
_session = retry(_cache, retries=5, backoff_factor=0.2)
_client = openmeteo_requests.Client(session=_session)

WEATHER_CODE = {
    0: "Clear",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Heavy drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Heavy rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm + hail",
    99: "Thunderstorm + heavy hail",
}

def get_current_weather(lat: float, lon: float, unit="fahrenheit"):
    params = {
        "latitude": lat,
        "longitude": lon,
        "timezone": "auto",
        "temperature_unit": unit,
        "wind_speed_unit": "mph",
        "current": "temperature_2m,relative_humidity_2m,weathercode,windspeed_10m",
        "daily":"temperature_2m_max,temperature_2m_min",
    }
    # request via open-meteo client
    response = _client.weather_api(BASE_URL, params=params)
    resp = response[0]
    current = resp.Current()

    # extract array data
    temperature = current.Variables(0).Value()
    humidity = current.Variables(1).Value()
    weather_code = int(current.Variables(2).Value())
    wind_mph = float(current.Variables(3).Value())
    daily = resp.Daily()
    today_high = daily.Variables(0).ValuesAsNumpy()[0]
    today_low = daily.Variables(0).ValuesAsNumpy()[0]

    return {
        "temperature": temperature,
        "humidity": humidity,
        "weathercode": weather_code,
        "condition": WEATHER_CODE.get(weather_code, "—"),
        "wind_mph": wind_mph,
        "today_high": float(today_high),
        "today_low": float(today_low),
    }
def get_forecast(lat: float, lon: float, days: int = 5, unit="fahrenheit"):
    params = {
        "latitude": lat,
        "longitude": lon,
        "timezone": "auto",
        "temperature_unit": unit,
        "precipitation_unit": "inch",
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max",
        "forecast_days": days,
    }

    responses = _client.weather_api(BASE_URL, params=params)
    resp = responses[0]
    daily = resp.Daily()

    # extract array data
    codes = daily.Variables(0).ValuesAsNumpy()
    tmax  = daily.Variables(1).ValuesAsNumpy()
    tmin  = daily.Variables(2).ValuesAsNumpy()
    psum  = daily.Variables(3).ValuesAsNumpy()
    pprob = daily.Variables(4).ValuesAsNumpy()

    # Build readable date strings
    dates = pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left",
    ).tz_convert(None).strftime("%Y-%m-%d").tolist()

    rows = []
    for i, d in enumerate(dates):
        rows.append({
            "date": d,
            ("high_f" if unit == "fahrenheit" else "high_c"): float(tmax[i]),
            ("low_f"  if unit == "fahrenheit" else "low_c"):  float(tmin[i]),
            "precip_in": float(psum[i]),
            "precip_prob_%": int(pprob[i]),
            "condition": WEATHER_CODE.get(int(codes[i]), "—"),
        })
    return rows
