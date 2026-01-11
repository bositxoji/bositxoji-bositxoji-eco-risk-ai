import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Portal Pro", layout="wide")

# Til lug'ati (Sidebar va Menyu uchun)
lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t_dict = {
    "UZ": {
        "m1": "📊 Global AQI", 
        "m2": "🛰 Issiqlik Xaritasi", 
        "m3": "🤖 AI Risk Tahlil", 
        "m4": "📶 IoT Sensorlar"
    }
}
t = t_dict.get(lang, t_dict["UZ"])

# 2. SIDEBAR NAVIGATSIYA
with st.sidebar:
    st.title("🚀 Dashboard")
    menu = st.radio("Bo'limni tanlang:", list(t.values()))
    st.markdown("---")
    st.caption("Mualliflar: Prof. Egamberdiyev E.A. | PhD Ataxo'jayev A.")

# --- 1-BO'LIM: GLOBAL AQI ---
if menu == t['m1']:
    st.header(t['m1'])
    st.components.v1.iframe("https://aqicn.org/map/world/", height=700)

# --- 2-BO'LIM: ISSIQLIK XARITASI (TUZATILGAN) ---
elif menu == t['m2']:
    st.header(t['m2'])
    # Xaritadagi ValueError 'attr' qo'shish bilan tuzatildi
    m = folium.Map(location=[41.31, 69.24], zoom_start=6)
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google Satellite Imagery',
        name='Google Satellite'
    ).add_to(m)
    
    # Issiqlik ma'lumotlari simulyatsiyasi
    heat_data = [[41.31, 69.24, 0.9], [42.46, 59.61, 1.0], [37.22, 67.27, 0.8]]
    HeatMap(heat_data, radius=25, blur=15).add_to(m)
    folium_static(m, width=1100, height=600)
    st.success("✅ Issiqlik xaritasi yuklandi.")

# --- 3-BO'LIM: AI RISK TAHLIL ---
elif menu == t['m3']:
    st.header(t['m3'])
    # Secrets-dan foydalanish xavfsizlikni ta'minlaydi
    topic = st.text_area("Tahlil uchun mavzu:")
    if st.button("Tahlilni boshlash"):
        st.info("AI tahlil tayyorlamoqda... (GROQ_API_KEY Secrets-da bo'lishi shart)")

# --- 4-BO'LIM: IoT SENSORLAR (TIKLANGAN) ---
elif menu == t['m4']:
    st.header(t['m4'])
    # IoT ma'lumotlar jadvali
    iot_data = pd.DataFrame({
        'Hudud': ['Toshkent', 'Nukus', 'Termiz', 'Andijon'],
        'PM2.5': [45, 120, 95, 38],
        'AQI': [115, 185, 160, 68]
    })
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📋 Sensor ko'rsatkichlari")
        st.table(iot_data)
    with c2:
        st.subheader("📈 Vizualizatsiya")
        fig = px.bar(iot_data, x='Hudud', y='AQI', color='AQI', title="Mintaqaviy AQI tahlili")
        st.plotly_chart(fig, use_container_width=True)
