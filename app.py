import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import json

# 1. SAHIFA KONFIGURATSIYASI
st.set_page_config(page_title="Eko-Portal Pro AI", layout="wide")

# Til sozlamalari lug'ati
lang_dict = {
    "UZ": {"m1": "🛰 Sun'iy Yo'ldosh Monitoringi", "m2": "🤖 Akademik Tahlil & Iqtiboslar", "m3": "📶 IoT Sensorlar", "btn": "Chuqur Tahlil"},
    "EN": {"m1": "🛰 Satellite Monitoring", "m2": "🤖 Academic Analysis & Citations", "m3": "📶 IoT Sensors", "btn": "Deep Analysis"},
    "RU": {"m1": "🛰 Спутниковый мониторинг", "m2": "🤖 ИИ Анализ и Цитаты", "m3": "📶 IoT Сенсоры", "btn": "Глубокий анализ"}
}

lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t = lang_dict[lang]

# 2. GROQ AI FUNKSIYASI (Akademik daraja)
def get_pro_analysis(prompt):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Eng barqaror model
            messages=[
                {"role": "system", "content": f"Sen PhD darajasidagi olimsan. {lang} tilida akademik va imloviy hatolarsiz javob ber. Har bir tahlilda kamida 3 ta ilmiy manba keltir. Oxirida '---DATA---' dan keyin JSON formatda grafik ma'lumotlarini ber."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI xatolik: {str(e)}"

# 3. SIDEBAR MENYU
with st.sidebar:
    st.title("🚀 Pro Dashboard")
    menu = st.radio("Bo'limlar:", [t['m1'], t['m2'], t['m3']])
    st.markdown("---")
    st.write("🎓 **Mualliflar:** Prof. Egamberdiyev E.A. | PhD Ataxo'jayev A.")

# --- 1-BO'LIM: SUN'IY YO'LDOSH MONITORINGI ---
if menu == t['m1']:
    st.header(t['m1'])
    # Xaritadagi 'ValueError' xatosini tuzatish (attribution qo'shildi)
    m = folium.Map(location=[41.311081, 69.240562], zoom_start=6)
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google Satellite Imagery', # Ushbu qator xatoni tuzatadi
        name='Google Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    folium_static(m, width=1100, height=600)

# --- 2-BO'LIM: AKADEMIK TAHLIL ---
elif menu == t['m2']:
    st.header(t['m2'])
    col_in, col_out = st.columns([0.4, 0.6])
    with col_in:
        uploaded_file = st.file_uploader("Ilmiy hujjat yuklang", type=['pdf', 'docx', 'csv'])
        context = st.text_area("Tahliliy savol:", height=200)
        if st.button(t['btn'], use_container_width=True):
            with st.spinner("AI Scopus bazasi asosida tahlil qilmoqda..."):
                res = get_pro_analysis(f"{context} mavzusida ilmiy iqtiboslar bilan maqola tayyorla.")
                st.session_state.analysis_result = res

    with col_out:
        if 'analysis_result' in st.session_state:
            res = st.session_state.analysis_result
            if "---DATA---" in res:
                text, data = res.split("---DATA---")
                st.markdown(text)
                try:
                    graph_data = json.loads(data.strip())
                    fig = px.bar(x=graph_data['labels'], y=graph_data['values'], title=graph_data.get('title', 'Tahlil'))
                    st.plotly_chart(fig)
                except: pass
            else: st.markdown(res)

# --- 3-BO'LIM: IoT SENSORLAR ---
elif menu == t['m3']:
    st.header(t['m3'])
    # IoT ma'lumotlar simulyatsiyasi
    iot_df = pd.DataFrame({
        'Hudud': ['Toshkent', 'Nukus', 'Termiz', 'Andijon'],
        'PM2.5': [45, 118, 92, 35],
        'AQI': [115, 190, 165, 70]
    })
    st.table(iot_df)
    fig_iot = px.line(iot_df, x='Hudud', y='AQI', markers=True, title="Havo Sifati (AQI)")
    st.plotly_chart(fig_iot)
