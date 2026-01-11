import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
try:
    from streamlit_chat import message
except: pass

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Portal Global AI", layout="wide")

# Til lug'ati
lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t_dict = {
    "UZ": {
        "m1": "📊 Global AQI", "m2": "🌍 Carbon ArcGIS", "m3": "🛰 Issiqlik Xaritasi",
        "m4": "🤖 AI Risk Tahlil", "m5": "🧠 PESTEL Strategiya", "m6": "💬 AI Chat", "m7": "📶 IoT"
    }
}
t = t_dict.get(lang, t_dict["UZ"])

# 2. AI FUNKSIYASI (Secrets orqali)
def get_ai_res(prompt, system):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        comp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}]
        )
        return comp.choices[0].message.content
    except: return "Xatolik: API kalitni Secrets-ga qo'shing!"

# 3. SIDEBAR NAVIGATSIYA (Hamma bo'limlar shu yerda!)
with st.sidebar:
    st.title("🌱 Eco-Global Pro")
    menu = st.radio("Bo'limni tanlang:", list(t.values()))
    st.markdown("---")
    st.caption("Prof. Egamberdiyev E.A. | PhD Ataxo'jayev A.")

# --- BO'LIMLAR ---
if menu == t['m1']:
    st.header(t['m1'])
    st.components.v1.iframe("https://aqicn.org/map/world/", height=700)

elif menu == t['m2']: # CARBON FOOTPRINT ARCGIS
    st.header(t['m2'])
    m = folium.Map(location=[41.31, 69.24], zoom_start=6)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri, ArcGIS', name='ArcGIS').add_to(m)
    # Carbon Heatmap (To'g'rilangan intensivlik)
    c_data = [[41.31, 69.24, 0.8], [42.46, 59.61, 1.0], [37.22, 67.27, 0.7]]
    HeatMap(c_data, radius=35, blur=20, gradient={0.4:'blue', 0.65:'lime', 1:'red'}).add_to(m)
    folium_static(m, width=1100)

elif menu == t['m4']: # AI RISK TAHLIL
    st.header(t['m4'])
    txt = st.text_area("Ma'lumot kiriting:")
    if st.button("Tahlil"):
        st.markdown(get_ai_res(txt, "Sen PhD ekologsan. Akademik tahlil yoz."))

elif menu == t['m5']: # PESTEL
    st.header(t['m5'])
    p_txt = st.text_input("Mavzu:", "Orolbo'yi 2030")
    if st.button("Ssenariy tuzish"):
        st.markdown(get_ai_res(p_txt, "Sen strategik tahlilchisan. PESTEL tahlil yoz."))

elif menu == t['m6']: # AI CHAT
    st.header(t['m6'])
    if 'msgs' not in st.session_state: st.session_state.msgs = []
    if prompt := st.chat_input("Savol..."):
        st.session_state.msgs.append({"r": "u", "c": prompt})
        res = get_ai_res(prompt, "PhD Ekspert maslahatchi.")
        st.session_state.msgs.append({"r": "a", "c": res})
    for m in st.session_state.msgs:
        with st.chat_message("user" if m["r"]=="u" else "assistant"): st.write(m["c"])
