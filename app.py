import streamlit as st
import pandas as pd
import numpy as np

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Eko-Risk AI", layout="wide")

# 2. TILLAR VA MATNLAR LUG'ATI
if 'lang' not in st.session_state:
    st.session_state.lang = 'UZ'

content = {
    'UZ': {
        'title': "🌍 Global Ekologik Risklar va AI Tahlili",
        'sidebar': "Boshqaruv Paneli",
        'warning': "⚠️ Kirish uchun tugmani bosing.",
        'welcome': "Xush kelibsiz!",
        'login': "Google orqali kirish",
        'logout': "Chiqish"
    },
    'RU': {
        'title': "🌍 Глобальные экологические риски и ИИ анализ",
        'sidebar': "Панель управления",
        'warning': "⚠️ Пожалуйста, войдите в систему.",
        'welcome': "Добро пожаловать!",
        'login': "Войти через Google",
        'logout': "Выйти"
    },
    'EN': {
        'title': "🌍 Global Environmental Risks & AI Analysis",
        'sidebar': "Control Panel",
        'warning': "⚠️ Please log in to continue.",
        'welcome': "Welcome!",
        'login': "Login with Google",
        'logout': "Logout"
    }
}

t = content[st.session_state.lang]

# 3. TUN/KUN VA VIDEO FON (CSS)
st.markdown(f"""
    <style>
    /* Harakatlanuvchi fon videosi */
    #bgVideo {{
        position: fixed;
        right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -1;
        filter: brightness(50%); /* Matnlar ko'rinishi uchun rasm biroz qoraytirilgan */
    }}

    /* Matnlar ko'rinishi uchun maxsus soya va oq rang */
    .main .block-container h1, .main .block-container h2, .main .block-container p {{
        color: white !important;
        text-shadow: 2px 2px 4px #000000;
    }}

    /* Sidebar - Siz so'ragan ideal yashil */
    [data-testid="stSidebar"] {{
        background-color: #1E3932 !important;
    }}

    /* Footer - Abdubositxo'ja */
    .footer {{
        position: fixed;
        right: 20px;
        bottom: 20px;
        color: white;
        font-weight: bold;
        background: rgba(0,0,0,0.7);
        padding: 5px 15px;
        border-radius: 10px;
        z-index: 1000;
    }}
    </style>

    <video autoplay muted loop playsinline id="bgVideo">
        <source src="https://assets.mixkit.co/videos/preview/mixkit-rotating-earth-in-space-11119-large.mp4" type="video/mp4">
    </video>
    
    <div class="footer">by Abdubositxo'ja</div>
    """, unsafe_allow_html=True)

# 4. SIDEBAR - TILLARNI TANLASH
st.sidebar.title(t['sidebar'])

# Til tugmalari
col_uz, col_ru, col_en = st.sidebar.columns(3)
if col_uz.button("UZ"): st.session_state.lang = 'UZ'; st.rerun()
if col_ru.button("RU"): st.session_state.lang = 'RU'; st.rerun()
if col_en.button("EN"): st.session_state.lang = 'EN'; st.rerun()

st.sidebar.markdown("---")

# Login qismi
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    if st.sidebar.button(t['login']):
        st.session_state['logged_in'] = True
        st.rerun()
else:
    st.sidebar.success(f"✅ {t['welcome']}")
    if st.sidebar.button(t['logout']):
        st.session_state['logged_in'] = False
        st.rerun()

# 5. ASOSIY SAHIFA
st.title(t['title'])

if st.session_state['logged_in']:
    st.write(f"### {t['welcome']}")
    # AI Bashorat va boshqa qismlar shu yerda bo'ladi
else:
    st.warning(t['warning'])
