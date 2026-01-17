import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static

# ---------------------------------------------------------
# 1. GOOGLE SEARCH CONSOLE UCHUN IKKALAY USULNI HAM QO'SHAMIZ
# ---------------------------------------------------------

# A. HTML FAYL USULI (Link orqali tekshirish uchun)
if "google19952789cd1d86.html" in st.query_params:
    st.write("google-site-verification: google19952789cd1d86.html")
    st.stop()

# B. META TAG USULI (Asosiy head qismi uchun)
# Bu funksiya orqali biz Google-ga kerakli kodni majburlab ko'rsatamiz
st.markdown('<p style="display:none;">google-site-verification: maybg4-LdPKEKS8plcTQclxsDBM6XX8lGzOQIwbv0W8</p>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. SAYT KONFIGURATSIYASI
# ---------------------------------------------------------
st.set_page_config(
    page_title="Eco-Portal Pro: Global Eko Risk Monitoring",
    page_icon="🌍",
    layout="wide"
)

# Secrets tekshiruvi
if "GROQ_API_KEY" not in st.secrets:
    st.error("GROQ_API_KEY topilmadi!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------------------------------------------------------
# 3. INTERFEYS (Sizning mavjud kodingiz)
# ---------------------------------------------------------
st.sidebar.title("🌱 Eco-Portal Pro AI")
menu = st.sidebar.radio("Bo'limni tanlang:", ["🌍 Global AQI (Jonli)", "🤖 AI Chat Ekspert"])

if menu == "🌍 Global AQI (Jonli)":
    st.header("🌍 Global AQI (Jonli)")
    st.components.v1.iframe("https://aqicn.org/map/world/", height=650)

elif menu == "🤖 AI Chat Ekspert":
    st.header("🤖 AI Chat Ekspert")
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])
    
    if p := st.chat_input("Savol bering..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": p}]
        )
        ans = res.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"): st.write(ans)
