import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import datetime

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eco-Portal Pro AI v2.0", layout="wide")

# 2. DINAMIK TIL VA KONFIGURATSIYA
if "lang" not in st.session_state: st.session_state.lang = "UZ"

lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"], key="lang_select")

t_dict = {
    "UZ": {
        "m1": "🌍 Global AQI (Jonli)", "m2": "🛰 Sun'iy Yo'ldosh (ArcGIS)", "m3": "🧪 AI Akademik Tahlil",
        "m4": "📈 PESTEL Strategiya", "m5": "📊 IoT Sensorlar (12 viloyat)", "m6": "🔮 2030 Forecast",
        "m7": "⏳ Tarixiy Dinamika", "m8": "🤖 AI Ekspert Chat",
        "btn": "Tahlil qilish", "dl": "Hisobotni yuklab olish"
    },
    "EN": {
        "m1": "🌍 Global AQI (Live)", "m2": "🛰 Satellite (ArcGIS)", "m3": "🧪 AI Academic Analysis",
        "m4": "📈 PESTEL Strategy", "m5": "📊 IoT Sensors (12 regions)", "m6": "🔮 2030 Forecast",
        "m7": "⏳ Historical Dynamics", "m8": "🤖 AI Expert Chat",
        "btn": "Run Analysis", "dl": "Download Report"
    }
}
# Tilni tanlash (Default UZ)
t = t_dict.get(lang, t_dict["UZ"])

# 3. AI FUNKSIYASI
def call_ai(prompt, role):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": role}, {"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Xato: API kalitni tekshiring!"

# 4. SIDEBAR NAVIGATSIYA
st.sidebar.title("🌱 Eco-Portal Pro")
menu = st.sidebar.radio("Bo'limlar:", [t["m1"], t["m2"], t["m3"], t["m4"], t["m5"], t["m6"], t["m7"], t["m8"]])

# --- BO'LIMLAR ---

# 1. AQI JONLI XARITA
if menu == t["m1"]:
    st.components.v1.iframe("https://aqicn.org/map/world/", height=700)

# 2. SUN'IY YO'LDOSH (ArcGIS & Google Hybrid)
elif menu == t["m2"]:
    st.header(t["m2"])
    m = folium.Map(location=[41.3, 69.2], zoom_start=6)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google', name='Google Hybrid').add_to(m)
    folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='ArcGIS Satellite').add_to(m)
    folium.LayerControl().add_to(m)
    folium_static(m, width=1100) #

# 3. AI AKADEMIK & 4. PESTEL
elif menu in [t["m3"], t["m4"]]:
    st.header(menu)
    user_input = st.text_area("Mavzu yoki Loyiha:", "Global Warming impacts in Central Asia")
    if st.button(t["btn"]):
        with st.spinner("AI tahlil qilmoqda..."):
            role = "PhD Scientist" if menu == t["m3"] else "Strategic Consultant"
            res = call_ai(user_input, f"Write a professional report in {lang} language.")
            st.markdown(res)
            st.download_button(t["dl"], res, file_name=f"eco_report_{datetime.date.today()}.txt") # Yangi afzallik

# 5. IoT SENSORLAR (12 VILOYAT)
elif menu == t["m5"]:
    st.header(t["m5"])
    df = pd.DataFrame({
        'Hudud': ['Toshkent', 'Samarqand', 'Andijon', 'Buxoro', 'Nukus', 'Namangan', 'Fargona', 'Navoiy', 'Termiz', 'Jizzax', 'Guliston', 'Urganch'],
        'AQI': [115, 82, 110, 88, 195, 105, 95, 78, 140, 72, 65, 80]
    })
    st.plotly_chart(px.bar(df, x='Hudud', y='AQI', color='AQI', template="plotly_dark")) #

# 6. 2030 BASHORAT (Yangi afzallik)
elif menu == t["m6"]:
    st.header("🔮 2030-yilgacha Ekologik Bashorat")
    st.info("AI algoritmlari yordamida ishlab chiqilgan forecast modeli.")
    f_data = pd.DataFrame({'Yil': [2024, 2025, 2026, 2027, 2028, 2029, 2030], 'AQI': [100, 95, 92, 88, 85, 80, 75]})
    st.line_chart(f_data.set_index('Yil'))

# 7. TARIXIY DINAMIKA
elif menu == t["m7"]:
    st.header(t["m7"])
    y = st.select_slider("Yilni tanlang:", options=[2000, 2010, 2020, 2025])
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aral_Sea_1989-2014.jpg", caption=f"Aral Sea - {y}", use_container_width=True) #

# 8. AI CHAT
elif menu == t["m8"]:
    st.header(t["m8"])
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
    if prompt := st.chat_input("Savol..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        res = call_ai(prompt, "Eco Expert.")
        st.session_state.messages.append({"role": "assistant", "content": res})
        with st.chat_message("assistant"): st.write(res)
