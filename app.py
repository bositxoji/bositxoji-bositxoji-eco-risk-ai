import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_google_auth import Authenticate

# --- 1. SOZLAMALAR ---
# Google Cloud va Secrets dan olinadigan kalitlar
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]

st.set_page_config(page_title="Eko-Risk AI O'zbekiston", layout="wide")

# Google Auth sozlamasi - To'g'ri va yagona blok
auth = Authenticate(
    secret_key="ixtiyoriy_matn_123",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="https://eko-risk-ai-uz.streamlit.app",
    cookie_name="google_auth_cookie"
)

# Login tugmasini chiqarish
user_info = auth.check_authenticity()

# Sidebar: Foydalanuvchi va Chiqish
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2913/2913520.png", width=100)
if user_info:
    st.sidebar.success(f"Foydalanuvchi: {user_info.get('name')}")
    
    if st.sidebar.button("Tizimdan chiqish"):
        auth.logout()

# --- 2. ASOSIY SAHIFA ---
st.title("🌍 Global Ekologik Risklar va AI Tahlili")

tabs = st.tabs(["📊 Global Xarita", "🔬 AI Risk Analizi", "⚖️ Qonuniy Mezonlar"])

with tabs[0]:
    st.subheader("Dunyo bo'yicha ekologik holat (Interaktiv)")
    st.info("Bu bo'limda global ekologik ma'lumotlar vizualizatsiyasi ko'rsatiladi.")
