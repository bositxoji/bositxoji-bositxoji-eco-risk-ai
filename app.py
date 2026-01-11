import streamlit as st
import google.generativeai as genai

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Risk AI Global", layout="wide")

# AI Konfiguratsiyasi
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.warning("AI kaliti topilmadi. Iltimos, Secrets-ni tekshiring.")

# 2. DIZAYN (UNEP va aqicn.org uslubida)
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #ffffff; }
    [data-testid="stPopover"] { position: fixed; top: 15px; left: 15px; z-index: 1000; }
    button[aria-haspopup="dialog"] { 
        background-color: #00ff41 !important; color: black !important;
        border-radius: 10px !important; font-weight: bold !important;
    }
    .news-container {
        background: #111418; padding: 20px; border-radius: 15px;
        border: 1px solid #00df61; height: 85vh; overflow-y: auto;
    }
    .source-tag {
        font-size: 10px; background: #00df61; color: black;
        padding: 2px 6px; border-radius: 4px; font-weight: bold;
    }
    iframe { border-radius: 15px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False
if 'active_news' not in st.session_state: st.session_state.active_news = None

# 3. KIRISH EKRANI
if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<div style='text-align:center; background:#111418; padding:40px; border-radius:20px; border:1px solid #00ff41;'>", unsafe_allow_html=True)
        st.title("🌍 Eko-Risk AI Portal")
        st.write("Xalqaro Ekologik Monitoring Tizimi")
        if st.button("🌐 Google Account orqali kirish", use_container_width=True):
            st.session_state.auth = True; st.rerun()
        if st.button("🔵 Facebook orqali kirish", use_container_width=True):
            st.session_state.auth = True; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# 4. ASOSIY INTERFEYS
else:
    # ☰ Menyu
    with st.popover("☰"):
        if st.button("🗺 Global Xarita (Live)"): st.session_state.active_news = None
        st.markdown("---")
        st.write("🎓 **Loyiha Mualliflari:**")
        st.caption("Prof. Egamberdiyev Elmurod A.")
        st.caption("PhD Ataxo'jayev Abdubositxo'ja")
        if st.button("📜 Platforma Nizomi"): st.info("Sayt nizomi ilmiy tahlil va ochiq ma'lumotlar qoidalariga asoslangan.")
        if st.button("🚪 Chiqish"): st.session_state.auth = False; st.rerun()

    left_col, right_col = st.columns([0.7, 0.3])

    with left_col:
        if st.session_state.active_news:
            news = st.session_state.active_news
            st.button("⬅️ Xaritaga qaytish", on_click=lambda: st.session_state.__setitem__('active_news', None))
            st.header(news['title'])
            st.markdown(f"<span class='source-tag'>{news['source']}</span> 📅 {news['date']}", unsafe_allow_html=True)
            
            with st.spinner("AI xalqaro hisobotni tahlil qilmoqda..."):
                prompt = f"Ushbu xalqaro yangilik bo'yicha ({news['title']}) risk analizi, tarixiy sabablar va mintaqaviy takliflarni ilmiy tahlil qilib ber."
                response = model.generate_content(prompt)
                st.markdown(f"### 🤖 AI Tahlili\n{response.text}")
            st.markdown("---")
            st.caption(f"Ma'lumotlar {news['source']} rasmiy manbalari asosida taqdim etildi.")
        else:
            # aqicn.org xaritasi
            st.subheader("🗺 Dunyo Havo Sifati (Real-Vaqt)")
            st.components.v1.iframe("https://aqicn.org/map/world/", height=650, scrolling=True)

    with right_col:
        st.markdown('<div class="news-container">', unsafe_allow_html=True)
        st.subheader("🌐 Global Xabarlar")
        
        # Xalqaro Eko saytlar xabarlari (Simulyatsiya)
        news_data = [
            {"source": "UNEP", "date": "11.01.2026", "title": "Global plastik ifloslanishiga qarshi yangi pakt"},
            {"source": "WMO", "date": "11.01.2026", "title": "2025-yil tarixdagi eng issiq yil deb topildi"},
            {"source": "IPCC", "date": "10.01.2026", "title": "Metan emissiyasini kamaytirish bo'yicha yangi hisobot"},
            {"source": "GREENPEACE", "date": "10.01.2026", "title": "Okean ekotizimlarini himoya qilish loyihasi"},
            {"source": "NASA", "date": "09.01.2026", "title": "Amazonka o'rmonlari qisqarishi monitoringi"}
        ]
        
        for item in news_data:
            if st.button(f"🌐 {item['source']}: {item['title']}", key=item['title'], use_container_width=True):
                st.session_state.active_news = item
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
