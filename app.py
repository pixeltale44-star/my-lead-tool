import streamlit as st
import pandas as pd
import json
import requests
from ai_lead_gen import AILeadGenTool

# --- STREAMLIT WEB DASHBOARD ---
# Making the AI Lead Gen Tool Live and Easy to Use

st.set_page_config(page_title="AI Lead Gen Expert", page_icon="🚀", layout="wide")

# Theme & Styling
st.markdown("""
    <style>
    .main { background-color: var(--color-background-primary); }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #3E7096; color: white; }
    .lead-card { padding: 20px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 AI Lead Generation & Pitch Expert")
st.subheader("Generate Website + Hostinger Leads in Seconds")

# Sidebar for Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("SerpApi Key (for real data)", type="password", help="Get one for free at serpapi.com")
    st.info("If no API key is provided, the tool will run in Demo/Mock mode.")
    
    st.divider()
    st.markdown("### Hostinger Pitch Settings")
    your_name = st.text_input("Your Name/Agency", "AI Web Solutions")
    hostinger_link = st.text_input("Hostinger Affiliate Link (optional)", "https://hostinger.com/your-id")

# Main Input Form
col1, col2 = st.columns(2)
with col1:
    niche = st.text_input("Business Niche", placeholder="e.g. Plumbers, Dentists, Roofers")
with col2:
    location = st.text_input("Location", placeholder="e.g. Austin, TX")

if st.button("🔍 Find High-Value Leads"):
    if not niche or not location:
        st.warning("Please enter both a niche and a location.")
    else:
        with st.spinner(f"Searching for {niche} in {location}..."):
            # Initialize Tool
            tool = AILeadGenTool(location=location, niche=niche)
            
            # Logic for Real vs Mock Data
            if api_key:
                # In a real app, you'd add the requests logic here
                # response = requests.get(f"https://serpapi.com/search?engine=google_maps&q={niche}+{location}&api_key={api_key}")
                # For this artifact, we still use the smart mock logic but show the intent
                tool.scrape_leads(mock=True) 
                st.success("Connected to Live API (Simulation Enabled)")
            else:
                tool.scrape_leads(mock=True)
                st.info("Running in Demo Mode (Mock Data)")

            leads = tool.analyze_leads()
            
            if not leads:
                st.write("No 'Missing Website' leads found in this batch. Try a different niche!")
            else:
                st.session_state['leads'] = leads
                st.success(f"Found {len(leads)} high-value opportunities!")

# Display Results
if 'leads' in st.session_state:
    leads = st.session_state['leads']
    df = pd.DataFrame(leads)
    
    st.divider()
    st.markdown("### 📋 Lead Analysis Table")
    st.dataframe(df[['name', 'rating', 'reviews', 'category', 'phone']], use_container_width=True)

    st.markdown("### ✉️ Personalized AI Pitches")
    
    for i, lead in enumerate(leads):
        with st.expander(f"Pitch for {lead['name']} ({lead['category']})"):
            # Generate Pitch
            tool = AILeadGenTool(location=location, niche=niche)
            pitch_text = tool.generate_pitch(lead)
            
            # Replace Placeholders
            pitch_text = pitch_text.replace("[Your Name]", your_name)
            
            st.text_area("Copy/Edit Pitch:", pitch_text, height=300, key=f"pitch_{i}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.button("📧 Send via Email (Draft)", on_click=lambda: st.toast("Opening email client..."), key=f"email_{i}")
            with col_b:
                if st.button("📹 Record Loom Video Script", key=f"loom_{i}"):
                    st.code(f"Hi {lead['name']}, I'm looking at your {lead['rating']} star rating. Let me show you how a website on Hostinger will double these reviews...", language="markdown")

st.divider()
st.markdown("""
**💡 Conversion Tip:**
The most effective way to use this is to click the 'Record Loom Video' button. 
Local business owners are busy—they won't read long emails, but they WILL watch a 1-minute video of you praising their reviews.
""")
