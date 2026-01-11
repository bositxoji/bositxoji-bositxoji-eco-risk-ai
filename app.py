import streamlit as st
from groq import Groq
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
try:
    from streamlit_chat import message
except ImportError:
    st.error("Iltimos, requirements.txt fayliga 'streamlit-chat' qo'shilganiga ishonch hosil qiling.")

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Carbon & ArcGIS Expert", layout="wide")

# Xavfsizlik: Kalitlarni kodda yozmang!
# Ularni faqat Streamlit Secrets bo'limiga qo'ying.

lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t_dict = {
    "UZ": {"m1": "🌍 Carbon Footprint (ArcGIS)", "m2": "⏳ Tarixiy Dinamika", "m3": "💬 AI Ekspert Chat"},
    "EN": {"m1": "🌍 Carbon Footprint (ArcGIS)", "m2": "⏳ Historical Dynamics", "m3": "💬 AI Expert Chat"}
}
t = t_dict.get(lang, t_dict["UZ"])

# 2. AI FUNKSIYASI
def get_ai_chat_response(user_input):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": f"Sen PhD ekologsan. {lang} tilida javob ber."},
                      {"role": "user", "content": user_input}]
        )
        return completion.choices[0].message.content
    except: return "Secrets-da GROQ_API_KEY topilmadi."

# 3. SIDEBAR NAVIGATSIYA
with st.sidebar:
    st.title("🌱 Eco ArcGIS Pro")
    menu = st.radio("Bo'limlar:", [t['m1'], t['m2'], t['m3']])
    st.markdown("---")
    st.caption("Prof. Egamberdiyev E.A. | PhD Ataxo'jayev A.")

# --- 1-BO'LIM: CARBON FOOTPRINT (ArcGIS Style) ---
if menu == t['m1']:
    st.header(t['m1'])
    # ArcGIS uslubidagi xarita. Attr xatosi tuzatildi
    m = folium.Map(location=[41.31, 69.24], zoom_start=6)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri, DigitalGlobe, GeoEye, Earthstar Geographics',
        name='ArcGIS World Imagery'
    ).add_to(m)
    
    # Uglerod izi (Lat, Lon, Emissiya)
    carbon_data = [[41.31, 69.24, 0.9], [40.99, 71.67, 0.7], [42.46, 59.61, 1.0]]
    HeatMap(carbon_data, radius=25, gradient={0.2:'blue', 0.5:'yellow', 1:'red'}).add_to(m)
    folium_static(m, width=1100, height=600)

# --- 2-BO'LIM: TARIXIY DINAMIKA ---
elif menu == t['m2']:
    st.header(t['m2'])
    year = st.select_slider("Tahlil yili:", options=list(range(2000, 2027)), value=2024)
    st.subheader(f"📊 {year}-yil uchun ekologik o'zgarishlar bashorati")
    st.info("Bu bo'limda tanlangan yil bo'yicha sun'iy yo'ldosh arxiv ma'lumotlari solishtiriladi.")
    # Vaqt shkalasi bo'yicha tasvirlar (misol)
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aral_Sea_1989-2014.jpg", caption="Orol dengizi retrospektivasi")

# --- 3-BO'LIM: AI EKSPERT CHAT ---
elif menu == t['m3']:
    st.header(t['m3'])
    if 'messages' not in st.session_state: st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
        
    if prompt := st.chat_input("Savolingizni yozing..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        response = get_ai_chat_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"): st.markdown(response)
