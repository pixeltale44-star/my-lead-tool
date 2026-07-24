import streamlit as st
import pandas as pd
import requests

# --- 🔑 CUSTOMER DATABASE (Exact Keys - No Spaces) ---
USER_DATABASE = {
    "memuna123": "Master Admin",
    "pro2026": "Premium User"
}

# --- CONFIGURATION ---
REAL_API_KEY = "b940832ef990aa072bc43da75530e0ef4aa2d8a12e53b0103e37b022154872bc"
HOSTINGER_AFFILIATE = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

# --- LOGIN SYSTEM ---
def check_login():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        st.title("🛡️ Pro SaaS Login")
        # Added .strip() to ignore accidental spaces
        key = st.text_input("Enter License Key", type="password").strip()
        if st.button("Access Dashboard"):
            if key in USER_DATABASE:
                st.session_state["authenticated"] = True
                st.session_state["user_info"] = USER_DATABASE[key]
                st.rerun()
            else:
                st.error(f"Invalid Key. (You entered: {key})")
        return False
    return True

# --- SEARCH ENGINE ---
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
            st.error("Connection error. Check API key.")

# --- MAIN APP ---
if check_login():
    st.set_page_config(page_title="AI Lead Gen PRO", layout="wide")
    st.title(f"🚀 Dashboard: {st.session_state['user_info']}")
    
    with st.sidebar:
        st.header("Control Panel")
        my_name = st.text_input("Your Name", "Expert")
        if st.button("Logout"):
            st.session_state["authenticated"] = False
            st.rerun()

    n = st.text_input("Niche (e.g. Lawyers)")
    l = st.text_input("City (e.g. London)")

    if st.button("🔥 Scan for Leads"):
        if n and l:
            finder = LeadFinder(l, n)
            with st.spinner("Searching..."):
                finder.fetch()
                if finder.leads:
                    for i, lead in enumerate(finder.leads):
                        name = lead.get("title")
                        site = lead.get("website")
                        with st.expander(f"PROSPECT: {name}"):
                            cl, cr = st.columns(2)
                            with cl:
                                st.subheader("AI Pitch")
                                if not site:
                                    msg = f"Hi {name}, I noticed you are missing a site. I can build one on Hostinger: {HOSTINGER_AFFILIATE}"
                                else:
                                    msg = f"Hi {name}, your site at {site} needs a speed boost on Hostinger: {HOSTINGER_AFFILIATE}"
                                st.text_area("Copy Pitch:", msg, height=150, key=f"p_{i}")
                            with cr:
                                st.subheader("Site Preview")
                                if site:
                                    st.components.v1.iframe(site, height=350)
                                else:
                                    st.warning("No site found—HIGH VALUE!")
        else:
            st.warning("Enter Niche and City.")
