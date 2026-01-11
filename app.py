import streamlit as st
from groq import Groq
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eco-Portal Global", layout="wide")

# 2. TIL LUG'ATI (TO'LIQ DINAMIK)
lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t_dict = {
    "UZ": {
        "menu": ["AQI Xaritasi", "Carbon Tahlil", "Issiqlik Xaritasi", "AI Akademik", "PESTEL Strategiya", "IoT Sensorlar", "Tarixiy Dinamika", "AI Chat"],
        "iot_uz": "O'zbekistonning 12 ta viloyati", "iot_gl": "Global 20 ta shahar", "year": "Yil:", "btn": "Tahlil"
    },
    "EN": {
        "menu": ["AQI Map", "Carbon Analysis", "Heatmap", "AI Academic", "PESTEL Strategy", "IoT Sensors", "Historical Dynamics", "AI Chat"],
        "iot_uz": "12 Regions of Uzbekistan", "iot_gl": "Global 20 Cities", "year": "Year:", "btn": "Analyze"
    },
    "RU": {
        "menu": ["AQI Карта", "Carbon Анализ", "Тепловая карта", "AI Академик", "PESTEL Стратегия", "IoT Сенсоры", "История", "AI Чат"],
        "iot_uz": "12 областей Узбекистана", "iot_gl": "20 городов мира", "year": "Год:", "btn": "Анализ"
    }
}
t = t_dict[lang]

# 3. SIDEBAR NAVIGATSIYA
with st.sidebar:
    st.title("🌱 Eco Dashboard")
    menu = st.radio("Bo'limni tanlang:", t["menu"])
    st.markdown("---")
    st.caption("Mualliflar: Prof. Egamberdiyev E.A. | PhD Ataxo'jayev A.")

# AI Funksiyasi
def call_ai(prompt, role):
    if "GROQ_API_KEY" not in st.secrets: return "API Key topilmadi!"
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": role}, {"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e: return f"Xato: {e}"

# --- BO'LIMLAR ---

# 1. AQI MAP
if menu == t["menu"][0]:
    st.components.v1.iframe("https://aqicn.org/map/world/", height=700)

# 2. CARBON & 3. ISSIQLIK XARITASI (Xatolarsiz)
elif menu in [t["menu"][1], t["menu"][2]]:
    st.header(menu)
    m = folium.Map(location=[41.31, 69.24], zoom_start=6)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', 
                     attr='Google Satellite', name='Google').add_to(m)
    HeatMap([[41.3, 69.2, 0.9], [40.7, 72.3, 0.8]], radius=25).add_to(m)
    folium_static(m, width=1100)

# 4. AI AKADEMIK & 5. PESTEL
elif menu in [t["menu"][3], t["menu"][4]]:
    st.header(menu)
    user_in = st.text_input("Mavzu:", "Climate Action 2030")
    if st.button(t["btn"]):
        with st.spinner("AI tahlil qilmoqda..."):
            res = call_ai(user_in, f"Sen PhD darajasidagi ekspert ekologsan. {lang} tilida tahlil yoz.")
            st.markdown(res)

# 6. IoT SENSORLAR (12 Viloyat + 20 Global)
elif menu == t["menu"][5]:
    st.header(menu)
    st.subheader(t["iot_uz"])
    uz_df = pd.DataFrame({'Hudud': ['Toshkent', 'Samarqand', 'Andijon', 'Buxoro', 'Nukus', 'Namangan', 'Fargona', 'Navoiy', 'Termiz', 'Jizzax', 'Guliston', 'Urganch'], 'AQI': [115, 82, 110, 88, 195, 105, 95, 78, 140, 72, 65, 80]})
    st.bar_chart(uz_df.set_index('Hudud'))
    st.subheader(t["iot_gl"])
    gl_df = pd.DataFrame({'City': ['New York', 'London', 'Tokyo', 'Beijing', 'Cairo', 'Sydney', 'Paris', 'Dubai', 'Moscow', 'Delhi', 'Rio', 'Seoul', 'Berlin', 'Toronto', 'Lagos', 'Istanbul', 'Jakarta', 'Mexico City', 'Rome', 'Bangkok'], 'AQI': [42, 55, 62, 145, 130, 28, 45, 115, 60, 220, 52, 78, 40, 32, 165, 92, 150, 125, 48, 135]})
    st.bar_chart(gl_df.set_index('City'))

# 7. TARIXIY DINAMIKA
elif menu == t["menu"][6]:
    st.header(menu)
    year = st.select_slider(t["year"], options=[2000, 2010, 2020, 2025])
    img_url = "https://upload.wikimedia.org/wikipedia/commons/e/e0/Aral_Sea_1989-2014.jpg"
    st.image(img_url, caption=f"Aral Sea - {year}", use_container_width=True)

# 8. AI CHAT
elif menu == t["menu"][7]:
    st.header(menu)
    if 'msgs' not in st.session_state: st.session_state.msgs = []
    if prompt := st.chat_input("Savol yozing..."):
        st.session_state.msgs.append({"role": "user", "content": prompt})
        ans = call_ai(prompt, "Expert maslahatchi.")
        st.session_state.msgs.append({"role": "assistant", "content": ans})
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]): st.write(m["content"])
