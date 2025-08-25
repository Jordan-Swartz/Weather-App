import requests
import streamlit as st
import pandas as pd

from core.weather import get_forecast
from collections import deque
from core.geocode import search_places, get_ip_location
from core.weather import get_current_weather

st.set_page_config(page_title="Weather App", layout="centered")

# Header
with st.container():
    st.markdown(
        """
        <div style="
            background-color: #172A4F;
            border-radius: 15px;
            margin-bottom: 1rem;
            margin-top: 3rem;
            color: white;
            text-align: center;
        ">
            <h1 style="margin: 0.3em; font-size: 3rem;">
                🌤️ JDS Weather & Forecast
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# Page Layout
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1200px;   
        margin: 0 auto;      /* center */
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Session State Initialization
if "last_query" not in st.session_state:
    st.session_state.last_query = None

if "history" not in st.session_state:
    st.session_state.history = deque(maxlen=5)

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "selected_place" not in st.session_state:
    st.session_state.selected_place = None

# Sidebar UI
st.sidebar.title("Recent Locations")
if len(st.session_state.history) == 0:
    st.sidebar.caption("No history yet")
else:
    for item in st.session_state.history:
        if st.sidebar.button(item, key=f"hist-{item}"):
            st.session_state.last_query = item
            st.rerun()

st.divider()

# How To
st.subheader("How To Use")
col1, col2, col3, col4= st.columns(4, gap="medium", border=True)

with col1:
    st.subheader("Input Location 📍")
    st.badge("City: San Jose", icon=":material/check:", color="blue", width="stretch")
    st.badge("ZIP: 95634", icon=":material/check:", color="blue")
    st.badge("State: California", icon=":material/check:", color="blue")
    st.badge("GPS: 37.7749, -122.4194", icon=":material/check:", color="blue")

with col2:
    st.subheader("Select Result ✅ ")
    st.selectbox(
        "Confirm Location?",
        ("San Jose, California", "San José, Costa Rica", "San José, Philippines"),
    )

with col3:
    st.subheader("View Forecast 🌦️")
    st.metric("Temperature", "30°F", "-9°F", border=True)

with col4:
    st.subheader("Refresh History 📂")
    st.button("New York, New York")
    st.button("San Francisco, California")
    st.button("Truckers, Georgia")

st.divider()

# Collect Input
st.subheader("Get Started")
with st.form("search_form"):
    location_text = st.text_input(
        "Please enter your location (city, state, ZIP, GPS)",
        placeholder="San Jose"
    )
    submitted = st.form_submit_button("Search") #reruns script upon submitting

# Handle Submission
if submitted:
    text = (location_text or "").strip()
    st.session_state.last_query = text or None
    st.session_state.search_results = []
    st.session_state.selected_place = None

    if text and len(text) >= 2:
        # Process Request
        try:
            st.session_state.search_results = search_places(text, 5, "en")
        except requests.RequestException:
            st.error("Could not reach geocoding service. Please try again.")
            st.session_state.search_results = [] #clear error results

        # Confirm Matches
        if not st.session_state.search_results:
            st.error("No matching locations found. Try a different place or be more specific.")
        else:
            # Process History
            if text in st.session_state.history:
                st.session_state.history.remove(text) #remove duplicates
            st.session_state.history.appendleft(text) #add to top
            st.rerun()

col1, col2 = st.columns([0.2, 0.8])
with col1:
    if st.button("Use Current Location"):
        try:
            ip_location = get_ip_location()
            st.session_state.selected_place = ip_location
            st.session_state.search_results = []  # clear any old results
            label = ip_location["label"]

            # temp history as string
            if label in st.session_state.history:
                st.session_state.history.remove(label)
            st.session_state.history.appendleft(label)
            st.session_state.last_query = label
            st.rerun()

        except requests.RequestException:
            st.error("Could not reach IP location service. Please try again.")
        except Exception as e:
            st.error(f"Location error: {e}")

with col2:
    if st.session_state.last_query is None:
        st.info("No location entered")
    else:
        st.success(f"You searched for {st.session_state.last_query}")

# Geocoding Results
results = st.session_state.search_results
if results:
    labels = [p["label"] for p in results]
    # Display Results in Selectbox
    choice = st.selectbox("Confirm Location", options=labels, index=0, key="confirm_select")
    if st.button("Use This Location", key="confirm_btn"):
        picked = results[labels.index(choice)]
        st.session_state.selected_place = picked
        # Keep your history as strings for now (label is enough to test)
        if picked["label"] in st.session_state.history:
            st.session_state.history.remove(picked["label"])
        st.session_state.history.appendleft(picked["label"])
        st.rerun()

st.divider()

# Weather Results
st.subheader("Weather & Forecast")
st.write("Current Weather")

place = st.session_state.selected_place
if place:
    current_weather = get_current_weather(
        place["lat"],
        place["lon"],
        unit="fahrenheit"
    )
    a, b = st.columns(2)
    c, d = st.columns(2)
    with a:
        st.metric("Temperature", f"{current_weather['temperature']:.0f}°F",
          delta=f"{current_weather['temperature'] - current_weather['today_low']:.0f}° above low", border=True)
    with b:
        st.metric("Humidity", f"{current_weather['humidity']:.0f}%",
                  delta=f"{current_weather['humidity'] - 50}% vs. avg", border=True)
    with c:
        st.metric("Condition", current_weather['condition'], border=True)
    with d:
        st.metric("Wind", f"{current_weather['wind_mph']:.0f} mph", border=True)
else:
    st.info("Select a location to see current weather.")

st.write("Expected Forecast")
place = st.session_state.selected_place
if place:
    days = 5
    daily_rows = get_forecast(place["lat"], place["lon"], days=days, unit="fahrenheit")

    frame = pd.DataFrame(daily_rows)
    frame = frame.rename(columns={
        "date": "Date",
        "high_f": "High (°F)",
        "low_f": "Low (°F)",
        "precip_in": "Precip (in)",
        "precip_prob_%": "Precip Prob (%)",
        "condition": "Condition",
    })

    st.subheader(f"Next {days} Days")
    st.dataframe(frame, use_container_width=True)
else:
    st.info("Select a location to see expected forecast.")

st.divider()

# Feedback
st.subheader("Feedback")
sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
selected = st.feedback("thumbs")
if selected is not None:
    st.markdown(f"You selected: {sentiment_mapping[selected]}")
st.markdown("<br><br>", unsafe_allow_html=True)
