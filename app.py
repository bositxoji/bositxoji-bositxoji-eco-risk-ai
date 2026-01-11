import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
from datetime import datetime

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Risk Global AI", layout="wide")

# Session State
if 'lang' not in st.session_state: st.session_state.lang = 'UZ'
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# 2. YUQORI DARARAJALI EKO-DIZAYN (CSS)
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #050505;
        color: #ffffff;
    }}
    /* 3 TA NUQTA MENYUSINI KO'RINARLI QILISH */
    [data-testid="stPopover"] {{
        position: fixed; top: 25px; left: 25px; z-index: 100000;
    }}
    button[aria-haspopup="dialog"] {{
        background-color: #00FF41 !important; /* Matrix/Neon Green */
        color: black !important;
        font-weight: bold !important;
        font-size: 24px !important;
        border-radius: 50% !important;
        width: 50px !important; height: 50px !important;
        border: 3px solid #ffffff !important;
    }}
    /* Matnlar ko'rinishi */
    h1, h2, h3, p {{
        color: #00FF41 !important;
        text-shadow: 0 0 10px rgba(0,255,65,0.5);
    }}
    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(0, 255, 65, 0.1);
        border-radius: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. INTERAKTIV GLOBUS MA'LUMOTLARI (Simulyatsiya)
data = pd.DataFrame({
    'lat': [41.2995, 51.5074, 40.7128, 35.6762, -33.8688, 55.7558],
    'lon': [69.2401, -0.1278, -74.0060, 139.6503, 151.2093, 37.6173],
    'city': ['Tashkent', 'London', 'New York', 'Tokyo', 'Sydney', 'Moscow'],
    'temp': [12, 8, 4, 15, 28, -5],
    'eco_risk': ['O\'rta', 'Past', 'Yuqori', 'O\'rta', 'Yuqori', 'O\'rta'],
    'earthquake': ['3.2', '0', '1.2', '4.5', '0', '0.5']
})

# 4. CHAP YASHIL MENYU (3 TA NUQTA)
with st.popover("⋮"):
    st.subheader("⚙️ Boshqaruv")
    lang = st.radio("Til / Язык", ["UZ", "RU", "EN"], horizontal=True)
    st.session_state.lang = lang
    
    st.markdown("---")
    if st.button("🎓 Muallif haqida"):
        st.info("Professor Egamberdiyev E.A. va PhD tadqiqotchi Ataxo'jayev Abdubositxo'ja.")
    
    if st.button("🔑 Tizimga kirish/chiqish"):
        st.session_state.logged_in = not st.session_state.logged_in
        st.rerun()

# 5. ASOSIY QISM
st.title("🌍 Global Eko-Monitoring Real-Time AI")

# Globus qismi
st.subheader("🗺 Interaktiv Yer shari (Davlatlar va Harorat)")

view_state = pdk.ViewState(latitude=41.29, longitude=69.24, zoom=1.5, pitch=45)

layer = pdk.Layer(
    "ColumnLayer",
    data,
    get_position='[lon, lat]',
    get_elevation='temp * 10000',
    elevation_scale=100,
    radius=200000,
    get_fill_color="[temp > 20 ? 255 : 0, temp < 10 ? 255 : 150, 0, 140]",
    pickable=True,
    auto_highlight=True,
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "Shahar: {city}\nHarorat: {temp}°C\nEko-risk: {eco_risk}\nZilzila: {earthquake} ball"},
    map_style="mapbox://styles/mapbox/satellite-v9"
)

st.pydeck_chart(r)

# 6. DINAMIK YANGILIKLAR VA TAHLIL
if st.session_state.logged_in:
    t1, t2 = st.tabs(["🔥 Favqulodda xabarlar", "📊 Batafsil Tahlil"])
    with t1:
        st.error(f"⚠️ {datetime.now().strftime('%H:%M')} - Yaponiya sohillarida 4.5 balli zilzila qayd etildi.")
        st.warning("💨 Toshkent: Havo ifloslanishi me'yordan 1.2 barobar yuqori.")
    with t2:
        st.write("Havodagi zaharli moddalar (PM2.5) tahlili AI tomonidan amalga oshirilmoqda...")
        st.line_chart(np.random.randn(20, 3))
else:
    st.info("Batafsil ma'lumotlar va AI tahlilini ko'rish uchun menyu (⋮) orqali tizimga kiring.")
