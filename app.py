import streamlit as st

# 1. GOOGLE TASDIQLASH KODI (Eng tepada bo'lishi shart!)
st.markdown('<meta name="google-site-verification" content="maybg4-LdPKEKS8plcTQclxsDBM6XX8lGzOQIwbv0W8" />', unsafe_allow_html=True)

# 2. SAYT SARLAVHASI
st.set_page_config(page_title="Eco-Portal Pro AI", layout="wide")

st.title("🌱 Eco-Portal Pro: Global Monitoring")
st.write("Sayt Google qidiruv tizimiga ulanmoqda...")

# 3. AQI XARITASI (Google botiga ko'rinishi uchun oddiyroq qildik)
st.components.v1.iframe("https://aqicn.org/map/world/", height=600)

st.sidebar.write("Muallif: Ataxojayev Abdubosit")
