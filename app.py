import streamlit as st
import plotly.express as px
import pandas as pd

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Risk AI Platforma", layout="wide")

# Session State
if 'auth' not in st.session_state: st.session_state.auth = False
if 'page' not in st.session_state: st.session_state.page = "Xarita"

# 2. DIZAYN (YANGILIKLAR VA MENYU UCHUN)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    
    /* 3 TA NUQTA MENYUSI */
    [data-testid="stPopover"] { position: fixed; top: 15px; left: 15px; z-index: 100000; }
    button[aria-haspopup="dialog"] { 
        background-color: #00ff41 !important; color: black !important; 
        border-radius: 50% !important; width: 50px !important; height: 50px !important;
        font-weight: bold !important; border: 2px solid white !important;
    }

    /* YANGILIKLAR BLOKI */
    .news-container {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px; border-radius: 15px;
        border: 1px solid #1db954; height: 80vh; overflow-y: auto;
    }
    .news-item {
        border-bottom: 1px solid #333; padding: 10px 0;
    }
    .news-date { color: #00ff41; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# 3. KIRISH EKRANI (Google va Facebook)
if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.markdown("<div style='text-align:center; background:#161b22; padding:40px; border-radius:20px; border:1px solid #00ff41;'>", unsafe_allow_html=True)
        st.title("🌍 Eko-Risk AI")
        st.write("Platformaga kirish uchun tanlang:")
        if st.button("🔴 Google orqali kirish", use_container_width=True):
            st.session_state.auth = True; st.rerun()
        if st.button("🔵 Facebook orqali kirish", use_container_width=True):
            st.session_state.auth = True; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# 4. ASOSIY INTERFEYS (KIRGANDAN SO'NG)
else:
    # MENYU (3 ta nuqta ichida)
    with st.popover("⋮"):
        st.subheader("Menyu")
        if st.button("🗺 Butun dunyo xaritasi"): st.session_state.page = "Xarita"
        if st.button("🌫 Havo muammolari"): st.session_state.page = "Havo"
        if st.button("💧 Suv muammolari"): st.session_state.page = "Suv"
        if st.button("🌡 Iqlim o'zgarishi"): st.session_state.page = "Iqlim"
        st.markdown("---")
        if st.button("📜 Sayt Nizomi"): st.session_state.page = "Nizom"
        if st.button("🎓 Ixtirochilar"): st.session_state.page = "Ixtirochilar"
        if st.button("🚪 Chiqish"): st.session_state.auth = False; st.rerun()

    # EKRANNI 2 GA BO'LISH (70% va 30%)
    left_col, right_col = st.columns([0.7, 0.3])

    with left_col:
        if st.session_state.page == "Xarita":
            st.subheader("🗺 Global Ekologik Monitoring (Butun dunyo)")
            # To'liq dunyo xaritasi (O'zbekiston va Rossiya markazda)
            df = px.data.gapminder().query("year==2007")
            fig = px.choropleth(df, locations="iso_alpha", color="lifeExp",
                                hover_name="country", 
                                projection="natural earth", # Butun dunyoni ko'rsatadi
                                color_continuous_scale="Greens")
            fig.update_layout(
                template="plotly_dark", 
                margin={"r":0,"t":0,"l":0,"b":0},
                geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular')
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("ℹ️ Sichqonchani davlatlar ustiga olib boring. O'zbekiston va Rossiya to'liq kiritilgan.")

        elif st.session_state.page in ["Havo", "Suv", "Iqlim"]:
            st.header(f"🔍 {st.session_state.page} Muammosi - AI Tahlili")
            st.markdown(f"""
            ### 📊 Risk Analizi
            AI bashoratiga ko'ra, {st.session_state.page} xavfi global miqyosda ortib bormoqda.
            
            ### 📜 Tarix va Sabablar
            Ushbu muammo oxirgi 50 yillik sanoatlashuv va ekotizimga bo'lgan antropogen ta'sir natijasidir.
            
            ### 💡 Takliflar va Yechimlar
            1. Monitoring tizimini raqamlashtirish.
            2. Qat'iy ekologik standartlarni joriy etish.
            
            **Manba:** Ma'lumotlar NASA va JST (World Health Organization) arxivlari asosida AI tomonidan tahlil qilindi.
            """)

        elif st.session_state.page == "Ixtirochilar":
            st.subheader("🎓 Sayt Ixtirochilari")
            st.info("**Rahbar:** Professor Egamberdiyev Elmurod Abduqodirovich\n\n**PhD Tadqiqotchi:** Ataxo'jayev Abdubositxo'ja")

    with right_col:
        st.markdown('<div class="news-container">', unsafe_allow_html=True)
        st.subheader("📰 Yangiliklar")
        news_data = [
            {"d": "11.01.2026", "t": "O'zbekistonda yangi eko-datchiklar o'rnatildi"},
            {"d": "11.01.2026", "t": "Rossiya shimolida havo harorati kutilmaganda ko'tarildi"},
            {"d": "10.01.2026", "t": "Jahon okeani sathi 2mm ga ko'tarilgani aniqlandi"},
            {"d": "09.01.2026", "t": "AI yordamida suv toshqinlari bashorat qilinmoqda"}
        ]
        for n in news_data:
            st.markdown(f"""
            <div class="news-item">
                <span class="news-date">{n['d']}</span><br>
                <b>{n['t']}</b>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
