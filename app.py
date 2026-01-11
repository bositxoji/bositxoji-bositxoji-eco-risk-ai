import streamlit as st
import google.generativeai as genai

# 1. SAHIFA KONFIGURATSIYASI
st.set_page_config(page_title="Eko-Portal AI", layout="wide")

# AI MODELINI SOZLASH (Barqaror versiya)
def get_ai_analysis(prompt):
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Rasmdagi 404 xatosini oldini olish uchun eng so'nggi model
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI xatolik: {str(e)}. Iltimos, API kalitini tekshiring."

# 2. DIZAYN VA STIL
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; color: #1e1e1e; }
    .sidebar .sidebar-content { background: #ffffff; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    .news-card { background: white; padding: 15px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. YON PANEL (SIDEBAR) - MUALLIFLAR VA ASOSIY TUGMALAR
with st.sidebar:
    st.title("📌 Boshqaruv")
    
    # Havo sifati tugmasi
    if st.button("🌡 Havo Sifati (Xarita)"):
        st.session_state.view = "map"
        st.session_state.selected_news = None

    # AI Tahlil tugmasi
    if st.button("🤖 AI Risk Analizi"):
        st.session_state.view = "ai_analysis"

    st.markdown("---")
    st.write("🎓 **Loyiha mualliflari:**")
    st.caption("Prof. Egamberdiyev Elmurod A.")
    st.caption("PhD Ataxo'jayev Abdubositxo'ja")

# 4. SESSION STATE BOSHQARUVI
if 'view' not in st.session_state: st.session_state.view = "news"
if 'selected_news' not in st.session_state: st.session_state.selected_news = None

# 5. ASOSIY OYNA TAQSIMOTI
col_main, col_side = st.columns([0.7, 0.3])

with col_main:
    # XARITA OYNASI
    if st.session_state.view == "map":
        st.header("🗺 Global Havo Sifati Monitoringi")
        st.components.v1.iframe("https://aqicn.org/map/world/", height=700)
    
    # AI RISKI TAHLILI OYNASI
    elif st.session_state.view == "ai_analysis":
        st.header("🤖 Sun'iy Intellekt: Risk Analizi va Grafik Tahlil")
        topic = st.text_input("Tahlil uchun mavzu kiriting (masalan: Toshkentdagi chang bo'ronlari):")
        if st.button("Tahlilni tayyorlash"):
            with st.spinner("Gemini AI ma'lumotlarni tahlil qilib, maqola va grafik tayyorlamoqda..."):
                prompt = f"{topic} mavzusida ekologik risk analizi o'tkaz, tarixiy ma'lumotlar ber va natijalarni maqola ko'rinishida yoz. Shuningdek, matn ichida taxminiy ko'rsatkichlar uchun ASCII grafik yasab ber."
                result = get_ai_analysis(prompt)
                st.markdown(result)

    # YANGILIK MATNI OYNASI
    elif st.session_state.selected_news:
        news = st.session_state.selected_news
        st.header(news['title'])
        st.write(f"**Manba:** {news['org']} | **Sana:** {news['date']}")
        st.markdown("---")
        st.write(news['full_text'])
        if st.button("⬅️ Yangiliklarga qaytish"):
            st.session_state.selected_news = None
            st.rerun()

with col_side:
    st.subheader("📰 Yangiliklar")
    # Real yangiliklar matni bilan
    news_data = [
        {
            "org": "UNEP", "date": "11.01.2026", 
            "title": "Plastik ifloslanish bo'yicha hisobot",
            "full_text": "BMT Atrof-muhit dasturi (UNEP) dunyo okeanlaridagi plastik miqdori rekord darajaga yetganini ma'lum qildi. Hisobotda aytilishicha, 2030-yilga borib plastik chiqindilar ikki baravar ko'payishi mumkin..."
        },
        {
            "org": "NASA", "date": "11.01.2026", 
            "title": "Ozon qatlamining tiklanishi",
            "full_text": "NASA sun'iy yo'ldoshlari Antarktida ustidagi ozon teshigi kutilganidan tezroq yopilayotganini aniqladi. Bu global miqyosda zararli moddalar chiqarishni kamaytirish bo'yicha qilingan ishlarning natijasidir."
        }
    ]

    for item in news_data:
        if st.button(f"📌 {item['org']}: {item['title']}", key=item['title']):
            st.session_state.selected_news = item
            st.session_state.view = "news_detail"
            st.rerun()
