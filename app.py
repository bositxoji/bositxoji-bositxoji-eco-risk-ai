import streamlit as st
import pandas as pd
import numpy as np

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Eko-Risk AI", layout="wide")

# 2. Session State - Til va Mavzu
if 'lang' not in st.session_state: st.session_state.lang = 'UZ'
if 'theme' not in st.session_state: st.session_state.theme = 'dark'

content = {
    'UZ': {'title': "🌍 Global Ekologik Risklar va AI Tahlili", 'login': "Kirish", 'theme_btn': "Mavzu rejimi", 'welcome': "Xush kelibsiz"},
    'RU': {'title': "🌍 Глобальные эко-риски и ИИ анализ", 'login': "Вход", 'theme_btn': "Режим темы", 'welcome': "Добро пожаловать"},
    'EN': {'title': "🌍 Global Eco Risks & AI Analysis", 'login': "Login", 'theme_btn': "Theme mode", 'welcome': "Welcome"}
}
t = content[st.session_state.lang]

# 3. STATIK FON VA DIZAYN (CSS)
overlay = "rgba(0, 0, 0, 0.7)" if st.session_state.theme == 'dark' else "rgba(255, 255, 255, 0.4)"
text_color = "white" if st.session_state.theme == 'dark' else "black"

st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient({overlay}, {overlay}), 
                          url("https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?q=80&w=2074&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    h1, h2, h3, p, .stMarkdown {{
        color: {text_color} !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}
    .footer {{
        position: fixed; right: 20px; bottom: 20px;
        color: white; font-weight: bold;
        background: rgba(0,0,0,0.6);
        padding: 5px 15px; border-radius: 10px; z-index: 1000;
    }}
    /* Sidebar-ni yashirish (agar kerak bo'lsa) */
    [data-testid="stSidebar"] {{ display: none; }}
    </style>
    <div class="footer">by Abdubositxo'ja</div>
    """, unsafe_allow_html=True)

# 4. YUQORI MENYU (3 TA NUQTA O'RNIGA POPOVER)
col1, col2 = st.columns([0.9, 0.1])
with col2:
    # Streamlit-da 3 ta nuqta menyu vazifasini popover bajaradi
    with st.popover("⋮"):
        st.write("🌐 Languages")
        cl1, cl2, cl3 = st.columns(3)
        if cl1.button("UZ"): st.session_state.lang = 'UZ'; st.rerun()
        if cl2.button("RU"): st.session_state.lang = 'RU'; st.rerun()
        if cl3.button("EN"): st.session_state.lang = 'EN'; st.rerun()
        
        st.markdown("---")
        
        # Login
        if st.button(f"🔑 {t['login']}"):
            st.session_state['logged_in'] = True
            st.toast(t['welcome'])
        
        st.markdown("---")
        
        # Mavzu tugmasi menyu pastida
        theme_icon = "☀️" if st.session_state.theme == 'dark' else "🌙"
        if st.button(f"{theme_icon} {t['theme_btn']}"):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()

# 5. ASOSIY SAHIFA
st.title(t['title'])

if st.session_state.get('logged_in'):
    st.success(f"{t['welcome']}!")
    # AI qismlari shu yerda boshlanadi
else:
    st.info("Log in via the menu to see details.")
