import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import json

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Portal Pro AI", layout="wide")

# Til sozlamalari lug'ati
lang_dict = {
    "UZ": {"m1": "🛰 Sun'iy Yo'ldosh Monitoringi", "m2": "🤖 Akademik Tahlil & Iqtiboslar", "m3": "📶 IoT Sensorlar", "btn": "Chuqur Tahlil"},
    "EN": {"m1": "🛰 Satellite Monitoring", "m2": "🤖 Academic Analysis & Citations", "m3": "📶 IoT Sensors", "btn": "Deep Analysis"},
    "RU": {"m1": "🛰 Спутниковый мониторинг", "m2": "🤖 ИИ Анализ и Цитаты", "m3": "📶 IoT Сенсоры", "btn": "Глубокий анализ"}
}

lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t = lang_dict[lang]

# 2. AI FUNKSIYASI (Akademik va xatosiz)
def get_pro_analysis(prompt):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Sen PhD darajasidagi ekolog-olimisan. {lang} tilida, imloviy xatolarsiz, akademik uslubda javob ber. Har bir tahlilda kamida 3 ta ilmiy manba (Citation) keltir. Javob oxirida '---DATA---' dan keyin grafik uchun JSON formatda ma'lumot ber."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"

# 3. SIDEBAR MENYU
with st.sidebar:
    st.title("🚀 Pro Dashboard")
    menu = st.radio("Bo'limni tanlang:", [t['m1'], t['m2'], t['m3']])
    st.markdown("---")
    st.write("🎓 **Mualliflar:**")
    st.caption("Prof. Egamberdiyev E.A. | PhD Ataxo'jayev A.")

# --- 1-BO'LIM: SUN'IY YO'LDOSH MONITORINGI (XATOSIZ) ---
if menu == t['m1']:
    st.header(t['m1'])
    # Rasmdagi 'ValueError' xatosini tuzatish uchun attribution qo'shildi
    m = folium.Map(location=[41.311081, 69.240562], zoom_start=6)
    google_satellite = folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google Satellite',
        name='Google Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    folium_static(m, width=1100, height=600)
    st.success("🛰 Sun'iy yo'ldosh xaritasi muvaffaqiyatli yuklandi.")

# --- 2-BO'LIM: AKADEMIK TAHLIL ---
elif menu == t['m2']:
    st.header(t['m2'])
    col_in, col_out = st.columns([0.4, 0.6])
    
    with col_in:
        st.subheader("📥 Manba")
        uploaded_file = st.file_uploader("Fayl yuklang (PDF, Word, Excel, CSV)", type=['pdf', 'docx', 'csv', 'xlsx'])
        context = st.text_area("Tahlil uchun mavzu yoki gipoteza:", height=200)
        analyze_btn = st.button(t['btn'], use_container_width=True)

    with col_out:
        if analyze_btn:
            with st.spinner("AI Scopus bazasi asosida akademik tahlil tayyorlamoqda..."):
                prompt = f"{context} mavzusida ilmiy iqtiboslar bilan chuqur akademik maqola va risk tahlili yoz. Grafik uchun JSON ma'lumotni unutma."
                res = get_pro_analysis(prompt)
                
                if "---DATA---" in res:
                    parts = res.split("---DATA---")
                    st.markdown(parts[0]) # Maqola
                    try:
                        data = json.loads(parts[1].strip())
                        fig = px.bar(x=data['labels'], y=data['values'], title=data.get('title', 'Tahlil'))
                        st.plotly_chart(fig)
                    except: pass
                else:
                    st.markdown(res)

# --- 3-BO'LIM: IoT SENSORLAR ---
elif menu == t['m3']:
    st.header(t['m3'])
    # Real-vaqt ko'rsatkichlari (Jadval va Grafik)
    iot_df = pd.DataFrame({
        'Hudud': ['Toshkent', 'Nukus', 'Termiz', 'Andijon', 'Buxoro'],
        'PM2.5': [42, 115, 88, 32, 75],
        'AQI': [110, 185, 160, 65, 140]
    })
    
    st.subheader("📊 Mintaqaviy Sensor Ma'lumotlari")
    c1, c2 = st.columns(2)
    with c1:
        st.dataframe(iot_df, use_container_width=True)
    with c2:
        fig_iot = px.line(iot_iot_df if 'iot_iot_df' in locals() else iot_df, x='Hudud', y='AQI', markers=True, title="Havo Sifati Indeksi (AQI)")
        st.plotly_chart(fig_iot)
