import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Eko-Risk AI O'zbekiston", layout="wide")

# 2. Login holatini boshqarish
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 3. Sidebar (Yon panel)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2913/2913520.png", width=100)
st.sidebar.title("Boshqaruv Paneli")

if not st.session_state['logged_in']:
    if st.sidebar.button("Google orqali kirish"):
        st.session_state['logged_in'] = True
        st.rerun()
else:
    st.sidebar.success("✅ Tizimga kirdingiz")
    if st.sidebar.button("Tizimdan chiqish"):
        st.session_state['logged_in'] = False
        st.rerun()

# 4. Asosiy sahifa mazmuni
st.title("🌍 Global Ekologik Risklar va AI Tahlili")

if st.session_state['logged_in']:
    # Kirgandan keyin ko'rinadigan qism
    st.markdown("---")
    
    # Interaktiv ko'rsatkichlar
    col1, col2, col3 = st.columns(3)
    col1.metric("Global Harorat", "+1.2°C", "0.1°C")
    col2.metric("CO2 Darajasi", "417 ppm", "2 ppm")
    col3.metric("O'rmonlar qisqarishi", "12M ga", "-5%", delta_color="inverse")

    # Grafiklar bo'limi
    tab1, tab2 = st.tabs(["📊 Global Xarita", "🔬 AI Risk Analizi"])
    
    with tab1:
        st.subheader("Hududlar bo'yicha ekologik xavf darajasi")
        # Tasodifiy ma'lumotlar bilan xarita yaratish
        map_data = pd.DataFrame({
            'lat': np.random.uniform(37, 45, 20),
            'lon': np.random.uniform(58, 72, 20),
            'xavf': np.random.randint(1, 100, 20)
        })
        st.map(map_data)

    with tab2:
        st.subheader("AI bashorati: Kelgusi 10 yil")
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['Havo sifati', 'Suv tanqisligi', 'Tuproq unumdorligi']
        )
        st.line_chart(chart_data)
else:
    # Kirishdan oldin ko'rinadigan ogohlantirish
    st.warning("⚠️ Diqqat: Ma'lumotlarni ko'rish uchun chap paneldagi 'Google orqali kirish' tugmasini bosing.")
    st.info("Ushbu platforma sun'iy intellekt yordamida ekologik risklarni bashorat qilish uchun mo'ljallangan.")
