import streamlit as st

# 1. Google Verification Metatag
st.markdown('<meta name="google-site-verification" content="maybg4-LdPKEKS8plcTQclxsDBM6XX8lGzOQIwbv0W8" />', unsafe_allow_html=True)

# 2. Oddiy interfeys
st.title("Eco-Portal Pro AI: Verification")
st.write("Google qidiruv tizimi tasdiqlashi kutilmoqda...")

# 3. Zaxira HTML tekshiruvi
if "google19952789cd1d86.html" in st.query_params:
    st.write("google-site-verification: google19952789cd1d86.html")
