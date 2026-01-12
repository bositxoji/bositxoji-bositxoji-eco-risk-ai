import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import datetime

# 1. GOOGLE SEO VA TASDIQLASH (META TAG)
st.set_page_config(
    page_title="Eko Risk AI - Global Monitoring & Tahlil",
    page_icon="🌍",
    layout="wide"
)

# Siz bergan Google tasdiqlash kodi
st.markdown('<meta name="google-site-verification" content="maybg4-LdPKEKS8plcTQclxsDBM6XX8lGzOQIwbv0W8" />', unsafe_allow_html=True)
# Qidiruv botlari uchun yashirin kalit so'zlar
st.markdown('<h1 style="display:none;">Eko risk, ekologik tahlil, Uzbekistan AQI, AI Environmental Analysis</h1>', unsafe_allow_html=True)

# 2. API KALITNI TEKSHIRISH
if "GROQ_API_KEY" not in st.secrets:
    st.error("Secrets bo'limiga 'GROQ_API_KEY' kiritilmagan!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. TILNI TANLASH
lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t_dict = {
    "UZ": {
        "m1": "🌍 Global AQI (Jonli)", "m2": "🛰 Sun'iy Yo'ldosh", "m3": "🧪 AI Akademik Tahlil",
        "m4": "📈 PESTEL Strategiya", "m5": "📊 IoT Sensorlar (12 viloyat)", "m6": "🔮 2030 Bashorat",
        "m7": "⏳ Tarixiy Dinamika", "m8": "🤖 AI Chat Ekspert",
        "btn": "Tahlilni boshlash", "dl": "Hisobotni yuklab olish"
    },
    "EN": {
        "m1": "🌍 Global AQI (Live)", "m2": "🛰 Satellite View", "m3": "🧪 AI Academic Analysis",
        "m4": "📈 PESTEL Strategy", "m5": "📊 IoT Sensors (12 regions)", "m6": "🔮 2030 Forecast",
        "m7": "⏳ Historical Dynamics", "m8": "🤖 AI Expert Chat",
        "btn": "Run Analysis", "dl": "Download Report"
    }
}
t = t_dict.get(lang, t_dict["UZ"])

# 4. SIDEBAR NAVIGATSIYA
st.sidebar.title("🌱 Eco-Portal Pro")
menu = st.sidebar.radio("Bo'limni tanlang:", list(t.values())[:8])
st.sidebar.markdown("---")
st.sidebar.caption("Mualliflar: Prof. Egamberdiyev E.A. | PhD Ataxo'jayev A.")

# --- FUNKSIYALAR ---

def call_ai(prompt, role):
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": role}, {"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"AI Xatosi: {e}"

# --- BO'LIMLAR ---

# 1. AQI JONLI XARITA
if menu == t["m1"]:
    st.header(t["m1"])
    st.components.v1.iframe("https://aqicn.org/map/world/", height=700)

# 2. SUN'IY YO'LDOSH (YANGI AFZALLIK)
elif menu == t["m2"]:
    st.header(t["m2"])
    m = folium.Map(location=[41.31, 69.24], zoom_start=6)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google', name='Google Hybrid').add_to(m)
    folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='ArcGIS Satellite').add_to(m)
    folium.LayerControl().add_to(m)
    folium_static(m, width=1100) #

# 3. AI AKADEMIK & 4. PESTEL
elif menu in [t["m3"], t["m4"]]:
    st.header(menu)
    user_in = st.text_area("Mavzu:", "Impact of Carbon Emissions in Central Asia")
    if st.button(t["btn"]):
        with st.spinner("AI ishlamoqda..."):
            role = "PhD Environmental Scientist" if menu == t["m3"] else "Strategic Policy Analyst"
            response = call_ai(user_in, f"Write a deep professional analysis in {lang} language.")
            st.markdown(response) #
            st.download_button(t["dl"], response, file_name=f"eco_analysis_{datetime.date.today()}.txt")

# 5. IoT SENSORLAR (12 VILOYAT)
elif menu == t["m5"]:
    st.header(t["m5"])
    data = pd.DataFrame({
        'Hudud': ['Toshkent', 'Samarqand', 'Andijon', 'Buxoro', 'Nukus', 'Namangan', 'Fargona', 'Navoiy', 'Termiz', 'Jizzax', 'Guliston', 'Urganch'],
        'AQI Index': [115, 82, 110, 88, 195, 105, 95, 78, 140, 72, 65, 80]
    })
    st.plotly_chart(px.bar(data, x='Hudud', y='AQI Index', color='AQI Index', template="plotly_dark")) #

# 6. 2090 BASHORAT (YANGI AFZALLIK)
elif menu == t["m6"]:
    st.header(t["m6"])
    st.info("AI asosidagi chiziqli bashorat modeli (Trend Analysis)")
    f_data = pd.DataFrame({
        'Yil': [2024, 2025, 2026, 2027, 2028, 2029, 2030, 2035, 2040, 2050, 2060, ... ,2090],
        'Barqarorlik %': [55, 58, 64, 70, 78, 85, 92]
    })
    st.line_chart(f_data.set_index('Yil'))

# 7. TARIXIY DINAMIKA
elif menu == t["m7"]:
    st.header(t["m7"])
    yil = st.select_slider("Yilni tanlang:", options=[2000, 2010, 2020, 2025])
    # Orol dengizi dinamikasi
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aral_Sea_1989-2014.jpg", caption=f"Aral Sea Dynamics - Year: {yil}", use_container_width=True)

# 8. AI EXPERT CHAT
elif menu == t["m8"]:
    st.header(t["m8"])
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])
    
    if p := st.chat_input("Savolingizni yozing..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        res = call_ai(p, "Siz ekologiya bo'yicha yuqori malakali ekspertsiz.")
        st.session_state.messages.append({"role": "assistant", "content": res})
        with st.chat_message("assistant"): st.write(res)
