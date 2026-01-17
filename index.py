import streamlit as st

# 1. GOOGLE SEARCH CONSOLE TASDIQLASH (METATAG)
# Bu kod Google botiga "Men egasiman" deb signal beradi
st.markdown('<meta name="google-site-verification" content="maybg4-LdPKEKS8plcTQclxsDBM6XX8lGzOQIwbv0W8" />', unsafe_allow_html=True)

# 2. ENG SODDA INTERFEYS (TEZ YUKLANISHI UCHUN)
st.set_page_config(page_title="Eco-Portal Pro AI", layout="centered")
st.title("🌐 Eco-Portal Pro AI: Global Monitoring")
st.success("Sayt Google tizimi tomonidan tekshirilmoqda...")
st.write("Tasdiqlash jarayoni tugagach, to'liq dizayn va AI funksiyalari qo'shiladi.")

# 3. ZAXIRA TASDIQLASH YO'LI
if "google19952789cd1d86.html" in st.query_params:
    st.write("google-site-verification: google19952789cd1d86.html")
