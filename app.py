import streamlit as st
import pandas as pd
import numpy as np

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Eko-Risk AI O'zbekiston", layout="wide")

# 2. ORQA FON VA MUALLIF YOZUG'I UCHUN CSS
st.markdown(
    """
    <style>
    /* Orqa fonga Yer rasmini qo'yish */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                    url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* O'ng pastki burchakka muallif yozuvi */
    .footer {
        position: fixed;
        right: 10px;
        bottom: 10px;
        color: white;
        font-family: sans-serif;
        font-size: 14px;
        font-weight: bold;
        background-color: rgba(0, 0, 0, 0.5);
        padding: 5px 10px;
        border-radius: 5px;
        z-index: 1000;
    }

    /* Matnlarni oq rangga o'tkazish (ko'rinishi uchun) */
    h1, h2, h3, p, .stMarkdown {
        color: white !important;
    }
    </style>
    <div class="footer">by Abdubositxo'ja</div>
    """,
    unsafe_allow_html=True
)

# 3. Login holati
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 4. Sidebar
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2913/2913520.png", width=80)
st.sidebar.title("Boshqaruv")

if not st.session_state['logged_in']:
    if st.sidebar.button("Google orqali kirish"):
        st.session_state['logged_in'] = True
        st.rerun()
else:
    st.sidebar.success("✅ Kirildi")
    if st.sidebar.button("Chiqish"):
        st.session_state['logged_in'] = False
        st.rerun()

# 5. Asosiy mazmun
st.title("🌍 Global Ekologik Risklar va AI Tahlili")

if st.session_state['logged_in']:
    st.write("### Xush kelibsiz! Ma'lumotlar yuklandi.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Statistik ko'rsatkich")
        st.bar_chart(np.random.randn(10, 2))
    with col2:
        st.subheader("🔬 AI Analiz")
        st.line_chart(np.random.randn(10, 2))
else:
    st.warning("Iltimos, tizimga kirish uchun chap paneldagi tugmani bosing.")
