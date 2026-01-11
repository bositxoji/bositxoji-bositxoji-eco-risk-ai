import streamlit as st
import plotly.express as px
import google.generativeai as genai

# 1. AI SOZLAMASI
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API kaliti topilmadi. Iltimos, Secrets-ga GOOGLE_API_KEY ni qo'shing.")

# 2. DIZAYN (Interaktiv xarita va menyu uchun)
st.set_page_config(page_title="Eko-Risk AI Global", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False
if 'page' not in st.session_state: st.session_state.page = "Xarita"

# 3. KIRISH (Google/Facebook simulyatsiyasi)
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>🌍 Global Eko-Monitoring AI</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1, 1])
    with col:
        if st.button("🔴 Google orqali kirish", use_container_width=True):
            st.session_state.auth = True; st.rerun()
        if st.button("🔵 Facebook orqali kirish", use_container_width=True):
            st.session_state.auth = True; st.rerun()
else:
    # MENYU TUGMASI (☰)
    with st.popover("☰"):
        if st.button("🗺 Dunyo xaritasi"): st.session_state.page = "Xarita"
        if st.button("🌫 Havo muammolari"): st.session_state.page = "Havo"
        if st.button("💧 Suv muammolari"): st.session_state.page = "Suv"
        if st.button("🌡 Iqlim o'zgarishi"): st.session_state.page = "Iqlim"
        st.markdown("---")
        if st.button("📜 Nizom"): st.session_state.page = "Nizom"
        if st.button("🎓 Ixtirochilar"): st.session_state.page = "Ixtirochilar"
        if st.button("🚪 Chiqish"): st.session_state.auth = False; st.rerun()

    # EKRAN TAQSIMOTI
    main_c, news_c = st.columns([0.7, 0.3])

    with main_c:
        if st.session_state.page == "Xarita":
            st.subheader("🗺 Global Ekologik Monitoring")
            df = px.data.gapminder().query("year==2007")
            fig = px.choropleth(df, locations="iso_alpha", color="lifeExp",
                                hover_name="country", projection="natural earth",
                                color_continuous_scale="Greens")
            fig.update_layout(template="plotly_dark", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.page in ["Havo", "Suv", "Iqlim"]:
            st.header(f"🔍 {st.session_state.page} bo'yicha AI Tahlili")
            with st.spinner("AI tahlil qilmoqda..."):
                try:
                    prompt = f"{st.session_state.page} muammosi haqida risk analizi, tarixi va yechimlari haqida o'zbek tilida professional ma'lumot ber."
                    response = model.generate_content(prompt)
                    st.write(response.text)
                except:
                    st.write("AI bilan bog'lanishda xatolik. Kalitni tekshiring.")

        elif st.session_state.page == "Ixtirochilar":
            st.info("Ixtirochilar: Prof. Egamberdiyev E.A. va PhD Ataxo'jayev A.")

    with news_c:
        st.subheader("📰 Yangiliklar")
        st.markdown("""
        <div style='background:#111; padding:10px; border-left:4px solid #00ff41; margin-bottom:10px;'>
        <small>11.01.2026</small><br><b>O'zbekistonda yangi havo datchiklari o'rnatildi</b></div>
        <div style='background:#111; padding:10px; border-left:4px solid #00ff41;'>
        <small>11.01.2026</small><br><b>Global iqlim sammiti natijalari</b></div>
        """, unsafe_allow_html=True)
