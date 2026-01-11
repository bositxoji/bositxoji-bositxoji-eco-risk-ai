import streamlit as st
from streamlit_google_auth import Authenticate

st.set_page_config(page_title="Eko-Risk AI O'zbekiston", layout="wide")

# YANGI FORMAT: client_id o'rniga faqat secrets orqali ulanadi
auth = Authenticate(
    cookie_name="google_auth_cookie",
    cookie_key="ixtiyoriy_matn_123", # Bu sirli so'z
    redirect_uri="https://eko-risk-ai-uz.streamlit.app",
)

# Login tekshiruvi
auth.check_authenticity()

# Sidebar
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2913/2913520.png", width=100)

if st.session_state.get('connected'):
    st.sidebar.success(f"Xush kelibsiz!")
    if st.sidebar.button("Chiqish"):
        auth.logout()
else:
    auth.login()

st.title("🌍 Global Ekologik Risklar va AI Tahlili")
