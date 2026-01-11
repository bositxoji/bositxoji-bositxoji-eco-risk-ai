import streamlit as st
from streamlit_google_auth import Authenticate

# Sozlamalar
st.set_page_config(page_title="Eko-Risk AI O'zbekiston", layout="wide")

# Google Auth - Yangi versiya formati
auth = Authenticate(
    client_id=st.secrets["CLIENT_ID"],
    client_secret=st.secrets["CLIENT_SECRET"],
    redirect_uri="https://eko-risk-ai-uz.streamlit.app",
    cookie_name="google_auth_cookie",
    cookie_key="ixtiyoriy_matn_123", # secret_key o'rniga cookie_key ishlatiladi
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

# Asosiy qism
st.title("🌍 Global Ekologik Risklar va AI Tahlili")
st.write("Tizimga muvaffaqiyatli kirdingiz!")
