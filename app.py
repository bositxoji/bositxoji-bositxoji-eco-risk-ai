import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Sahifa sozlamalari
st.set_page_config(page_title="Eko-Risk AI O'zbekiston", layout="wide")

# Google kalitlarini Secrets'dan olish
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]

# Login holatini tekshirish
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Sidebar qismi
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2913/2913520.png", width=100)

if not st.session_state['logged_in']:
    if st.sidebar.button("Google orqali kirish"):
        # Bu yerda foydalanuvchi muvaffaqiyatli kirdi deb hisoblaymiz
        st.session_state['logged_in'] = True
        st.rerun()
else:
    st.sidebar.success("Xush kelibsiz!")
    if st.sidebar.button("Tizimdan chiqish"):
        st.session_state['logged_in'] = False
        st.rerun()

# Asosiy sahifa
st.title("🌍 Global Ekologik Risklar va AI Tahlili")

if st.session_state['logged_in']:
    st.markdown("---")
    # Bu yerda sizning asosiy tahliliy bloklaringiz bo'ladi
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Global Statistikalar")
        st.bar_chart(np.random.randn(10, 2))
    with col2:
        st.subheader("🔬 AI Bashorati")
        st.line_chart(np.random.randn(10, 2))
else:
    st.warning("Iltimos, tizimga kirish uchun chap tarafdagi tugmani bosing.")
