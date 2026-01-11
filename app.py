import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eco-System Pro Global", layout="wide")

# 2. TO'LIQ DINAMIK TIL TIZIMI
languages = {
    "UZ": {
        "title": "Eco-System Pro",
        "menu": ["Global AQI", "Carbon Footprint", "Issiqlik Xaritasi", "AI Akademik Tahlil", "PESTEL Strategiya", "IoT Sensorlar", "Tarixiy Dinamika", "AI Ekspert Chat"],
        "iot_local": "O'zbekiston Viloyatlari", "iot_global": "Dunyo Shaharlari", "hist_label": "Yilni tanlang:"
    },
    "EN": {
        "title": "Eco-System Global",
        "menu": ["Global AQI Map", "Carbon Footprint", "Heatmap Analysis", "AI Academic Analysis", "PESTEL Strategy", "IoT Sensors", "Historical Dynamics", "AI Expert Chat"],
        "iot_local": "Uzbekistan Regions", "iot_global": "World Cities", "hist_label": "Select Year:"
    },
    "RU": {
        "title": "Эко-Система Про",
        "menu": ["AQI Карта мира", "Углеродный след", "Тепловая карта", "AI Академический анализ", "PESTEL Стратегия", "IoT Сенсоры", "Историческая динамика", "AI Эксперт Чат"],
        "iot_local": "Регионы Узбекистана", "iot_global": "Города Мира", "hist_label": "Выберите год:"
    }
}

lang_code = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t = languages[lang_code]

# 3. SIDEBAR NAVIGATSIYA
with st.sidebar:
    st.title(f"🌱 {t['title']}")
    menu_choice = st.radio("Bo'lim:", t['menu'])
    st.markdown("---")
    st.caption("Mualliflar: Prof. Egamberdiyev E.A. | PhD Ataxo'jayev A.")

# --- 4. BO'LIMLAR MANTIQLARI ---

# GLOBAL AQI
if menu_choice == t['menu'][0]:
    st.header(t['menu'][0])
    st.components.v1.iframe("https://aqicn.org/map/world/", height=700)

# CARBON FOOTPRINT (ArcGIS)
elif menu_choice == t['menu'][1]:
    st.header(t['menu'][1])
    m = folium.Map(location=[41.31, 69.24], zoom_start=6)
    folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', 
                     attr='Esri, ArcGIS Imagery').add_to(m)
    HeatMap([[41.3, 69.2, 0.9], [42.4, 59.6, 1.0]], radius=30).add_to(m)
    folium_static(m, width=1100)

# ISSIQLIK XARITASI
elif menu_choice == t['menu'][2]:
    st.header(t['menu'][2])
    m2 = folium.Map(location=[41.31, 69.24], zoom_start=6)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google').add_to(m2)
    folium_static(m2, width=1100)

# AI TAHLIL & PESTEL (Umumiy AI funksiyasi)
elif menu_choice in [t['menu'][3], t['menu'][4]]:
    st.header(menu_choice)
    topic = st.text_input("Mavzu:", "Global Warming 2050")
    if st.button("Generate"):
        st.info("AI Analysis started... (Secrets'da API kalit bo'lishi shart)")

# IoT SENSORLAR (Yangilangan: 12 viloyat + 20 Global)
elif menu_choice == t['menu'][5]:
    st.header(t['menu'][5])
    
    # 1. O'zbekiston 12 viloyat
    st.subheader(f"📊 {t['iot_local']}")
    uzb_data = pd.DataFrame({
        'Viloyat': ['Toshkent', 'Samarqand', 'Buxoro', 'Andijon', 'Namangan', 'Fargona', 'Navoiy', 'Qashqadaryo', 'Surxondaryo', 'Jizzax', 'Sirdaryo', 'Xorazm'],
        'AQI': [115, 85, 95, 120, 110, 105, 90, 80, 130, 75, 70, 88]
    })
    st.plotly_chart(px.bar(uzb_data, x='Viloyat', y='AQI', color='AQI', template="plotly_dark"))

    # 2. Dunyo 20 shahri
    st.subheader(f"🌍 {t['iot_global']}")
    world_data = pd.DataFrame({
        'City': ['New York', 'London', 'Tokyo', 'Beijing', 'Cairo', 'Sydney', 'Paris', 'Dubai', 'Moscow', 'Delhi', 'Rio', 'Seoul', 'Berlin', 'Toronto', 'Lagos', 'Istanbul', 'Jakarta', 'Mexico City', 'Rome', 'Bangkok'],
        'AQI': [45, 52, 60, 155, 140, 30, 48, 110, 65, 210, 55, 80, 42, 35, 160, 95, 145, 130, 50, 125]
    })
    st.plotly_chart(px.bar(world_data, x='City', y='AQI', color='AQI', template="plotly_white"))

# TARIXIY DINAMIKA (Tuzatilgan rasm havolasi bilan)
elif menu_choice == t['menu'][6]:
    st.header(t['menu'][6])
    year = st.select_slider(t['hist_label'], options=[2000, 2010, 2015, 2020, 2025])
    # Orol dengizi dinamikasi uchun rasm
    url = "https://upload.wikimedia.org/wikipedia/commons/e/e0/Aral_Sea_1989-2014.jpg"
    st.image(url, caption=f"Aral Sea Dynamics - Observation Year: {year}", use_container_width=True)
    st.info("Ushbu bo'limda sun'iy yo'ldosh arxiv ma'lumotlari vizualizatsiya qilinadi.")

# AI CHAT
elif menu_choice == t['menu'][7]:
    st.header(t['menu'][7])
    st.write("Ekspert AI bilan jonli muloqot bo'limi.")
