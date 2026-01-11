import streamlit as st
import google.generativeai as genai

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Risk Global AI", layout="wide")

# AI MODELINI SOZLASH (Xatolikni oldini olish uchun)
def get_ai_response(prompt):
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Eng barqaror model nomini ishlatamiz
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI tahlilida xatolik yuz berdi. Iltimos, API kalitini tekshiring. Xato: {str(e)}"

# 2. DIZAYN (AQICN va UNEP uslubida)
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #ffffff; }
    [data-testid="stPopover"] { position: fixed; top: 15px; left: 15px; z-index: 1000; }
    .news-card {
        background: #111418; padding: 15px; border-radius: 12px;
        border-left: 5px solid #00ff41; margin-bottom: 12px;
    }
    iframe { border-radius: 15px; border: 1px solid #30363d; background: white; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False
if 'active_news' not in st.session_state: st.session_state.active_news = None

# 3. KIRISH TIZIMI
if not st.session_state.auth:
    st.markdown("<br><br><div style='text-align:center;'><h1>🌍 Eko-Risk AI</h1><p>Xalqaro Monitoring Portali</p></div>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1, 1])
    with col:
        if st.button("🌐 Kirish", use_container_width=True):
            st.session_state.auth = True; st.rerun()
else:
    # ☰ MENYU
    with st.popover("☰"):
        if st.button("🗺 aqicn.org Xaritasi"): st.session_state.active_news = None
        st.write("---")
        st.caption("PhD Ataxo'jayev A.")

    left_col, right_col = st.columns([0.7, 0.3])

    with left_col:
        if st.session_state.active_news:
            news = st.session_state.active_news
            st.button("⬅️ Xaritaga qaytish", on_click=lambda: st.session_state.__setitem__('active_news', None))
            st.header(news['title'])
            st.success(f"Manba: {news['source']} | Sana: {news['date']}")
            
            with st.spinner("AI xalqaro hisobotni o'zbek tiliga o'girmoqda va tahlil qilmoqda..."):
                analysis = get_ai_response(f"{news['source']} tashkilotining '{news['title']}' xabari bo'yicha ilmiy tahlil va O'zbekiston uchun tavsiyalar ber.")
                st.markdown(analysis)
        else:
            st.subheader("🗺 Real-vaqtdagi Dunyo Havo Sifati (AQICN)")
            # aqicn.org xaritasi integratsiyasi
            st.components.v1.iframe("https://aqicn.org/map/world/", height=700, scrolling=True)

    with right_col:
        st.subheader("🌐 Global Xabarlar")
        news_items = [
            {"source": "UNEP", "date": "11.01.2026", "title": "Global plastik ifloslanishiga qarshi yangi pakt"},
            {"source": "NASA", "date": "11.01.2026", "title": "Ozon qatlamidagi ijobiy o'zgarishlar monitoringi"},
            {"source": "WMO", "date": "10.01.2026", "title": "Muzliklar erishi: Yangi xalqaro hisobot"},
            {"source": "WHO", "date": "09.01.2026", "title": "Havo ifloslanishining salomatlikka ta'siri"}
        ]
        
        for item in news_items:
            with st.container():
                st.markdown(f"**{item['source']}** - {item['date']}")
                if st.button(item['title'], key=item['title'], use_container_width=True):
                    st.session_state.active_news = item
                    st.rerun()
