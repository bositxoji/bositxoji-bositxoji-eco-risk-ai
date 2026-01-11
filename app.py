import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

# 1. Sahifa konfiguratsiyasi
st.set_page_config(page_title="Eko-Risk AI Global", layout="wide")

# Session State (Foydalanuvchi holati)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'page' not in st.session_state: st.session_state.page = "Xarita"
if 'active_news' not in st.session_state: st.session_state.active_news = None

# 2. Login Ekran (Google & Facebook)
if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 1.5, 1])
    with col_mid:
        st.markdown("<div style='text-align:center; padding:40px; border:2px solid #00ff41; border-radius:20px; background:#111418;'>", unsafe_allow_html=True)
        st.title("🌍 Eko-Risk AI Platforma")
        st.write("Xush kelibsiz! Davom etish uchun tizimga kiring:")
        if st.button("🔴 Google orqali kirish", use_container_width=True):
            st.session_state.auth = True; st.rerun()
        if st.button("🔵 Facebook orqali kirish", use_container_width=True):
            st.session_state.auth = True; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# 3. Asosiy Interfeys
else:
    # Chap yuqoridagi ☰ Menyu
    with st.popover("☰"):
        st.subheader("Navigatsiya")
        if st.button("🗺 Butun dunyo xaritasi"): st.session_state.page = "Xarita"; st.session_state.active_news = None
        if st.button("🌫 Havo muammosi"): st.session_state.page = "Havo"
        if st.button("💧 Suv muammosi"): st.session_state.page = "Suv"
        if st.button("🌡 Iqlim o'zgarishi"): st.session_state.page = "Iqlim"
        st.markdown("---")
        if st.button("📜 Sayt Nizomi"): st.session_state.page = "Nizom"
        if st.button("🎓 Ixtirochilar"): st.session_state.page = "Ixtirochilar"
        if st.button("🚪 Chiqish"): st.session_state.auth = False; st.rerun()

    # Ekran taqsimoti: 70% Kontent | 30% Yangiliklar
    col_main, col_news = st.columns([0.7, 0.3])

    with col_main:
        # Yangilik tanlangan bo'lsa uni ko'rsatish
        if st.session_state.active_news:
            st.button("⬅️ Xaritaga qaytish", on_click=lambda: st.session_state.__setitem__('active_news', None))
            st.header(st.session_state.active_news['title'])
            st.info(f"📅 {st.session_state.active_news['date']} holatiga AI Tahlili")
            st.write(st.session_state.active_news['full_text'])
            st.caption("Manba: NASA va Global Climate Monitoring AI")
        
        # Bo'limlarni ko'rsatish
        elif st.session_state.page == "Xarita":
            st.subheader("🗺 Global Ekologik Monitoring (2D)")
            df = px.data.gapminder().query("year==2007")
            fig = px.choropleth(df, locations="iso_alpha", color="lifeExp",
                                hover_name="country", projection="natural earth",
                                color_continuous_scale="Greens")
            fig.update_layout(template="plotly_dark", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.page in ["Havo", "Suv", "Iqlim"]:
            st.header(f"🔍 {st.session_state.page} tahlili")
            st.markdown("""
            ### 📊 Risk Analizi
            AI ushbu sohada xavf darajasini **75%** deb baholadi. 
            ### 📜 Tarix va Sabablar
            Asosiy sabab - texnologik chiqindilar va noto'g'ri utilizatsiya.
            ### 💡 Takliflar
            Yashil texnologiyalarni 2030-yilgacha 40% ga oshirish lozim.
            """)

        elif st.session_state.page == "Ixtirochilar":
            st.subheader("🎓 Sayt Ixtirochilari")
            st.write("Professor: **Egamberdiyev Elmurod Abduqodirovich**")
            st.write("PhD Tadqiqotchi: **Ataxo'jayev Abdubositxo'ja**")

    with col_news:
        st.subheader("📰 Yangiliklar")
        news_db = [
            {"date": "11.01.2026", "title": "O'zbekistonda havo tozaligi", "full_text": "AI tahlili: Toshkentda havo sifati me'yorga qaytmoqda..."},
            {"date": "10.01.2026", "title": "Rossiyada muzliklar monitoringi", "full_text": "Arktika yaqinida harorat 0.2 darajaga ko'tarilgani AI orqali aniqlandi..."},
            {"date": "09.01.2026", "title": "Zilzila bashorati: Yaponiya", "full_text": "Seysmik datchiklar Tinch okeanida faollik oshganini ko'rsatmoqda..."}
        ]
        for n in news_db:
            if st.button(f"📌 {n['date']}\n{n['title']}", key=n['title'], use_container_width=True):
                st.session_state.active_news = n
                st.rerun()

    st.markdown("<div style='position: fixed; bottom: 10px; right: 20px; color: #444;'>by Abdubositxo'ja</div>", unsafe_allow_html=True)
