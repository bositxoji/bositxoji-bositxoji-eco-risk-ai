import streamlit as st
from groq import Groq

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Portal AI", layout="wide")

# 2. GROQ AI FUNKSIYASI (Llama 3 Model)
def get_ai_analysis(prompt):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI xatolik: {str(e)}"

# 3. YON PANEL (SIDEBAR) - TUGMALAR VA MUALLIFLAR
with st.sidebar:
    st.title("🚀 Boshqaruv")
    
    # Havo sifati tugmasi (Xaritani ichiga oladi)
    if st.button("🌡 Havo Sifati (Xarita)", use_container_width=True):
        st.session_state.page = "map"
        
    # AI Risk Analizi tugmasi (Gemini o'rniga Groq Llama ulanadi)
    if st.button("🤖 AI Risk Analizi", use_container_width=True):
        st.session_state.page = "ai"

    st.markdown("---")
    # Mualliflar siz aytgan joyda
    st.write("🎓 **Loyiha mualliflari:**")
    st.caption("Prof. Egamberdiyev Elmurod A.")
    st.caption("PhD Ataxo'jayev Abdubositxo'ja")

# 4. ASOSIY OYNA BOSHQARUVI
if 'page' not in st.session_state: st.session_state.page = "news"
if 'selected_news' not in st.session_state: st.session_state.selected_news = None

main_col, side_col = st.columns([0.7, 0.3])

with main_col:
    # A. XARITA BO'LIMI
    if st.session_state.page == "map":
        st.header("🗺 Global Havo Sifati (aqicn.org)")
        st.components.v1.iframe("https://aqicn.org/map/world/", height=700)
    
    # B. AI RISK ANALIZI (MAQOLA VA GRAFIK)
    elif st.session_state.page == "ai":
        st.header("🤖 AI Risk Analizi va Ilmiy Maqola")
        user_input = st.text_area("Tahlil uchun mavzuni kiriting (masalan: Orol dengizi muammosi):", height=150)
        if st.button("Tahlilni va maqolani tayyorlash"):
            with st.spinner("AI ma'lumotlarni tahlil qilmoqda..."):
                res = get_ai_analysis(f"{user_input} bo'yicha ekologik risk analizi, batafsil maqola va matnli grafik tayyorla.")
                st.markdown(res)

    # D. YANGILIKLARNI O'QISH
    elif st.session_state.selected_news:
        n = st.session_state.selected_news
        st.header(n['title'])
        st.write(f"**Manba:** {n['source']} | **Sana:** {n['date']}")
        st.divider()
        st.write(n['body'])
        if st.button("⬅️ Orqaga"):
            st.session_state.selected_news = None
            st.rerun()
    else:
        st.info("Xush kelibsiz! Chap menyudan bo'limni tanlang yoki yangilikni tanlang.")

with side_col:
    st.subheader("📰 Yangiliklar")
    news_list = [
        {"source": "UNEP", "date": "11.01.2026", "title": "Plastik ifloslanish", "body": "UNEP hisobotiga ko'ra, plastik miqdori okeanlarda oshmoqda..."},
        {"source": "NASA", "date": "11.01.2026", "title": "Ozon qatlami", "body": "NASA ozon teshigining kichrayishini tasdiqladi..."}
    ]
    for news in news_list:
        if st.button(f"📌 {news['source']}: {news['title']}", use_container_width=True):
            st.session_state.selected_news = news
            st.rerun()
