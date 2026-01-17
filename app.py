import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static

# ---------------------------------------------------------
# 1. GOOGLE SEARCH CONSOLE TASDIQLASH (HTML FAYL USULI)
# ---------------------------------------------------------
# Google botlari uchun maxsus "eshtik"
if "google19952789cd1d86.html" in st.query_params:
    st.write("google-site-verification: google19952789cd1d86.html")
    st.stop()

# ---------------------------------------------------------
# 2. SAYT SOZLAMALARI
# ---------------------------------------------------------
st.set_page_config(
    page_title="Eco-Portal Pro: Global Eko Risk Monitoring",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------------------------------
# 3. API VA SOZLAMALAR
# ---------------------------------------------------------
if "GROQ_API_KEY" not in st.secrets:
    st.error("Xatolik: Secrets bo'limiga 'GROQ_API_KEY' kiritilmagan!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Tilni tanlash
lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t_dict = {
    "UZ": {
        "title": "🌱 Eco-Portal Pro AI",
        "m1": "🌍 Global AQI (Jonli)", "m2": "🛰 Sun'iy Yo'ldosh", "m3": "🧪 AI Akademik Tahlil",
        "m4": "📈 PESTEL Strategiya", "m5": "📊 IoT Sensorlar (12 viloyat)", "m6": "🔮 2030 Bashorat",
        "m7": "⏳ Tarixiy Dinamika", "m8": "🤖 AI Chat Ekspert",
        "btn": "Tahlilni boshlash", "dl": "Hisobotni yuklab olish"
    },
    "EN": {
        "title": "🌱 Eco-Portal Pro AI",
        "m1": "🌍 Global AQI (Live)", "m2": "🛰 Satellite View", "m3": "🧪 AI Academic Analysis",
        "m4": "📈 PESTEL Strategy", "m5": "📊 IoT Sensors", "m6": "🔮 2030 Forecast",
        "m7": "⏳ Historical Dynamics", "m8": "🤖 AI Expert Chat",
        "btn": "Run Analysis", "dl": "Download"
    }
}
t = t_dict.get(lang, t_dict["UZ"])

# ---------------------------------------------------------
# 4. SIDEBAR VA NAVIGATSIYA
# ---------------------------------------------------------
st.sidebar.title(t["title"])
menu = st.sidebar.radio("Bo'limni tanlang:", list(t.values())[1:9])
st.sidebar.markdown("---")
st.sidebar.write(f"**Muallif:** Ataxojayev Abdubosit")
st.sidebar.write(f"**Ilmiy rahbar:** Prof. Egamberdiyev E.A.")

def call_ai(prompt, role):
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": role}, {"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Xatolik: {e}"

# ---------------------------------------------------------
# 5. ASOSIY BO'LIMLAR
# ---------------------------------------------------------

if menu == t["m1"]:
    st.header(t["m1"])
    st.components.v1.iframe("https://aqicn.org/map/world/", height=650)

elif menu == t["m2"]:
    st.header(t["m2"])
    m = folium.Map(location=[41.31, 69.24], zoom_start=6)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google', name='Satellite').add_to(m)
    folium_static(m, width=1100)

elif menu in [t["m3"], t["m4"]]:
    st.header(menu)
    user_in = st.text_area("Mavzu:", "O'zbekistonda iqlim o'zgarishi tahlili")
    if st.button(t["btn"]):
        with st.spinner("AI tahlil qilmoqda..."):
            role = "PhD Scientist" if menu == t["m3"] else "Policy Analyst"
            res = call_ai(user_in, f"Provide professional analysis in {lang}")
            st.markdown(res)

elif menu == t["m5"]:
    st.header(t["m5"])
    df = pd.DataFrame({'Hudud': ['Toshkent', 'Samarqand', 'Nukus'], 'AQI': [115, 82, 195]})
    st.plotly_chart(px.bar(df, x='Hudud', y='AQI', color='AQI', template="plotly_dark"))

elif menu == t["m8"]:
    st.header(t["m8"])
    if "msgs" not in st.session_state: st.session_state.msgs = []
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]): st.write(m["content"])
    if p := st.chat_input("Savol bering..."):
        st.session_state.msgs.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        ans = call_ai(p, "Siz ekologiya mutaxassisiz.")
        st.session_state.msgs.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"): st.write(ans)
