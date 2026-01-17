import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import datetime

# ---------------------------------------------------------
# 1. GOOGLE TASDIQLASH (HTML FAYL VA META TAG)
# ---------------------------------------------------------
# Google botlari HTML fayl so'raganda javob qaytarish
if "google19952789cd1d86.html" in st.query_params:
    st.write("google-site-verification: google19952789cd1d86.html")
    st.stop()

st.set_page_config(
    page_title="Eco-Portal Pro: Global Eko Risk Monitoring",
    page_icon="🌍",
    layout="wide"
)

# Meta Tag usuli uchun (Zaxira)
st.markdown('<meta name="google-site-verification" content="maybg4-LdPKEKS8plcTQclxsDBM6XX8lGzOQIwbv0W8" />', unsafe_allow_html=True)

# SEO uchun yashirin matn
st.markdown('<h1 style="display:none;">Ataxojayev Abdubosit va Prof. Egamberdiyev: Eko Risk Monitoring AI Portal</h1>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. API VA SOZLAMALAR
# ---------------------------------------------------------
if "GROQ_API_KEY" not in st.secrets:
    st.error("Secrets bo'limiga 'GROQ_API_KEY' kiritilmagan!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

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
        "m4": "📈 PESTEL Strategy", "m5": "📊 IoT Sensors (12 regions)", "m6": "🔮 2030 Forecast",
        "m7": "⏳ Historical Dynamics", "m8": "🤖 AI Expert Chat",
        "btn": "Run Analysis", "dl": "Download Report"
    }
}
t = t_dict.get(lang, t_dict["UZ"])

# ---------------------------------------------------------
# 3. SIDEBAR VA NAVIGATSIYA
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
# 4. ASOSIY FUNKSIYALAR
# ---------------------------------------------------------

if menu == t["m1"]:
    st.header(t["m1"])
    st.components.v1.iframe("https://aqicn.org/map/world/", height=650)

elif menu == t["m2"]:
    st.header(t["m2"])
    m = folium.Map(location=[41.31, 69.24], zoom_start=6)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google', name='Satellite').add_to(m)
    folium_static(m, width=1100) #

elif menu in [t["m3"], t["m4"]]:
    st.header(menu)
    user_in = st.text_area("Mavzu:", "Impact of climate change in Uzbekistan")
    if st.button(t["btn"]):
        with st.spinner("AI tahlil qilmoqda..."):
            role = "PhD Scientist" if menu == t["m3"] else "Policy Analyst"
            res = call_ai(user_in, f"Provide professional analysis in {lang}")
            st.markdown(res) #
            st.download_button(t["dl"], res, file_name="eco_report.txt")

elif menu == t["m5"]:
    st.header(t["m5"])
    df = pd.DataFrame({
        'Hudud': ['Toshkent', 'Samarqand', 'Nukus', 'Buxoro', 'Andijon'],
        'AQI': [115, 82, 195, 88, 110]
    })
    st.plotly_chart(px.bar(df, x='Hudud', y='AQI', color='AQI', template="plotly_dark")) #

elif menu == t["m6"]:
    st.header(t["m6"])
    f_df = pd.DataFrame({'Yil': [2024, 2026, 2028, 2030], 'Ekologik Barqarorlik %': [55, 65, 78, 92]})
    st.line_chart(f_df.set_index('Yil'))

elif menu == t["m7"]:
    st.header(t["m7"])
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aral_Sea_1989-2014.jpg", caption="Aral Sea 1989-2014") #

elif menu == t["m8"]:
    st.header(t["m8"])
    if "msgs" not in st.session_state: st.session_state.msgs = []
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]): st.write(m["content"])
    if p := st.chat_input("Savol yozing..."):
        st.session_state.msgs.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        ans = call_ai(p, "Siz ekologiya bo'yicha mutaxassissiz.")
        st.session_state.msgs.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"): st.write(ans)
