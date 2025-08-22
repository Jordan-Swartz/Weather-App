from collections import deque

import requests
import streamlit as st

from core.geocode import search_places

st.set_page_config(page_title="Weather App", layout="centered")
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

# Main UI
st.title("Weather App")
st.subheader("This Weather App is Pretty Cool")
st.divider()

# How To
st.subheader("How To Use")
col1, col2, col3 = st.columns(3, gap="medium", border=True)

with col1:
    st.subheader("Input Location")
    st.metric("City", "ZIP Code", "GPS ", border=True)

with col2:
    st.subheader("Select Result")
    st.button("Refresh")

with col3:
    st.subheader("View Forecast")
    st.metric("Temperature", "30°F", "-9°F", border=True)
st.divider()

# Collect Input
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
    st.button("Use Current Location")

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
    choice = st.selectbox("Confirm location", options=labels, index=0, key="confirm_select")
    if st.button("Use this location", key="confirm_btn"):
        picked = results[labels.index(choice)]
        st.session_state.selected_place = picked
        # Keep your history as strings for now (label is enough to test)
        if picked["label"] in st.session_state.history:
            st.session_state.history.remove(picked["label"])
        st.session_state.history.appendleft(picked["label"])
        st.rerun()

st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<br><br><br>", unsafe_allow_html=True)

# Metric Widgets
# a, b = st.columns(2)
# c, d = st.columns(2)
#
# a.metric("Temperature", "30°F", "-9°F", border=True)
# b.metric("Wind", "4 mph", "2 mph", border=True)
#
# c.metric("Humidity", "77%", "5%", border=True)
# d.metric("Pressure", "30.34 inHg", "-2 inHg", border=True)