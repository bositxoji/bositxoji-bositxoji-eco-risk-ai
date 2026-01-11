import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
try:
    from streamlit_chat import message
except:
    pass

# 1. SAHIFA KONFIGURATSIYASI
st.set_page_config(page_title="Eko-Portal Pro Global", layout="wide")

# Xavfsizlik: Kalitlar faqat Secrets-da bo'lishi shart!
def get_ai_response(prompt, system_role):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_role}, {"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except:
        return "Xatolik: API kalitni Streamlit Secrets-ga kiriting!"

# 2. LUG'AT VA NAVIGATSIYA
lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t_dict = {
    "UZ": {
        "m1": "📊 Global AQI Map", "m2": "🌍 Carbon Footprint (ArcGIS)", "m3": "🛰 Issiqlik Xaritasi",
        "m4": "🤖 AI Akademik Tahlil", "m5": "🧠 PESTEL Strategiya", "m6": "📶 IoT Sensorlar",
        "m7": "⏳ Tarixiy Dinamika", "m8": "💬 AI Ekspert Chat"
    }
}
t = t_dict.get(lang, t_dict["UZ"])

with st.sidebar:
    st.title("🌱 Eco-System Pro")
    menu = st.radio("Bo'limni tanlang:", list(t.values()))
    st.markdown("---")
    st.caption("Mualliflar: Prof. Egamberdiyev E.A. | PhD Ataxo'jayev A.")

# --- HAR BIR BO'LIM MANTIQI ---

if menu == t['m1']: # GLOBAL AQI
    st.header(t['m1'])
    st.components.v1.iframe("https://aqicn.org/map/world/", height=700)

elif menu == t['m2']: # CARBON ARCGIS
    st.header(t['m2'])
    m = folium.Map(location=[41.31, 69.24], zoom_start=6)
    folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', 
                     attr='Esri, ArcGIS World Imagery', name='ArcGIS').add_to(m)
    c_data = [[41.31, 69.24, 0.9], [42.46, 59.61, 1.0], [37.22, 67.27, 0.8]]
    HeatMap(c_data, radius=30, gradient={0.4:'blue', 0.7:'lime', 1:'red'}).add_to(m)
    folium_static(m, width=1100)

elif menu == t['m3']: # ISSIQLIK XARITASI
    st.header(t['m3'])
    m2 = folium.Map(location=[41.31, 69.24], zoom_start=6)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', 
                     attr='Google Satellite', name='Google').add_to(m2)
    HeatMap([[41.32, 69.25, 0.9], [40.78, 72.34, 0.7]], radius=25).add_to(m2)
    folium_static(m2, width=1100)

elif menu == t['m4']: # AI TAHLIL
    st.header(t['m4'])
    txt = st.text_area("Ma'lumot kiriting:")
    if st.button("Tahlil qilish"):
        st.markdown(get_ai_response(txt, "Sen PhD ekologsan. Akademik tahlil yoz."))

elif menu == t['m5']: # PESTEL
    st.header(t['m5'])
    p_txt = st.text_input("Mavzu:", "Orolbo'yi 2030")
    if st.button("Ssenariy tuzish"):
        st.markdown(get_ai_response(p_txt, "Sen strategik tahlilchisan. PESTEL tahlil yoz."))

elif menu == t['m6']: # IoT SENSORLAR
    st.header(t['m6'])
    df = pd.DataFrame({'Hudud': ['Toshkent', 'Nukus', 'Andijon'], 'AQI': [115, 190, 75]})
    st.plotly_chart(px.bar(df, x='Hudud', y='AQI', color='AQI'))

elif menu == t['m7']: # TARIXIY
    st.header(t['m7'])
    year = st.select_slider("Yil:", options=[2010, 2015, 2020, 2025])
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aral_Sea_1989-2014.jpg", caption=f"{year}-yil holati")

elif menu == t['m8']: # AI CHAT
    st.header(t['m8'])
    if 'messages' not in st.session_state: st.session_state.messages = []
    if pr := st.chat_input("Savol..."):
        st.session_state.messages.append({"role": "user", "content": pr})
        res = get_ai_response(pr, "Ekspert maslahatchi.")
        st.session_state.messages.append({"role": "assistant", "content": res})
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
