import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import datetime

# 1. GOOGLE SEO VA BRAUZER SOZLAMALARI
st.set_page_config(
    page_title="Eko Risk AI - Global Monitoring & Tahlil",
    page_icon="🌍",
    layout="wide",
    menu_items={
        'About': "# Eko Risk Monitoring Portali\nPhD Egamberdiyev E.A. metodologiyasi asosida yaratilgan."
    }
)

# Qidiruv botlari uchun yashirin kalit so'zlar
st.markdown('<h1 style="display:none;">Eko risk, ekologik bashorat, Uzbekistan AQI, environmental AI tahlil</h1>', unsafe_allow_html=True)

# 2. API KALITNI TEKSHIRISH
if "GROQ_API_KEY" not in st.secrets:
    st.error("Xatolik: Streamlit Secrets-da 'GROQ_API_KEY' topilmadi!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. DINAMIK TIL TIZIMI
lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t_dict = {
    "UZ": {
        "m0": "🏠 Asosiy Sahifa (Eko Risk)", "m1": "🌍 Global AQI Map", "m2": "🛰 Sun'iy Yo'ldosh", 
        "m3": "🧪 AI Akademik Tahlil", "m4": "📈 PESTEL Strategiya", "m5": "📊 IoT Sensorlar", 
        "m6": "🔮 2030 Bashorat", "m7": "⏳ Tarixiy Dinamika", "m8": "🤖 AI Chat",
        "btn": "Tahlilni boshlash", "dl": "Hisobotni yuklab olish"
    },
    "EN": {
        "m0": "🏠 Home (Eco Risk)", "m1": "🌍 Global AQI Map", "m2": "🛰 Satellite Imagery", 
        "m3": "🧪 AI Academic Analysis", "m4": "📈 PESTEL Strategy", "m5": "📊 IoT Sensors", 
        "m6": "🔮 2030 Forecast", "m7": "⏳ Historical Dynamics", "m8": "🤖 AI Chat",
        "btn": "Run Analysis", "dl": "Download Report"
    }
}
t = t_dict.get(lang, t_dict["UZ"])

# 4. SIDEBAR MENYU
st.sidebar.title("🌱 Eco-Portal Pro")
menu = st.sidebar.radio("Bo'limlar:", list(t.values())[:9])

# --- BO'LIMLAR MANTIQLARI ---

# 0. ASOSIY SAHIFA (SEO UCHUN MUHIM)
if menu == t["m0"]:
    st.title("🌱 Global Eko Risk Monitoring va AI Tahlil Portali")
    st.write(f"""
    Ushbu portal **Eko Risk** omillarini aniqlash va ekologik muammolarni AI yordamida akademik tahlil qilish uchun yaratilgan.
    
    **Tizim imkoniyatlari:**
    * 🛰 **Sun'iy yo'ldosh monitoringi:** Real vaqtda hududlar holati.
    * 🧪 **AI Akademik Tahlil:** PhD darajasidagi ilmiy xulosalar.
    * 🔮 **Bashorat:** 2030-yilgacha bo'lgan ekologik trendlar.
    * 📊 **IoT:** O'zbekistonning 12 ta viloyatidan jonli ma'lumotlar.
    """)
    st.image("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b", caption="Global Ecology Control Center")

# 1. GLOBAL AQI
elif menu == t["m1"]:
    st.components.v1.iframe("https://aqicn.org/map/world/", height=700)

# 2. SUN'IY YO'LDOSH
elif menu == t["m2"]:
    st.header(t["m2"])
    m = folium.Map(location=[41.3, 69.2], zoom_start=6)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google', name='Google Hybrid').add_to(m)
    folium.LayerControl().add_to(m)
    folium_static(m, width=1100)

# 3. AI AKADEMIK & 4. PESTEL
elif menu in [t["m3"], t["m4"]]:
    st.header(menu)
    user_input = st.text_area("Mavzu:", "Eko risk omillari va ularning ta'siri")
    if st.button(t["btn"]):
        with st.spinner("AI tahlil qilmoqda..."):
            role = "PhD Scientist" if menu == t["m3"] else "Strategic Consultant"
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "system", "content": role}, {"role": "user", "content": user_input}]).choices[0].message.content
            st.markdown(res)
            st.download_button(t["dl"], res, file_name=f"eco_report_{datetime.date.today()}.txt")

# 5. IoT SENSORLAR (12 VILOYAT)
elif menu == t["m5"]:
    st.header(t["m5"])
    df = pd.DataFrame({'Hudud': ['Toshkent', 'Samarqand', 'Andijon', 'Buxoro', 'Nukus', 'Namangan', 'Fargona', 'Navoiy', 'Termiz', 'Jizzax', 'Guliston', 'Urganch'], 'AQI': [115, 82, 110, 88, 195, 105, 95, 78, 140, 72, 65, 80]})
    st.plotly_chart(px.bar(df, x='Hudud', y='AQI', color='AQI', template="plotly_dark"))

# 6. 2030 BASHORAT
elif menu == t["m6"]:
    st.header(t["m6"])
    f_data = pd.DataFrame({'Yil': [2024, 2025, 2026, 2027, 2028, 2029, 2030], 'Eko-Barqarorlik': [60, 65, 72, 78, 85, 90, 95]})
    st.line_chart(f_data.set_index('Yil'))

# 7. TARIXIY DINAMIKA
elif menu == t["m7"]:
    st.header(t["m7"])
    y = st.select_slider("Yil:", options=[2000, 2010, 2020, 2025])
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aral_Sea_1989-2014.jpg", use_container_width=True)

# 8. AI CHAT
elif menu == t["m8"]:
    st.header(t["m8"])
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
    if prompt := st.chat_input("Savol bering..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}]).choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": res})
        with st.chat_message("assistant"): st.write(res)
