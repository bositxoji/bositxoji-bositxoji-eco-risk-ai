import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import json

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Portal Global AI", layout="wide")

# Til sozlamalari
lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t_dict = {
    "UZ": {
        "m1": "🌡 Global Havo Sifati", 
        "m2": "🛰 Sun'iy Yo'ldosh (Heatmap)", 
        "m3": "🤖 AI Risk & Akademik Tahlil", 
        "m4": "🧠 PESTEL & Strategiya", 
        "m5": "📶 IoT Sensorlar",
        "btn": "Tahlilni boshlash"
    },
    "EN": {
        "m1": "🌡 Global Air Quality", 
        "m2": "🛰 Satellite (Heatmap)", 
        "m3": "🤖 AI Risk & Academic", 
        "m4": "🧠 PESTEL & Strategy", 
        "m5": "📶 IoT Sensors",
        "btn": "Start Analysis"
    }
}
# Til lug'atini tekshirish
t = t_dict.get(lang, t_dict["UZ"])

# 2. STRATEGIK AI FUNKSIYASI (Secrets orqali xavfsiz)
def get_ai_response(prompt, system_role):
    try:
        # Kalitlarni kodda yozmang! Streamlit Secrets-dan foydalaning
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Xatolik: API kalit topilmadi yoki xato."

# 3. SIDEBAR NAVIGATSIYA
with st.sidebar:
    st.title("🚀 Eko-Portal Pro")
    menu = st.radio("Bo'limni tanlang:", [t['m1'], t['m2'], t['m3'], t['m4'], t['m5']])
    st.markdown("---")
    st.write("🎓 **Mualliflar:**")
    st.caption("Prof. Egamberdiyev E.A. | PhD Ataxo'jayev A.")

# --- 1-BO'LIM: GLOBAL HAVO SIFATI ---
if menu == t['m1']:
    st.header(t['m1'])
    st.components.v1.iframe("https://aqicn.org/map/world/", height=700)

# --- 2-BO'LIM: ISSIQLIK XARITASI (Tuzatilgan) ---
elif menu == t['m2']:
    st.header(t['m2'])
    m = folium.Map(location=[41.31, 69.24], zoom_start=6)
    # Attribution (attr) qo'shish orqali ValueError tuzatildi
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', 
        attr='Google Satellite Imagery', 
        name='Satellite'
    ).add_to(m)
    
    heat_data = [[41.31, 69.24, 0.9], [42.46, 59.61, 1.0], [37.22, 67.27, 0.8]]
    HeatMap(heat_data, radius=20, blur=15).add_to(m)
    folium_static(m, width=1100, height=600)

# --- 3-BO'LIM: AI RISK TAHLILI ---
elif menu == t['m3']:
    st.header(t['m3'])
    topic = st.text_area("Tahlil uchun mavzu yoki ma'lumot kiriting:")
    if st.button(t['btn']):
        with st.spinner("AI akademik tahlil tayyorlamoqda..."):
            res = get_ai_response(topic, f"Sen PhD ekologsan. {lang} tilida akademik iqtiboslar bilan tahlil yoz.")
            st.markdown(res)

# --- 4-BO'LIM: PESTEL STRATEGIYA ---
elif menu == t['m4']:
    st.header(t['m4'])
    p_topic = st.text_input("Strategik mavzu:", "Orolbo'yi 2030")
    if st.button("Strategik tahlil"):
        with st.spinner("PESTEL tahlil qilinmoqda..."):
            res = get_ai_response(f"{p_topic} uchun PESTEL tahlil va 3 ssenariy yoz.", "Sen strategik tahlilchisan.")
            st.markdown(res)

# --- 5-BO'LIM: IoT SENSORLAR ---
elif menu == t['m5']:
    st.header(t['m5'])
    iot_df = pd.DataFrame({
        'Hudud': ['Toshkent', 'Nukus', 'Termiz', 'Andijon'],
        'AQI': [115, 190, 165, 70]
    })
    st.plotly_chart(px.bar(iot_df, x='Hudud', y='AQI', color='AQI', title="Havo Sifati (Sensorlar)"))
