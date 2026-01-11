import streamlit as st

# Sahifa sozlamalari
st.set_page_config(page_title="Eko-Risk AI O'zbekiston", layout="wide")

# Google kalitlarini tekshirish (Secrets'dan oladi)
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]

# Oddiy va xatosiz login funksiyasi
def login_section():
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2913/2913520.png", width=100)
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        if st.sidebar.button("Google orqali kirish"):
            # Bu yerda simulyatsiya qilingan, haqiqiy ulanish Secrets orqali o'tadi
            st.session_state['logged_in'] = True
            st.rerun()
    else:
        st.sidebar.success("Xush kelibsiz!")
        if st.sidebar.button("Chiqish"):
            st.session_state['logged_in'] = False
            st.rerun()

# Login qismini chaqirish
login_section()

# Asosiy sahifa mazmuni
st.title("🌍 Global Ekologik Risklar va AI Tahlili")

if st.session_state.get('logged_in'):
    st.write("### Tizimga muvaffaqiyatli kirdingiz!")
    st.info("AI tahlillari va global xaritalar yuklanmoqda...")
    
    tabs = st.tabs(["📊 Global Xarita", "🔬 AI Risk Analizi", "⚖️ Qonuniy Mezonlar"])
    with tabs[0]:
        st.subheader("Dunyo bo'yicha ekologik holat")
        st.write("Interaktiv xarita bu yerda ko'rinadi.")
else:
    st.warning("Iltimos, tizimga kirish uchun chap tarafdagi tugmani bosing.")
