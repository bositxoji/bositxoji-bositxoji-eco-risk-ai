import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static

# ---------------------------------------------------------
# 1. GOOGLE SEARCH CONSOLE TASDIQLASH (META VA HTML FAYL)
# ---------------------------------------------------------
# HTML fayl usuli uchun (Zaxira)
if "google19952789cd1d86.html" in st.query_params:
    st.write("google-site-verification: google19952789cd1d86.html")
    st.stop()

# Sayt sozlamalari (layout va meta teglar uchun)
st.set_page_config(
    page_title="Eco-Portal Pro: Global Eko Risk Monitoring",
    page_icon="🌍",
    layout="wide"
)

# Siz yuborgan Meta Tag usuli (Asosiy)
st.markdown('<meta name="google-site-verification" content="maybg4-LdPKEKS8plcTQclxsDBM6XX8lGzOQIwbv0W8" />', unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. API VA SOZLAMALAR
# ---------------------------------------------------------
# Groq API kalitini Secrets bo'limidan olish
if "GROQ_API_KEY" not in st.secrets:
    st.error("Xatolik: Secrets bo'limiga 'GROQ_API_KEY' kiritilmagan!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Tilni tanlash
lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t_dict = {
    "UZ": {
        "title": "🌱 Eco-Portal Pro AI",
        "m1": "🌍 Global AQI (Jonli)", "m2": "🛰 Sun'iy Yo'ldosh", "m3": "🧪 AI Akademik Tahlil",
        "m4": "📈 PESTEL Strategiya", "m5": "📊 IoT Sensorlar (12 viloyat)", "m6": "🔮 2030 Bashorat",
        "m7": "⏳ Tarixiy Dinamika", "m8": "🤖 AI Chat Ekspert",
        "btn": "Tahlilni boshlash", "dl": "Hisobotni yuklab olish"
    },
    "EN": {
        "title": "🌱 Eco-Portal Pro AI",
        "m1": "🌍 Global AQI (Live)", "m2": "🛰 Satellite View", "m3": "🧪 AI Academic Analysis",
        "m4": "📈 PESTEL Strategy", "m5": "📊 IoT Sensors (12 regions)", "m6": "🔮 2030 Forecast",
        "m7": "⏳ Historical Dynamics", "m8": "🤖 AI Expert Chat",
        "btn": "Run Analysis", "dl": "Download Report"
    }
}
t = t_dict.get(lang, t_dict["UZ"])

# ---------------------------------------------------------
# 3. SIDEBAR VA NAVIGATSIYA
# ----------------
