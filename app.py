import streamlit as st
import google.generativeai as genai

# 1. SAHIFA SOZLAMASI
st.set_page_config(page_title="Eko-Portal AI", layout="wide")

# 2. AI MODELINI SOZLASH (Xatolikni yo'qotish uchun maxsus usul)
def get_ai_analysis(prompt):
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Rasmdagi 404 xatosini (image_3dd152.png) yo'qotish uchun 
        # eng barqaror model nomidan foydalanamiz
        model = genai.GenerativeModel('gemini-pro') 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI xatolik berdi. Iltimos, API kalitini tekshiring. Xato: {str(e)}"

# 3. SIDEBAR (BOSHQRUV VA MUALLIFLAR)
with st.sidebar:
    st.title("📌 Boshqaruv")
    # Siz aytganingizdek, xarita va AI uchun alohida tugmalar
    if st.button("🌡 Havo Sifati (Xarita)"):
        st.session_state.view = "map"
    if st.button("🤖 AI Risk Analizi"):
        st.session_state.view = "ai_analysis"
    
    st.markdown("---")
    st.write("🎓 **Loyiha mualliflari:**")
    st.caption("Prof. Egamberdiyev Elmurod A.")
    st.caption("PhD Ataxo'jayev Abdubositxo'ja")

# 4. ASOSIY QISM
if 'view' not in st.session_state: st.session_state.view = "news"
if 'active_news' not in st.session_state: st.session_state.active_news = None

col_main, col_news = st.columns([0.7, 0.3])

with col_main:
    # XARITA (TUGMA BOSILGANDA)
    if st.session_state.view == "map":
        st.header("🗺 Global Havo Sifati (Real-vaqt)")
        st.components.v1.iframe("https://aqicn.org/map/world/", height=650)
    
    # AI TAHLIL (TUGMA BOSILGANDA)
    elif st.session_state.view == "ai_analysis":
        st.header("🤖 AI Risk Analizi va Maqola")
        topic = st.text_area("Tahlil uchun ma'lumot kiriting:")
        if st.button("Maqola va grafik tayyorlash"):
            with st.spinner("AI tahlil qilmoqda..."):
                res = get_ai_analysis(f"{topic} haqida professional tahlil, maqola va grafik ko'rsatkichlar ber.")
                st.markdown(res)

    # YANGILIK MATNI
    elif st.session_state.active_news:
        news = st.session_state.active_news
        st.header(news['title'])
        st.write(news['text'])
        if st.button("⬅️ Orqaga"): st.session_state.active_news = None; st.rerun()

with col_news:
    st.subheader("📰 Yangiliklar")
    # Sodda yangiliklar (AI-siz)
    news_list = [
        {"title": "UNEP: Plastik hisoboti", "text": "Plastik ifloslanish darajasi ortib bormoqda..."},
        {"title": "NASA: Ozon qatlami", "text": "Ozon qatlamida ijobiy o'zgarishlar kuzatildi..."}
    ]
    for n in news_list:
        if st.button(n['title'], use_container_width=True):
            st.session_state.active_news = n
            st.session_state.view = "news_detail"
            st.rerun()
