import streamlit as st
import pandas as pd
import requests

# 1. THIS MUST BE THE VERY FIRST LINE
st.set_page_config(page_title="Lead Gen PRO", layout="wide")

# 2. Database of Keys
USER_KEYS = {
    "ahmad123": "Ahmad",
    "pro_user_2026": "Premium User",
    "memuna123": "Master Admin"
}

# 3. Setup
API_KEY = "b940832ef990aa072bc43da75530e0ef4aa2d8a12e53b0103e37b022154872bc"
AFFILIATE = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

# 4. Login Logic
if "login_state" not in st.session_state:
    st.session_state["login_state"] = False

if not st.session_state["login_state"]:
    st.title("🛡️ Pro SaaS Login")
    user_key = st.text_input("Enter License Key", type="password").strip()
    if st.button("Login"):
        if user_key in USER_KEYS:
            st.session_state["login_state"] = True
            st.session_state["user_name"] = USER_KEYS[user_key]
            # No rerun command here to prevent crashes
            st.info("Login successful! Click the button again or refresh to enter.")
        else:
            st.error("Invalid Key.")
else:
    # 5. The Main App (Only runs after login)
    st.title(f"🚀 Welcome, {st.session_state['user_name']}")
    
    with st.sidebar:
        st.header("Settings")
        if st.button("Logout"):
            st.session_state["login_state"] = False
            st.info("Logged out.")

    niche = st.text_input("Niche (e.g. Dentists)")
    city = st.text_input("City (e.g. New York)")

    if st.button("Find Leads"):
        if niche and city:
            with st.spinner("Searching..."):
                try:
                    params = {"engine": "google_maps", "q": f"{niche} in {city}", "api_key": API_KEY}
                    r = requests.get("https://serpapi.com/search", params=params)
                    leads = r.json().get("local_results", [])
                    
                    if leads:
                        st.success(f"Found {len(leads)} Leads!")
                        for i, lead in enumerate(leads):
                            name = lead.get("title")
                            site = lead.get("website")
                            with st.expander(f"Lead: {name}"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write("**AI Pitch**")
                                    pitch = f"Hi {name}, I noticed you need a better site on Hostinger: {AFFILIATE}"
                                    st.text_area("Pitch:", pitch, height=150, key=f"p_{i}")
                                with col2:
                                    st.write("**Preview**")
                                    if site:
                                        st.components.v1.iframe(site, height=350)
                                    else:
                                        st.warning("No website—High Value!")
                except:
                    st.error("Connection error.")
        else:
            st.warning("Enter Niche and City.")
