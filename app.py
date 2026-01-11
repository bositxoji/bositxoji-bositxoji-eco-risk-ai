import streamlit as st
import google.generativeai as genai

# 1. SAHIFA SOZLAMASI
st.set_page_config(page_title="Eko-Portal", layout="wide")

# 2. AI MODELINI ULANISHI
# Secrets-dan kalitni olamiz
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API kaliti topilmadi. Secrets bo'limiga kalitni kiriting.")

# 3. INTERFEYS (SODDA USLUB)
st.title("🌍 Global Ekologik Monitoring")

# Ekran ikki qismga bo'linadi: Xarita va Yangiliklar
col1, col2 = st.columns([0.7, 0.3])

with col1:
    st.subheader("🗺 Jonli xarita (aqicn.org)")
    # aqicn.org xaritasi eng sodda va aniq monitoring vositasi
    st.components.v1.iframe("https://aqicn.org/map/world/", height=600)

with col2:
    st.subheader("📰 Xalqaro yangiliklar")
    
    # UNEP va boshqa tashkilotlar yangiliklari ro'yxati
    news_items = [
        {"org": "UNEP", "title": "Plastik ifloslanish bo'yicha hisobot"},
        {"org": "NASA", "title": "Ozon qatlamining tiklanishi"},
        {"org": "WHO", "title": "Havo sifati va salomatlik"},
        {"org": "WMO", "title": "Global harorat o'zgarishi"}
    ]

    for item in news_items:
        # Har bir yangilik alohida tugma sifatida
        if st.button(f"{item['org']}: {item['title']}", use_container_width=True):
            st.session_state.selected_news = item

# 4. AI TAHLILI (AGAR YANGILIK TANLANSA)
if "selected_news" in st.session_state and st.session_state.selected_news:
    st.divider()
    news = st.session_state.selected_news
    st.header(f"🤖 AI Tahlili: {news['title']}")
    
    with st.spinner("Tahlil qilinmoqda..."):
        try:
            prompt = f"{news['org']} tashkilotining '{news['title']}' mavzusidagi xabari bo'yicha o'zbek tilida qisqa ilmiy xulosa bering."
            response = model.generate_content(prompt)
            st.write(response.text)
        except Exception as e:
            st.error(f"Xatolik yuz berdi: {e}")
    
    if st.button("Tahlilni yopish"):
        st.session_state.selected_news = None
        st.rerun()

# 5. MUALLIFLAR
st.sidebar.markdown("---")
st.sidebar.write("🎓 **Loyiha mualliflari:**")
st.sidebar.caption("Prof. Egamberdiyev Elmurod A.")
st.sidebar.caption("PhD Ataxo'jayev Abdubositxo'ja")
