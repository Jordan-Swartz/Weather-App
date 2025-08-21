from collections import deque

import streamlit as st

import streamlit as st

st.set_page_config(page_title="Weather App", layout="wide")

# Session State Initialization
if "last_query" not in st.session_state:
    st.session_state.last_query = None

if "history" not in st.session_state:
    st.session_state.history = deque(maxlen=5)

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

# Collect Input
with st.form(key="weather_form"):
    location_text = st.text_input(
        "Please enter your location",
        placeholder="San Jose, CA 95123"
    )
    submitted = st.form_submit_button("Submit") #reruns script upon submitting

if submitted:
    text = (location_text or "").strip()
    st.session_state.last_query = text or None
    if text:
        if text in st.session_state.history:
            st.session_state.history.remove(text) #remove duplicates
        st.session_state.history.appendleft(text) #add to top
        st.rerun()

if st.session_state.last_query is None:
    st.info("No location entered")
else:
    st.success(f"You searched for {st.session_state.last_query}")


# How To
# st.subheader("How To Use")


# Metric Widgets
# a, b = st.columns(2)
# c, d = st.columns(2)
#
# a.metric("Temperature", "30°F", "-9°F", border=True)
# b.metric("Wind", "4 mph", "2 mph", border=True)
#
# c.metric("Humidity", "77%", "5%", border=True)
# d.metric("Pressure", "30.34 inHg", "-2 inHg", border=True)