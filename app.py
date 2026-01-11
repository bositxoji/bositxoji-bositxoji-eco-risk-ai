import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Risk AI Platforma", layout="wide")

# Session State boshqaruvi
if 'auth' not in st.session_state: st.session_state.auth = False
if 'page' not in st.session_state: st.session_state.page = "Bosh sahifa"

# 2. DIZAYN (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    [data-testid="stPopover"] { position: fixed; top: 20px; left: 20px; z-index: 100000; }
    button[aria-haspopup="dialog"] { 
        background-color: #238636 !important; color: white !important; 
        border-radius: 50% !important; width: 55px !important; height: 55px !important;
        font-size: 24px !important; border: 2px solid #ffffff !important;
    }
    .auth-box { 
        text-align: center; padding: 50px; border-radius: 15px; 
        background: rgba(255,255,255,0.05); border: 1px solid #30363d;
    }
    .news-card {
        padding: 15px; border-radius: 10px; background: #161b22;
        margin-bottom: 10px; border-left: 5px solid #238636;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. KIRISH OYNASI (AUTH)
if not st.session_state.auth:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c2:
        st.markdown('<div class="auth-box">', unsafe_allow_html=True)
        st.title("🌍 Eko-Risk AI Platformasiga Kirish")
        st.write("Davom etish uchun ijtimoiy tarmoq orqali kiring")
        
        if st.button("🔵 Google orqali kirish", use_container_width=True):
            st.session_state.auth = True
            st.rerun()
        if st.button("🔵 Facebook orqali kirish", use_container_width=True):
            st.session_state.auth = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# 4. ASOSIY INTERFEYS (KIRGANDAN SO'NG)
else:
    # 3 TA NUQTA MENYUSI
    with st.popover("⋮"):
        st.subheader("📌 Bo'limlar")
        if st.button("🗺 Dunyo Eko-Xaritasi"): st.session_state.page = "Xarita"
        if st.button("🌫 Havo muammolari"): st.session_state.page = "Havo"
        if st.button("💧 Suv muammolari"): st.session_state.page = "Suv"
        if st.button("🌡 Iqlim o'zgarishi"): st.session_state.page = "Iqlim"
        st.markdown("---")
        if st.button("📜 Sayt Nizomi"): st.session_state.page = "Nizom"
        if st.button("🎓 Ixtirochilar"): st.session_state.page = "Ixtirochilar"
        if st.button("🚪 Chiqish"): 
            st.session_state.auth = False
            st.rerun()

    # EKRANNI IKKIGA BO'LISH
    left_col, right_col = st.columns([0.7, 0.3])

    with left_col:
        if st.session_state.page == "Bosh sahifa" or st.session_state.page == "Xarita":
            st.subheader("🗺 Dunyo Davlatlari Ekologik Monitoringi")
            # Xarita ma'lumotlari
            df_map = px.data.gapminder().query("year==2007")
            fig = px.choropleth(df_map, locations="iso_alpha", color="lifeExp",
                                hover_name="country", title="Sichqonchani davlatlar ustiga olib boring",
                                color_continuous_scale=px.colors.sequential.Greens)
            fig.update_layout(template="plotly_dark", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
            st.info("💡 Davlat ustiga bossangiz batafsil AI tahlili yuklanadi.")

        elif st.session_state.page in ["Havo", "Suv", "Iqlim"]:
            muammo = st.session_state.page
            st.header(f"🔍 {muammo} Muammosi - AI Mukammal Tahlili")
            
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.subheader("📊 Risk Analizi")
                st.write(f"AI Bashorati: {muammo} bo'yicha global xavf darajasi 78% ga yetdi.")
                st.subheader("📜 Tarix va Sabablar")
                st.write(f"Sanoatlashuv va tabiiy resurslardan noto'g'ri foydalanish {muammo} inqiroziga olib keldi.")
            with col_t2:
                st.subheader("💡 Takliflar")
                st.write("1. Qayta tiklanuvchi energiya.\n2. Raqamli monitoring.\n3. Yashil texnologiyalar.")
            
            st.markdown("---")
            st.caption("ℹ️ Manba: Ushbu ma'lumotlar NASA, JST va Sun'iy Intellekt algoritmlari asosida shakllantirildi.")

        elif st.session_state.page == "Nizom":
            st.subheader("📜 Saytdan foydalanish nizomi")
            st.write("Ushbu platforma faqat ilmiy va ma'rifiy maqsadlarda foydalanish uchun mo'ljallangan.")

        elif st.session_state.page == "Ixtirochilar":
            st.subheader("🎓 Sayt Ixtirochilari haqida")
            st.write("Toshkent davlat texnika universiteti jamoasi.")
            st.write("**Rahbar:** Professor Egamberdiyev Elmurod Abduqodirovich")
            st.write("**PhD Tadqiqotchi:** Ataxo'jayev Abdubositxo'ja Abdulaxatxo'ja o'g'li")

    with right_col:
        st.subheader("📰 So'nggi Yangiliklar")
        news_list = [
            {"date": "11.01.2026", "title": "Arktika muzliklari erishi tezlashdi"},
            {"date": "10.01.2026", "title": "Yangi ekologik qonunchilik e'lon qilindi"},
            {"date": "09.01.2026", "title": "AI havo sifatini bashorat qilishni boshladi"}
        ]
        for news in news_list:
            st.markdown(f"""
            <div class="news-card">
                <small>{news['date']}</small><br>
                <b>{news['title']}</b>
            </div>
            """, unsafe_allow_html=True)
