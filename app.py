import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import json

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Portal Predictive AI", layout="wide")

# MAXFIY KALITLARNI FAQAT SECRETS'DAN OLAMIZ (Leak xavfi yo'q)
# Secrets-ga GROQ_API_KEY qo'shilganiga ishonch hosil qiling!

lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t_dict = {
    "UZ": {"m1": "🗺 Issiqlik Xaritasi", "m2": "🧠 PESTEL & Ssenariylar", "btn": "Strategik Tahlil"},
    "EN": {"m1": "🗺 Heatmap Analysis", "m2": "🧠 PESTEL & Scenarios", "btn": "Strategic Analysis"},
    "RU": {"m1": "🗺 Тепловая карта", "m2": "🧠 PESTEL и Сценарии", "btn": "Стратегический анализ"}
}
t = t_dict[lang]

# 2. STRATEGIK AI FUNKSIYASI (Akademik va Iqtibosli)
def get_strategic_analysis(prompt):
    try:
        # Kod ichida API kalit yozish taqiqlanadi!
        client = Groq(api_key=st.secrets["GROQ_API_KEY"]) 
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Sen PhD darajasidagi tahlilchisan. {lang} tilida PESTEL metodikasida va ssenariylar bilan javob ber."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Xatolik: API kalitni Streamlit Secrets'ga qo'shing!"

# 3. SIDEBAR
with st.sidebar:
    st.title("🚀 Strategic AI")
    menu = st.radio("Bo'limlar:", [t['m1'], t['m2']])
    st.markdown("---")
    st.write("🎓 **Mualliflar:** Prof. Egamberdiyev E.A. | PhD Ataxo'jayev A.")

# --- ISSIQLIK XARITASI (Tuzatilgan versiya) ---
if menu == t['m1']:
    st.header(t['m1'])
    # ValueError xatosi 'attr' qo'shish bilan tuzatildi
    m = folium.Map(location=[41.31, 69.24], zoom_start=6)
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', 
        attr='Google Satellite Imagery', 
        name='Satellite'
    ).add_to(m)
    
    # Simulyatsiya qilingan issiqlik ma'lumotlari
    heat_data = [[41.31, 69.24, 0.9], [42.46, 59.61, 1.0], [37.22, 67.27, 0.8]]
    HeatMap(heat_data, radius=20, blur=15).add_to(m)
    folium_static(m, width=1100, height=600)

# --- PESTEL & SSENARIYLAR ---
elif menu == t['m2']:
    st.header(t['m2'])
    topic = st.text_input("Tahlil mavzusi:", "Orolbo'yi mintaqasining 2030-yilgacha bo'lgan ekologik ssenariylari")
    if st.button(t['btn']):
        with st.spinner("AI strategik tahlil o'tkazmoqda..."):
            res = get_strategic_analysis(f"{topic} mavzusida PESTEL tahlil va 3 xil (optimistik, realistik, pessmistik) ssenariy yoz.")
            st.markdown(res)
