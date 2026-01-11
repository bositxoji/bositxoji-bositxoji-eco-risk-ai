import streamlit as st
import pandas as pd
import numpy as np

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Eko-Risk AI O'zbekiston", layout="wide")

# 2. Tun va Kun funksiyasi uchun session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

def toggle_theme():
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'

# 3. DINAMIK DIZAYN (CSS)
# Orqa fonda harakatlanuvchi koinot videosi va ideal yashil sidebar
theme_style = {
    'dark': {
        'bg_overlay': 'rgba(0, 0, 0, 0.7)',
        'text_color': '#FFFFFF',
        'sidebar_bg': '#1E3932' # To'q, ammo chiroyli yashil (Starbucks yashili kabi)
    },
    'light': {
        'bg_overlay': 'rgba(255, 255, 255, 0.5)',
        'text_color': '#000000',
        'sidebar_bg': '#2D5A27' # Biroq yorqinroq yashil
    }
}

current = theme_style[st.session_state.theme]

st.markdown(f"""
    <style>
    /* Harakatlanuvchi video fon */
    #myVideo {{
        position: fixed;
        right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -1;
    }}

    .stApp {{
        background: {current['bg_overlay']};
    }}

    /* Sidebar dizayni - Siz so'ragan ideal yashil */
    [data-testid="stSidebar"] {{
        background-color: {current['sidebar_bg']} !important;
        border-right: 1px solid #4B5E52;
    }}

    /* Matn ranglari */
    h1, h2, h3, p, span, label {{
        color: {current['text_color']} !important;
    }}

    /* Footer - Abdubositxo'ja */
    .footer {{
        position: fixed;
        right: 20px;
        bottom: 20px;
        color: white;
        font-weight: bold;
        background: rgba(0,0,0,0.5);
        padding: 5px 15px;
        border-radius: 20px;
        z-index: 1000;
    }}
    </style>

    <video autoplay muted loop id="myVideo">
        <source src="https://v.ftcdn.net/02/91/52/35/700_F_291523533_V3Mv9RkSOfjP3X8A8wWc8Lp0Qz9B9F6l_ST.mp4" type="video/mp4">
    </video>

    <div class="footer">by Abdubositxo'ja</div>
    """, unsafe_allow_html=True)

# 4. Sidebar elementlari
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2913/2913520.png", width=80)
st.sidebar.title("Boshqaruv")

# Tun/Kun tugmasi
mode_icon = "☀️ Kun" if st.session_state.theme == 'dark' else "🌙 Tun"
if st.sidebar.button(mode_icon):
    toggle_theme()
    st.rerun()

# Login qismi
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    if st.sidebar.button("Google orqali kirish"):
        st.session_state['logged_in'] = True
        st.rerun()
else:
    st.sidebar.success("✅ Tizim faol")
    if st.sidebar.button("Chiqish"):
        st.session_state['logged_in'] = False
        st.rerun()

# 5. Asosiy sahifa
st.title("🌍 Global Ekologik Risklar va AI Tahlili")

if st.session_state['logged_in']:
    st.write(f"### Hozirgi rejim: {st.session_state.theme.upper()}")
    t1, t2 = st.tabs(["📊 Statistika", "🔬 AI Bashorat"])
    with t1:
        st.bar_chart(np.random.randn(10, 3))
    with t2:
        st.line_chart(np.random.randn(10, 2))
else:
    st.warning("⚠️ Kirish uchun chap paneldagi tugmani bosing.")
