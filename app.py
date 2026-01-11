import streamlit as st
import google.generativeai as genai

# 1. SAHIFA KONFIGURATSIYASI
st.set_page_config(page_title="Eko-Risk AI Global", layout="wide")

# AI Sozlamasi
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.warning("AI kalitini Secrets bo'limiga qo'shing.")

# 2. DIZAYN (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #ffffff; }
    /* Menyu tugmasi dizayni */
    [data-testid="stPopover"] { position: fixed; top: 15px; left: 15px; z-index: 1000; }
    button[aria-haspopup="dialog"] { 
        background-color: #00ff41 !important; color: black !important;
        border-radius: 10px !important; font-weight: bold !important;
    }
    /* Yangiliklar bloki */
    .news-container {
        background: #111418; padding: 20px; border-radius: 15px;
        border: 1px solid #00ff41; height: 85vh; overflow-y: auto;
    }
    iframe { border-radius: 15px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# Session State boshqaruvi
if 'auth' not in st.session_state: st.session_state.auth = False
if 'active_news' not in st.session_state: st.session_state.active_news = None

# 3. KIRISH EKRANI
if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<div style='text-align:center; background:#111418; padding:40px; border-radius:20px; border:1px solid #00ff41;'>", unsafe_allow_html=True)
        st.title("🌍 Eko-Risk AI Portal")
        st.write("Davom etish uchun tizimga kiring")
        if st.button("🌐 Google Account orqali kirish", use_container_width=True):
            st.session_state.auth = True; st.rerun()
        if st.button("🔵 Facebook orqali kirish", use_container_width=True):
            st.session_state.auth = True; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# 4. ASOSIY INTERFEYS
else:
    # ☰ Menyu tugmasi
    with st.popover("☰"):
        if st.button("🗺 Global Xarita (Live)"): st.session_state.active_news = None
        st.markdown("---")
        st.write("🎓 **Loyiha Mualliflari:**")
        st.caption("Prof. Egamberdiyev Elmurod A.")
        st.caption("PhD Ataxo'jayev Abdubositxo'ja")
        if st.button("🚪 Chiqish"): st.session_state.auth = False; st.rerun()

    # Ekran taqsimoti
    left_col, right_col = st.columns([0.7, 0.3])

    with left_col:
        if st.session_state.active_news:
            # Yangilikni to'liq o'qish
            news = st.session_state.active_news
            st.button("⬅️ Xaritaga qaytish", on_click=lambda: st.session_state.__setitem__('active_news', None))
            st.header(news['title'])
            st.info(f"📅 Sana: {news['date']}")
            
            with st.spinner("AI tahlil qilmoqda..."):
                prompt = f"{news['title']} haqida risk analizi, tarixiy sabablar va takliflarni o'zbek tilida ilmiy tahlil qilib ber."
                response = model.generate_content(prompt)
                st.write(response.text)
            st.markdown("---")
            st.caption("Manba: NASA, JST va Sun'iy Intellekt tahlili.")
        else:
            # aqicn.org saytini ulab qo'yish
            st.subheader("🗺 Real-vaqtdagi Global Havo Monitoringi")
            # aqicn.org xaritasi uchun iframe
            st.components.v1.iframe("https://aqicn.org/map/world/", height=650, scrolling=True)

    with right_col:
        st.markdown('<div class="news-container">', unsafe_allow_html=True)
        st.subheader("📰 Yangiliklar")
        news_data = [
            {"date": "11.01.2026", "title": "O'zbekistonda yangi eko-qonunchilik"},
            {"date": "11.01.2026", "title": "Global isish: Rossiya muzliklari tahlili"},
            {"date": "10.01.2026", "title": "AI datchiklari havo sifatini bashorat qilmoqda"},
            {"date": "09.01.2026", "title": "Jahon okeani sathi ko'tarilishi bo'yicha hisobot"}
        ]
        
        for item in news_data:
            if st.button(f"📌 {item['date']}\n{item['title']}", key=item['title'], use_container_width=True):
                st.session_state.active_news = item
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
