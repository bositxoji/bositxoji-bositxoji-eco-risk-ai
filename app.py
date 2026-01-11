import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import json

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Portal Pro AI", layout="wide")

# Til sozlamalari
lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t_dict = {
    "UZ": {"m1": "🛰 Sun'iy Yo'ldosh Monitoringi", "m2": "🤖 Akademik Tahlil & Iqtiboslar", "m3": "📶 IoT Sensorlar", "btn": "Chuqur Tahlil"},
    "EN": {"m1": "🛰 Satellite Monitoring", "m2": "🤖 Academic Analysis & Citations", "m3": "📶 IoT Sensors", "btn": "Deep Analysis"},
    "RU": {"m1": "🛰 Спутниковый мониторинг", "m2": "🤖 ИИ Анализ и Цитаты", "m3": "📶 IoT Сенсоры", "btn": "Глубокий анализ"}
}
t = t_dict[lang]

# 2. AI FUNKSIYASI (Scopus/Web of Science iqtiboslari bilan)
def get_pro_analysis(prompt):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Sen dunyoga mashhur ekolog-olim va tahlilchisan. {lang} tilida javob ber. Har bir tahlilingda kamida 3 ta haqiqiy ilmiy manba (Scopus/Web of Science uslubida) keltir. Javob oxirida grafik uchun JSON ma'lumot ber."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"

# 3. SIDEBAR MENYU
with st.sidebar:
    st.title("🚀 Pro Dashboard")
    menu = st.radio("Bo'limni tanlang:", [t['m1'], t['m2'], t['m3']])
    st.markdown("---")
    st.write("🎓 **Mualliflar:** Prof. Egamberdiyev E.A. | PhD Ataxo'jayev A.")

# --- 1-TAKLIFF: SUN'IY YO'LDOSH MONITORINGI ---
if menu == t['m1']:
    st.header(t['m1'])
    # Sun'iy yo'ldosh xaritasi (Folium orqali Sentinel/Google uslubida)
    m = folium.Map(location=[41.311081, 69.240562], zoom_start=6, tiles="Stamen Terrain")
    folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google', name='Satellite').add_to(m)
    folium_static(m, width=1100, height=600)
    st.info("ℹ️ Yuqoridagi xarita hududiy o'zgarishlarni kuzatish uchun sun'iy yo'ldosh tasvirlari rejimida ishlamoqda.")

# --- 2 VA 4-TAKLIFFLAR: AKADEMIK TAHLIL + IQTIBOSLAR ---
elif menu == t['m2']:
    st.header(t['m2'])
    col_in, col_out = st.columns([0.4, 0.6])
    
    with col_in:
        uploaded_file = st.file_uploader("Ilmiy hujjat yuklang (PDF/Word/Excel)", type=['pdf', 'docx', 'csv'])
        context = st.text_area("Tahliliy savolingiz yoki gipoteza:", height=200)
        analyze_btn = st.button(t['btn'], use_container_width=True)

    with col_out:
        if analyze_btn:
            with st.spinner("AI Scopus va Web of Science bazalari asosida iqtiboslar bilan tahlil tayyorlamoqda..."):
                res = get_pro_analysis(f"{context} mavzusida ilmiy iqtiboslar (citations) bilan maqola va risk tahlili yoz.")
                if "---DATA---" in res:
                    text, data = res.split("---DATA---")
                    st.markdown(text)
                else:
                    st.markdown(res)

# --- 2-TAKLIFF: IoT SENSORLAR INTERFEYSI ---
elif menu == t['m3']:
    st.header(t['m3'])
    st.write("📊 **Mahalliy IoT sensorlardan kelayotgan real-vaqt ma'lumotlari:**")
    
    # Simulyatsiya qilingan IoT ma'lumotlari
    iot_data = pd.DataFrame({
        'Hudud': ['Toshkent', 'Nukus', 'Termiz', 'Andijon'],
        'Chang (PM2.5)': [45, 120, 85, 30],
        'Namlik (%)': [35, 15, 20, 45],
        'Harorat (°C)': [22, 28, 32, 20]
    })
    
    col1, col2 = st.columns(2)
    with col1:
        st.table(iot_data)
    with col2:
        fig = px.bar(iot_data, x='Hudud', y='Chang (PM2.5)', color='Chang (PM2.5)', title="Chang miqdori (Sensorlar)")
        st.plotly_chart(fig)
