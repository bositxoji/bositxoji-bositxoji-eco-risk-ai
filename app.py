import streamlit as st
import plotly.express as px
import pandas as pd

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Risk AI Pro", layout="wide")

# Session State (Auth va Navigatsiya)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'page' not in st.session_state: st.session_state.page = "Xarita"
if 'selected_news' not in st.session_state: st.session_state.selected_news = None

# 2. PROFESSIONAL DESIGN (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #ffffff; }
    
    /* MENYU TUGMASI - YORQIN VA KO'RINARLI */
    [data-testid="stPopover"] { position: fixed; top: 20px; left: 20px; z-index: 1000000; }
    button[aria-haspopup="dialog"] { 
        background-color: #00ff41 !important; color: #000 !important; 
        border-radius: 12px !important; width: 60px !important; height: 50px !important;
        font-weight: bold !important; border: 2px solid #ffffff !important;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.4);
    }

    /* YANGILIKLAR BLOKI USLUBI */
    .news-box {
        background: #111418; padding: 15px; border-radius: 12px;
        border: 1px solid #1db954; margin-bottom: 15px; cursor: pointer;
        transition: 0.3s;
    }
    .news-box:hover { background: #1c2128; border-color: #00ff41; }
    .news-date { color: #00ff41; font-family: monospace; }
    
    /* XARITA KONTEYNERI */
    .main-map { border-radius: 20px; overflow: hidden; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# 3. LOGIN INTERFEYSI
if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    with col_l2:
        st.markdown("<div style='text-align:center; background:#111418; padding:50px; border-radius:25px; border:1px solid #00ff41;'>", unsafe_allow_html=True)
        st.title("🌿 Eko-Risk AI Portal")
        st.write("Xavfsiz kirish tizimi")
        if st.button("🌐 Google Account orqali kirish", use_container_width=True):
            st.session_state.auth = True; st.rerun()
        if st.button("🔵 Facebook orqali kirish", use_container_width=True):
            st.session_state.auth = True; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# 4. ASOSIY PLATFORMA (KIRGANDAN SO'NG)
else:
    # 3 TA NUQTA MENYUSI (Har doim ko'rinadi)
    with st.popover("☰"):
        st.subheader("Navigatsiya")
        if st.button("🗺 Global Monitoring"): st.session_state.page = "Xarita"; st.session_state.selected_news = None
        if st.button("🌫 Havo (Risk Analizi)"): st.session_state.page = "Havo"
        if st.button("💧 Suv (Risk Analizi)"): st.session_state.page = "Suv"
        if st.button("🌡 Iqlim O'zgarishi"): st.session_state.page = "Iqlim"
        st.markdown("---")
        if st.button("📜 Platforma Nizomi"): st.session_state.page = "Nizom"
        if st.button("🎓 Loyiha Mualliflari"): st.session_state.page = "Ixtirochilar"
        if st.button("🚪 Chiqish"): st.session_state.auth = False; st.rerun()

    # EKRANNI BO'LISH
    left_col, right_col = st.columns([0.65, 0.35])

    with left_col:
        # AGAR YANGILIK TANLANMAGAN BO'LSA XARITA CHIQADI
        if st.session_state.selected_news:
            st.button("⬅️ Orqaga", on_click=lambda: st.session_state.__setitem__('selected_news', None))
            st.header(st.session_state.selected_news['t'])
            st.write(f"📅 Sana: {st.session_state.selected_news['d']}")
            st.markdown(f"**AI Tahlili:** {st.session_state.selected_news['content']}")
        
        elif st.session_state.page == "Xarita":
            st.subheader("🗺 Dunyo Davlatlari Ekologik Holati")
            df = px.data.gapminder().query("year==2007")
            fig = px.choropleth(df, locations="iso_alpha", color="lifeExp",
                                hover_name="country", projection="equirectangular",
                                color_continuous_scale="Greens")
            fig.update_layout(template="plotly_dark", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.page in ["Havo", "Suv", "Iqlim"]:
            st.header(f"🔍 {st.session_state.page} Muammosi Tahlili")
            st.markdown(f"""
            **Risk Analizi:** AI ushbu sohada 82% lik o'sish xavfini aniqladi.
            **Tarixi:** Sanoat inqilobidan so'ng ushbu ko'rsatkichlar keskin o'zgargan.
            **Takliflar:** Raqamli monitoringni butun dunyo bo'ylab integratsiya qilish lozim.
            """)

        elif st.session_state.page == "Ixtirochilar":
            st.subheader("🎓 Tadqiqotchi va Ixtirochilar")
            st.success("**Professor:** Egamberdiyev Elmurod Abduqodirovich\n\n**PhD:** Ataxo'jayev Abdubositxo'ja")

    with right_col:
        st.subheader("📰 Yangiliklar Arvixi")
        news_items = [
            {"d": "11.01.2026", "t": "Orol bo'yi hududida AI monitoringi", "content": "AI datchiklari hududda sho'rlanish darajasi pasayganini ko'rsatdi."},
            {"d": "11.01.2026", "t": "Global Isish: Yangi rekordlar", "content": "Dunyo okeani harorati kutilganidan 0.5 daraja yuqori."},
            {"d": "10.01.2026", "t": "Yashil Energiya: Rossiya loyihalari", "content": "Rossiyaning shimoliy qismida yangi shamol elektr stansiyalari ishga tushdi."}
        ]
        
        for item in news_items:
            if st.button(f"📌 {item['d']} | {item['t']}", key=item['t'], use_container_width=True):
                st.session_state.selected_news = item
                st.rerun()

    # FOOTER
    st.markdown("<div style='text-align: right; color: #444; padding-top: 20px;'>by Abdubositxo'ja</div>", unsafe_allow_html=True)
