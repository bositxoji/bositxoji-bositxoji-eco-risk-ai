import streamlit as st
import google.generativeai as genai

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Risk Global AI", layout="wide")

# AI MODELINI SOZLASH (Eng barqaror modelni tanlaymiz)
def get_ai_response(prompt):
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # 'gemini-1.5-flash' o'rniga eng kuchli 'gemini-1.5-pro' ni ishlatamiz
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI tahlilida xatolik: {str(e)}. Iltimos, API kalitini tekshiring."

# 2. DIZAYN (Qora fon va yashil neon uslubi)
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #ffffff; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .news-card {
        background: #111418; padding: 15px; border-radius: 10px;
        border: 1px solid #00ff41; margin-bottom: 10px;
    }
    iframe { border-radius: 15px; border: 1px solid #30363d; background: white; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False
if 'active_news' not in st.session_state: st.session_state.active_news = None

# 3. ASOSIY QISM
if not st.session_state.auth:
    st.markdown("<br><br><div style='text-align:center;'><h1>🌍 Eko-Risk AI Portal</h1><p>Global Monitoring va Tahlil</p></div>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1, 1])
    with col:
        if st.button("🚀 Platformaga kirish", use_container_width=True):
            st.session_state.auth = True; st.rerun()
else:
    # ☰ MENYU (Chap tomonda)
    with st.sidebar:
        st.title("📌 Menyu")
        if st.button("🗺 aqicn.org Xaritasi"): st.session_state.active_news = None
        st.markdown("---")
        st.write("🎓 **Muallif:** PhD Ataxo'jayev A.")
        if st.button("🚪 Chiqish"): st.session_state.auth = False; st.rerun()

    left_col, right_col = st.columns([0.7, 0.3])

    with left_col:
        if st.session_state.active_news:
            news = st.session_state.active_news
            if st.button("⬅️ Xaritaga qaytish"):
                st.session_state.active_news = None
                st.rerun()
            
            st.header(news['title'])
            st.success(f"Manba: {news['source']} | Sana: {news['date']}")
            
            with st.spinner("AI tahlil qilmoqda (Gemini 1.5 Pro)..."):
                # AI tahlili shu yerda ishlaydi
                analysis = get_ai_response(f"{news['source']} tashkilotining '{news['title']}' xabari bo'yicha o'zbek tilida ilmiy tahlil bering.")
                st.markdown(analysis)
        else:
            st.subheader("🗺 Real-vaqtdagi Dunyo Havo Sifati (AQICN)")
            st.components.v1.iframe("https://aqicn.org/map/world/", height=750, scrolling=True)

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
