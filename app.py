import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static

# SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eco-System Global AI", layout="wide")

# TIL VA MATNLAR
lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t_dict = {
    "UZ": {
        "menu": ["AQI Xaritasi", "Carbon Footprint", "Issiqlik Xaritasi", "AI Akademik Tahlil", "PESTEL Strategiya", "IoT Sensorlar", "Tarixiy Dinamika", "AI Ekspert Chat"],
        "btn": "Tahlilni boshlash", "load": "AI tahlil qilmoqda...", "iot_uz": "O'zbekiston viloyatlari"
    },
    "EN": {
        "menu": ["AQI Map", "Carbon Footprint", "Heatmap Analysis", "AI Academic Analysis", "PESTEL Strategy", "IoT Sensors", "Historical Dynamics", "AI Expert Chat"],
        "btn": "Run Analysis", "load": "AI is analyzing...", "iot_uz": "Uzbekistan Regions"
    },
    "RU": {
        "menu": ["AQI Карта", "Углеродный след", "Тепловая карта", "AI Академический анализ", "PESTEL Стратегия", "IoT Сенсоры", "История", "AI Чат"],
        "btn": "Запустить анализ", "load": "AI анализирует...", "iot_uz": "Регионы Узбекистана"
    }
}
t = t_dict[lang]

# AI FUNKSIYASI (Secrets orqali ishlaydi)
def call_ai(prompt, system_role):
    if "GROQ_API_KEY" not in st.secrets:
        return "Xatolik: Secrets bo'limiga GROQ_API_KEY kiritilmagan!"
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_role}, {"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"AI xatosi: {e}"

# SIDEBAR NAVIGATSIYA
with st.sidebar:
    st.title("🌱 Eco-System Pro")
    menu = st.radio("Bo'limni tanlang:", t["menu"])
    st.markdown("---")
    st.caption("Mualliflar: Prof. Egamberdiyev E.A. | PhD Ataxo'jayev A.")

# --- BO'LIMLAR ---

# 1. AQI Map
if menu == t["menu"][0]:
    st.components.v1.iframe("https://aqicn.org/map/world/", height=700)

# 2. Carbon & 3. Heatmap (Xaritalar)
elif menu in [t["menu"][1], t["menu"][2]]:
    st.header(menu)
    m = folium.Map(location=[41.31, 69.24], zoom_start=6)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', 
                     attr='Google Satellite', name='Google').add_to(m)
    HeatMap([[41.3, 69.2, 0.9], [40.7, 72.3, 0.8], [42.4, 59.6, 0.7]], radius=30).add_to(m)
    folium_static(m, width=1100)

# 4. AI AKADEMIK TAHLIL
elif menu == t["menu"][3]:
    st.header(t["menu"][3])
    topic = st.text_input("Ilmiy mavzu:", "Impact of Climate Change on Uzbekistan's Water Resources")
    if st.button(t["btn"]):
        with st.spinner(t["load"]):
            res = call_ai(topic, f"Sen PhD ekologsan. {lang} tilida ilmiy-akademik tahlil yoz.")
            st.markdown(res)

# 5. PESTEL STRATEGIYA
elif menu == t["menu"][4]:
    st.header(t["menu"][4])
    project = st.text_input("Loyiha:", "Green Economy Roadmap 2030")
    if st.button(t["btn"]):
        with st.spinner(t["load"]):
            res = call_ai(project, f"Sen strategik tahlilchisan. {lang} tilida PESTEL tahlilini jadvalda ko'rsat.")
            st.markdown(res)

# 6. IoT SENSORLAR (12 ta viloyat)
elif menu == t["menu"][5]:
    st.header(t["menu"][5])
    st.subheader(t["iot_uz"])
    data = pd.DataFrame({
        'Hudud': ['Toshkent', 'Samarqand', 'Andijon', 'Buxoro', 'Nukus', 'Namangan', 'Fargona', 'Navoiy', 'Termiz', 'Jizzax', 'Guliston', 'Urganch'],
        'AQI': [115, 82, 110, 88, 195, 105, 95, 78, 140, 72, 65, 80]
    })
    st.plotly_chart(px.bar(data, x='Hudud', y='AQI', color='AQI', template="plotly_dark"))

# 7. TARIXIY DINAMIKA
elif menu == t["menu"][6]:
    st.header(menu)
    year = st.select_slider("Yil:", options=[2000, 2010, 2020, 2025])
    img = "https://upload.wikimedia.org/wikipedia/commons/e/e0/Aral_Sea_1989-2014.jpg"
    st.image(img, caption=f"Aral Sea - {year}-yil holati", use_container_width=True)

# 8. AI CHAT
elif menu == t["menu"][7]:
    st.header(t["menu"][7])
    if 'chat' not in st.session_state: st.session_state.chat = []
    if p := st.chat_input("Savol bering..."):
        st.session_state.chat.append(("user", p))
        st.session_state.chat.append(("assistant", call_ai(p, "Expert advisor.")))
    for role, text in st.session_state.chat:
        with st.chat_message(role): st.write(text)
