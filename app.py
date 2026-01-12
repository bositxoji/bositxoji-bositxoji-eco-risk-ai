import streamlit as st
from groq import Groq
import pandas as pd
import folium
from streamlit_folium import folium_static

# Sahifa sozlamalari
st.set_page_config(page_title="Eco-Portal Pro AI", layout="wide")

# Til tanlash
lang = st.sidebar.selectbox("🌐 Til", ["UZ", "EN", "RU"])
t_menu = {
    "UZ": ["Global AQI", "Carbon Footprint", "Issiqlik Xaritasi", "AI Akademik", "PESTEL Strategiya", "IoT Sensorlar", "Tarixiy Dinamika", "AI Chat"],
    "EN": ["Global AQI", "Carbon Footprint", "Heatmap", "AI Academic", "PESTEL Strategy", "IoT Sensors", "History", "AI Chat"],
    "RU": ["AQI Карта", "Carbon Footprint", "Тепловая карта", "AI Академик", "PESTEL Стратегия", "IoT Сенсоры", "История", "AI Чат"]
}
choice = st.sidebar.radio("Bo'limlar:", t_menu[lang])

# AI Funksiyasi
def ask_ai(prompt, role):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": role}, {"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"AI bilan bog'lanishda xato: {e}. Secrets bo'limini tekshiring."

# --- Bo'limlar Mantiqi ---

if choice == t_menu[lang][0]: # AQI Map
    st.components.v1.iframe("https://aqicn.org/map/world/", height=700)

elif choice in [t_menu[lang][1], t_menu[lang][2]]: # Maps
    m = folium.Map(location=[41.3, 69.2], zoom_start=6)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google').add_to(m)
    folium_static(m, width=1100)

elif choice == t_menu[lang][3]: # AI Akademik
    st.header("🔬 AI Akademik Tahlil")
    mavzu = st.text_input("Mavzu:", "Orol dengizi muammosi")
    if st.button("Tahlil"):
        with st.spinner("Tahlil ketmoqda..."):
            st.write(ask_ai(mavzu, "PhD ekolog kabi akademik tahlil yoz."))

elif choice == t_menu[lang][4]: # PESTEL
    st.header("🧠 PESTEL Strategiya")
    loyiha = st.text_input("Loyiha:", "Yashil Energiya 2030")
    if st.button("Generatsiya"):
        with st.spinner("Strategiya tuzilmoqda..."):
            st.write(ask_ai(loyiha, "Strategik tahlilchi kabi PESTEL jadvalini yoz."))

elif choice == t_menu[lang][5]: # IoT
    st.header("📊 IoT Sensorlar (12 viloyat)")
    df = pd.DataFrame({'Hudud': ['Toshkent', 'Nukus', 'Samarqand', 'Andijon', 'Buxoro', 'Namangan', 'Fargona', 'Navoiy', 'Termiz', 'Jizzax', 'Guliston', 'Urganch'], 
                       'AQI': [110, 195, 85, 105, 90, 100, 95, 80, 145, 75, 70, 85]})
    st.bar_chart(df.set_index('Hudud'))

elif choice == t_menu[lang][6]: # History
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aral_Sea_1989-2014.jpg", use_container_width=True)

elif choice == t_menu[lang][7]: # Chat
    prompt = st.chat_input("Savol...")
    if prompt: st.write(ask_ai(prompt, "Ekolog-maslahatchi."))
