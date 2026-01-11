import streamlit as st
from groq import Groq
import pandas as pd
import folium
from folium.plugins import HeatMap, TimeSliderChoropleth
from streamlit_folium import folium_static
from streamlit_chat import message # Chatbot interfeysi uchun

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Carbon & AI Portal", layout="wide")

# Til lug'ati
lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t_dict = {
    "UZ": {"m1": "🌍 Carbon Footprint (ArcGIS)", "m2": "⏳ Tarixiy O'zgarishlar", "m3": "💬 AI Ekspert Chat", "btn": "Hisoblash"},
    "EN": {"m1": "🌍 Carbon Footprint Map", "m2": "⏳ Historical Timeline", "m3": "💬 AI Expert Chat", "btn": "Calculate"}
}
t = t_dict.get(lang, t_dict["UZ"])

# 2. AI FUNKSIYASI (Secrets orqali xavfsiz)
def get_ai_chat_response(user_input):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Sen PhD darajasidagi ekologsan. {lang} tilida foydalanuvchiga maslahat ber."},
                {"role": "user", "content": user_input}
            ]
        )
        return completion.choices[0].message.content
    except Exception: return "API kalitni tekshiring!"

# 3. SIDEBAR
with st.sidebar:
    st.title("🌱 Eco-Advanced")
    menu = st.radio("Bo'limlar:", [t['m1'], t['m2'], t['m3']])
    st.markdown("---")
    st.caption("Prof. Egamberdiyev E.A. | PhD Ataxo'jayev A.")

# --- 1-BO'LIM: CARBON FOOTPRINT (ArcGIS Style) ---
if menu == t['m1']:
    st.header(t['m1'])
    st.write("🏭 **Sanoat zonalari va shaharlarning uglerod emissiyasi tahlili:**")
    
    # ArcGIS uslubidagi xarita (Satellite + Carbon Heatmap)
    m = folium.Map(location=[41.31, 69.24], zoom_start=6)
    folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', 
                     attr='Esri, DigitalGlobe, GeoEye, Earthstar Geographics', name='ArcGIS Satellite').add_to(m)
    
    # Uglerod izi ma'lumotlari (Lat, Lon, Emissiya tonnada)
    carbon_data = [[41.31, 69.24, 1.5], [40.99, 71.67, 1.2], [42.46, 59.61, 2.0], [40.45, 71.78, 1.8]]
    HeatMap(carbon_data, radius=30, gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}).add_to(m)
    folium_static(m, width=1100, height=600)

# --- 2-BO'LIM: TARIXIY O'ZGARISHLAR ---
elif menu == t['m2']:
    st.header(t['m2'])
    year = st.slider("Yilni tanlang:", 2010, 2026, 2024)
    st.info(f"📅 {year}-yil holatiga ko'ra hududdagi cho'llanish va o'rmon qatlami dinamikasi.")
    # Bu yerda yilga qarab xarita qatlamini o'zgartirish mumkin
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Aral_Sea_1989-2014.jpg/800px-Aral Sea 1989-2014.jpg", caption="Orol dengizi retrospektiv tahlili")

# --- 3-BO'LIM: AI EKSPERT CHAT ---
elif menu == t['m3']:
    st.header(t['m3'])
    if 'chat_history' not in st.session_state: st.session_state.chat_history = []
    
    user_msg = st.chat_input("Savolingizni yozing (masalan: Uglerod izini qanday kamaytirish mumkin?)...")
    if user_msg:
        st.session_state.chat_history.append({"user": user_msg})
        ans = get_ai_chat_response(user_msg)
        st.session_state.chat_history.append({"ai": ans})
        
    for chat in st.session_state.chat_history:
        if "user" in chat: st.chat_message("user").write(chat["user"])
        if "ai" in chat: st.chat_message("assistant").write(chat["ai"])
