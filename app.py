import streamlit as st
import pandas as pd
from groq import Groq

# 1. GOOGLE UCHUN ENG ISHONCHLI QISM (GTM)
# Siz yuborgan koddagi haqiqiy GTM ID: GTM-52GRQSL
gtm_code = """
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-52GRQSL');</script>
"""
st.markdown(gtm_code, unsafe_allow_html=True)

# 2. SAYT KONFIGURATSIYASI
st.set_page_config(page_title="Eco-Portal Pro AI", page_icon="🌍", layout="wide")

# Google verification uchun zaxira (Metatag)
st.markdown('<meta name="google-site-verification" content="maybg4-LdPKEKS8plcTQclxsDBM6XX8lGzOQIwbv0W8" />', unsafe_allow_html=True)

# API SOZLAMASI
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("GROQ_API_KEY topilmadi!")
    st.stop()

# 3. INTERFEYS
st.title("🌱 Eco-Portal Pro AI")
st.write("Google Search Console tasdiqlash rejimi faollashtirildi.")

# Xarita (Sizda ishlagan qism)
st.components.v1.iframe("https://aqicn.org/map/world/", height=700)
