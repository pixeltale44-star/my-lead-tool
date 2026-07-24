import streamlit as st
import pandas as pd
import requests

# --- 🔑 CUSTOMER DATABASE ---
USER_DATABASE = {
    "admin123": "Master Admin",
    "user_pro_2026": "Premium Subscriber",
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
        key = st.text_input("Enter License Key", type="password")
        if st.button("Access Dashboard"):
            if key in USER_DATABASE:
                st.session_state["authenticated"] = True
                st.session_state["user_info"] = USER_DATABASE[key]
                st.rerun()
            else:
                st.error("Invalid Key.")
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
            st.error("Search error. Check API connection.")

# --- MAIN INTERFACE ---
if check_login():
    st.set_page_config(page_title="AI Lead Gen PRO", layout="wide")
    st.title(f"🚀 Dashboard: {st.session_state['user_info']}")
    
    with st.sidebar:
        st.header("Settings")
        my_name = st.text_input("Your Agency Name", "AI Expert")
        if st.button("Log Out"):
            st.session_state["authenticated"] = False
            st.rerun()

    # Inputs
    c1, c2 = st.columns(2)
    with c1: niche = st.text_input("Niche (e.g. Lawyers)")
    with c2: location = st.text_input("City (e.g. Miami)")

    if st.button("🔥 Start Lead Scan"):
        finder = LeadFinder(location, niche)
        with st.spinner("Scanning Google Maps..."):
            finder.fetch()
            
            if finder.leads:
                for i, lead in enumerate(finder.leads):
                    name = lead.get("title")
                    site = lead.get("website")
                    
                    # THE EXPERT PREVIEW LAYOUT
                    with st.expander(f"PROSPECT: {name}"):
                        col_left, col_right = st.columns([1, 1])
                        
                        with col_left:
                            st.subheader("✉️ AI Sales Pitch")
                            if not site:
                                msg = f"Hi {name}, I noticed you're missing a website on Google. I can build one on Hostinger today. Link: {HOSTINGER_AFFILIATE}"
                            else:
                                msg = f"Hi {name}, your site at {site} needs an AI speed boost. Move to Hostinger here: {HOSTINGER_AFFILIATE}"
                            st.text_area("Pitch:", msg.replace("Expert", my_name), height=200, key=f"pitch_{i}")
                            st.info(f"📞 Phone: {lead.get('phone', 'Not listed')}")

                        with col_right:
                            st.subheader("🌐 Website Preview")
                            if site:
                                st.write(f"Analyzing: {site}")
                                # Try to show the website inside the app
                                st.components.v1.iframe(site, height=400, scrolling=True)
                                st.markdown(f"[Open site in new tab]({site})")
                            else:
                                st.error("No website found—This is a HIGH VALUE lead!")
                                st.write(f"Targeting: {name}")
                                st.write(f"Location: {lead.get('address')}")
            else:
                st.info("No leads found. Check your search terms.")
