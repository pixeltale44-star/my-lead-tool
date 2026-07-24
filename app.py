import streamlit as st
import pandas as pd
import requests

# --- 1. MUST BE FIRST ---
st.set_page_config(page_title="AI Lead Gen PRO", layout="wide")

# --- 2. DATABASE ---
USER_DATABASE = {
    "ahmad123": "Ahmad - Master Admin",
    "pro_user_2026": "Premium Subscriber",
    "memuna123": "Master Admin"
}

# --- 3. CONFIGURATION ---
REAL_API_KEY = "b940832ef990aa072bc43da75530e0ef4aa2d8a12e53b0103e37b022154872bc"
HOSTINGER_AFFILIATE = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

# --- 4. LOGIN SYSTEM ---
def check_login():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        st.title("🛡️ Pro SaaS Login")
        key = st.text_input("Enter License Key", type="password").strip()
        
        if st.button("Access Dashboard"):
            if key in USER_DATABASE:
                st.session_state["authenticated"] = True
                st.session_state["user_info"] = USER_DATABASE[key]
                st.rerun()
            else:
                st.error("Invalid Key. Please check the spelling.")
        return False
    return True

# --- 5. SEARCH ENGINE ---
class LeadFinder:
    def __init__(self, location, niche):
        self.location = location
        self.niche = niche
        self.leads = []

    def fetch(self):
        try:
            p = {"engine": "google_maps", "q": f"{self.niche} in {self.location}", "api_key": REAL_API_KEY}
            r = requests.get("https://serpapi.com/search", params=p)
            self.leads = r.json().get("local_results", [])
        except:
            st.error("Connection Error. Please check API limits.")

# --- 6. MAIN APP ---
if check_login():
    st.title(f"🚀 Welcome, {st.session_state['user_info']}")
    
    with st.sidebar:
        st.header("Settings")
        my_name = st.text_input("Your Agency Name", "Expert")
        if st.sidebar.button("Logout"):
            st.session_state["authenticated"] = False
            st.rerun()

    n = st.text_input("Niche (e.g. Dentists)")
    l = st.text_input("City (e.g. New York)")

    if st.button("🔥 Find High-Value Leads"):
        if n and l:
            finder = LeadFinder(l, n)
            with st.spinner("Searching Google Maps..."):
                finder.fetch()
                if finder.leads:
                    st.success(f"Found {len(finder.leads)} Opportunities")
                    for i, lead in enumerate(finder.leads):
                        name = lead.get("title")
                        site = lead.get("website")
                        with st.expander(f"Lead: {name}"):
                            cl, cr = st.columns(2)
                            with cl:
                                st.subheader("✉️ AI Pitch")
                                if not site:
                                    msg = f"Hi {name} Team, I noticed you're missing a website on Google. I can build you one on Hostinger in 48 hours. Link: {HOSTINGER_AFFILIATE}"
                                else:
                                    msg = f"Hi {name} Team, your site at {site} needs a speed boost. Moving to Hostinger's AI hosting will help. Link: {HOSTINGER_AFFILIATE}"
                                st.text_area("Ready Pitch:", msg, height=150, key=f"p_{i}")
                            with cr:
                                st.subheader("🌐 Preview")
                                if site:
                                    st.components.v1.iframe(site, height=350)
                                else:
                                    st.warning("No site found—High Value!")
        else:
            st.warning("Please fill in both fields.")
