import streamlit as st
import pandas as pd
import numpy as np

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Eko-Risk AI", layout="wide")

# 2. Session State - Til va Mavzu (Tun/Kun)
if 'lang' not in st.session_state: st.session_state.lang = 'UZ'
if 'theme' not in st.session_state: st.session_state.theme = 'dark'

# Tillar lug'ati
content = {
    'UZ': {'title': "🌍 Global Ekologik Risklar va AI Tahlili", 'login': "Kirish", 'sidebar': "Boshqaruv", 'theme_btn': "Mavzu"},
    'RU': {'title': "🌍 Глобальные эко-риски и ИИ анализ", 'login': "Вход", 'sidebar': "Управление", 'theme_btn': "Тема"},
    'EN': {'title': "🌍 Global Eco Risks & AI Analysis", 'login': "Login", 'sidebar': "Control", 'theme_btn': "Theme"}
}
t = content[st.session_state.lang]

# 3. DINAMIK DIZAYN (Video va CSS)
overlay_color = "rgba(0, 0, 0, 0.6)" if st.session_state.theme == 'dark' else "rgba(255, 255, 255, 0.4)"
text_shadow = "2px 2px 4px #000000" if st.session_state.theme == 'dark' else "1px 1px 2px #FFFFFF"

st.markdown(f"""
    <style>
    /* Harakatlanuvchi Yer videosi */
    #bgVideo {{
        position: fixed; right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -1;
        object-fit: cover;
    }}
    .stApp {{
        background: {overlay_color};
    }}
    /* Matnlarni ko'rinishi */
    h1, h2, h3, p, .stMarkdown {{
        color: {"white" if st.session_state.theme == 'dark' else "black"} !important;
        text-shadow: {text_shadow};
    }}
    /* Boshqaruv paneli - Ideal Yashil */
    [data-testid="stSidebar"] {{
        background-color: #1E3932 !important;
        border-right: 1px solid #2D5A27;
    }}
    /* Footer */
    .footer {{
        position: fixed; right: 20px; bottom: 20px;
        color: white; font-weight: bold;
        background: rgba(0,0,0,0.6);
        padding: 5px 15px; border-radius: 10px; z-index: 1000;
    }}
    </style>

    <video autoplay muted loop playsinline id="bgVideo">
        <source src="https://cdn.pixabay.com/video/2023/10/20/185802-876735166_large.mp4" type="video/mp4">
    </video>
    <div class="footer">by Abdubositxo'ja</div>
    """, unsafe_allow_html=True)

# 4. SIDEBAR - FUNKSIYALAR
st.sidebar.title(t['sidebar'])

# Tillar
c1, c2, c3 = st.sidebar.columns(3)
if c1.button("UZ"): st.session_state.lang = 'UZ'; st.rerun()
if c2.button("RU"): st.session_state.lang = 'RU'; st.rerun()
if c3.button("EN"): st.session_state.lang = 'EN'; st.rerun()

st.sidebar.markdown("---")

# Tun/Kun tugmasi
theme_icon = "☀️" if st.session_state.theme == 'dark' else "🌙"
if st.sidebar.button(f"{theme_icon} {t['theme_btn']}"):
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
    st.rerun()

# Login
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    if st.sidebar.button(f"🔑 {t['login']}"):
        st.session_state['logged_in'] = True; st.rerun()
else:
    st.sidebar.success("✅ Online")
    if st.sidebar.button("Logout"): st.session_state['logged_in'] = False; st.rerun()

# 5. ASOSIY SAHIFA
st.title(t['title'])
if not st.session_state['logged_in']:
    st.warning("Iltimos, tizimga kiring / Пожалуйста, войдите / Please login")
else:
    st.info("AI Tizimi tayyor!")
