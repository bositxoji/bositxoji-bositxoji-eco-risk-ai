import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
from groq import Groq

# 1. SAHIFA SOZLAMALARI VA GOOGLE VERIFICATION
st.set_page_config(
    page_title="Eco-Portal Pro: Global Eko Risk Monitoring",
    page_icon="🌍",
    layout="wide"
)

# Google Search Console Meta Tag
st.markdown('<meta name="google-site-verification" content="maybg4-LdPKEKS8plcTQclxsDBM6XX8lGzOQIwbv0W8" />', unsafe_allow_html=True)

# 2. GROQ API SOZLAMASI
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Secrets bo'limiga 'GROQ_API_KEY' qo'shilmagan!")
    st.stop()

# 3. TIL VA TRANSLATSIYA
lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t_dict = {
    "UZ": {
        "title": "🌱 Eco-Portal Pro AI",
        "m1": "🌍 Global AQI (Jonli)", "m2": "🛰 Sun'iy Yo'ldosh", "m3": "🧪 AI Akademik Tahlil",
        "m4": "📈 PESTEL Strategiya", "m5": "📊 IoT Sensorlar", "m6": "🔮 2030 Bashorat",
        "m7": "⏳ Tarixiy Dinamika", "m8": "🤖 AI Chat Ekspert",
        "btn": "Tahlilni boshlash", "dl": "Yuklab olish"
    }
}
# Boshqa tillar uchun default UZ ishlatiladi
t = t_dict.get(lang, t_dict["UZ"])

# 4. SIDEBAR MENU
st.sidebar.title(t["title"])
menu = st.sidebar.radio("Bo'limlar:", list(t.values())[1:9])
st.sidebar.markdown("---")
st.sidebar.write("**Muallif:** Ataxojayev Abdubosit")

# AI Funksiyasi
def call_ai(prompt, role):
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": role}, {"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Xatolik yuz berdi: {e}"

# 5. ASOSIY BO'LIMLAR LOGIKASI
if menu == t["m1"]:
    st.header(t["m1"])
    st.components.v1.iframe("https://aqicn.org/map/world/", height=700) #

elif menu == t["m2"]:
    st.header(t["m2"])
    m = folium.Map(location=[41.31, 69.24], zoom_start=6)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google', name='Satellite').add_to(m)
    folium_static(m, width=1100)

elif menu in [t["m3"], t["m4"]]:
    st.header(menu)
    user_in = st.text_area("Mavzu:", "Iqlim o'zgarishi va O'zbekiston")
    if st.button(t["btn"]):
        with st.spinner("AI tahlil qilmoqda..."):
            res = call_ai(user_in, "Siz ekologiya bo'yicha PhD olimsiz.")
            st.markdown(res)

elif menu == t["m5"]:
    st.header(t["m5"])
    data = pd.DataFrame({'Shahar': ['Toshkent', 'Samarqand', 'Nukus'], 'AQI': [155, 85, 120]})
    st.plotly_chart(px.bar(data, x='Shahar', y='AQI', color='AQI'))

elif menu == t["m6"]:
    st.header(t["m6"])
    st.line_chart(pd.DataFrame({'Yil': [2024, 2030], 'Resurs': [100, 140]}).set_index('Yil'))

elif menu == t["m7"]:
    st.header(t["m7"])
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aral_Sea_1989-2014.jpg")

elif menu == t["m8"]:
    st.header(t["m8"])
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])
    if p := st.chat_input("Savol bering..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        ans = call_ai(p, "Ekologiya eksperti")
        st.session_state.messages.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"): st.write(ans)
