import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static

# 1. SAHIFA KONFIGURATSIYASI
st.set_page_config(page_title="Eco-Portal Pro AI", layout="wide")

# 2. DINAMIK TIL TIZIMI
languages = {
    "UZ": {
        "title": "Eco-System Pro",
        "menu": ["Global AQI Map", "Carbon Footprint", "Issiqlik Xaritasi", "AI Akademik Tahlil", "PESTEL Strategiya", "IoT Sensorlar", "Tarixiy Dinamika", "AI Ekspert Chat"],
        "btn": "Tahlil qilish", "loading": "AI tahlil qilmoqda, kuting...", "error": "API kalit topilmadi!"
    },
    "EN": {
        "title": "Eco-System Global",
        "menu": ["Global AQI Map", "Carbon Footprint", "Heatmap Analysis", "AI Academic Analysis", "PESTEL Strategy", "IoT Sensors", "Historical Dynamics", "AI Expert Chat"],
        "btn": "Run Analysis", "loading": "AI is analyzing, please wait...", "error": "API Key not found!"
    },
    "RU": {
        "title": "Эко-Система Про",
        "menu": ["AQI Карта мира", "Углеродный след", "Тепловая карта", "AI Академический анализ", "PESTEL Стратегия", "IoT Сенсоры", "Историческая динамика", "AI Эксперт Чат"],
        "btn": "Запустить анализ", "loading": "AI анализирует, подождите...", "error": "API ключ не найден!"
    }
}

lang_code = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t = languages[lang_code]

# 3. AI FUNKSIYASI (Tuzatilgan va optimallashtirilgan)
def get_ai_response(prompt, system_role):
    if "GROQ_API_KEY" not in st.secrets:
        return t["error"]
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"

# 4. SIDEBAR
with st.sidebar:
    st.title(f"🌱 {t['title']}")
    menu_choice = st.radio("Bo'limlar:", t['menu'])
    st.markdown("---")
    st.caption("Muallif: Prof. Egamberdiyev E.A.")

# --- BO'LIMLAR MANTIQLARI ---

# AQI Map & Xaritalar (Xatolarsiz)
if menu_choice == t['menu'][0]:
    st.components.v1.iframe("https://aqicn.org/map/world/", height=750)

elif menu_choice in [t['menu'][1], t['menu'][2]]:
    st.header(menu_choice)
    m = folium.Map(location=[41.31, 69.24], zoom_start=6)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', 
                     attr='Google', name='Satellite').add_to(m)
    folium_static(m, width=1100)

# AI AKADEMIK TAHLIL (4-bo'lim)
elif menu_choice == t['menu'][3]:
    st.header(t['menu'][3])
    topic = st.text_input("Mavzu (Topic):", "Ecological problems in Aral Sea region")
    if st.button(t['btn']):
        with st.spinner(t['loading']):
            role = f"Sen PhD darajasidagi ekologsan. Berilgan mavzuni {lang_code} tilida akademik va ilmiy tilda tahlil qilib ber."
            result = get_ai_response(topic, role)
            st.markdown("### 📄 AI Academic Result:")
            st.write(result)

# PESTEL STRATEGIYA (5-bo'lim)
elif menu_choice == t['menu'][4]:
    st.header(t['menu'][4])
    project = st.text_input("Loyiha yoki Hudud:", "Uzbekistan Green Energy 2030")
    if st.button(t['btn']):
        with st.spinner(t['loading']):
            role = f"Sen strategik tahlilchisan. Berilgan loyihani {lang_code} tilida PESTEL (Political, Economic, Social, Technological, Environmental, Legal) tahlilini jadval ko'rinishida yozib ber."
            result = get_ai_response(project, role)
            st.markdown("### 🧠 PESTEL Strategy Analysis:")
            st.write(result)

# IoT, Tarix va Chat (Qisqartirilgan mantiq)
elif menu_choice == t['menu'][5]:
    st.header(t['menu'][5])
    uz_data = pd.DataFrame({'Hudud': ['Toshkent', 'Nukus', 'Andijon'], 'AQI': [115, 190, 75]})
    st.plotly_chart(px.bar(uz_data, x='Hudud', y='AQI', color='AQI'))

elif menu_choice == t['menu'][6]:
    st.header(t['menu'][6])
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aral_Sea_1989-2014.jpg", use_container_width=True)

elif menu_choice == t['menu'][7]:
    st.header(t['menu'][7])
    if 'chat_history' not in st.session_state: st.session_state.chat_history = []
    u_input = st.chat_input("Savol...")
    if u_input:
        ans = get_ai_response(u_input, "Ekspert maslahatchi.")
        st.session_state.chat_history.append((u_input, ans))
    for q, a in st.session_state.chat_history:
        st.chat_message("user").write(q)
        st.chat_message("assistant").write(a)
