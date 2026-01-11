import streamlit as st
import folium
from streamlit_folium import st_folium
import google.generativeai as genai

# 1. AI SOZLAMASI
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.warning("AI kaliti aniqlanmadi, iltimos Secrets bo'limini tekshiring.")

# 2. SAHIFA DIZAYNI
st.set_page_config(page_title="Eko-Risk Global Monitoring", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #ffffff; }
    .news-card {
        background: #111418; padding: 15px; border-radius: 10px;
        border-left: 5px solid #00ff41; margin-bottom: 10px; cursor: pointer;
    }
    .news-card:hover { background: #1c2128; }
    </style>
    """, unsafe_allow_html=True)

# 3. KIRISH TIZIMI
if 'auth' not in st.session_state: st.session_state.auth = False
if 'selected_news' not in st.session_state: st.session_state.selected_news = None

if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>🌍 Eko-Risk AI Portal</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1, 1])
    with col:
        if st.button("🔴 Google orqali kirish", use_container_width=True): st.session_state.auth = True; st.rerun()
        if st.button("🔵 Facebook orqali kirish", use_container_width=True): st.session_state.auth = True; st.rerun()
else:
    # MENYU (3 ta nuqta)
    with st.popover("☰"):
        if st.button("🗺 Asosiy Xarita"): st.session_state.selected_news = None
        st.markdown("---")
        st.write("Tadqiqotchi: Ataxo'jayev Abdubositxo'ja")

    # EKRAN TAQSIMOTI
    left_col, right_col = st.columns([0.7, 0.3])

    with left_col:
        if st.session_state.selected_news:
            # Yangilikni to'liq o'qish bo'limi
            news = st.session_state.selected_news
            st.button("⬅️ Xaritaga qaytish")
            st.header(news['title'])
            st.caption(f"Sana: {news['date']}")
            
            with st.spinner("AI tahlil qilmoqda..."):
                prompt = f"{news['title']} mavzusida batafsil ilmiy tahlil va takliflar ber."
                response = model.generate_content(prompt)
                st.write(response.text)
            st.markdown("---")
            st.caption("Manba: NASA va JST ma'lumotlari asosida AI tahlili.")
        else:
            # AQICN uslubidagi xarita
            st.subheader("🗺 Real-vaqtdagi Global Monitoring (AQI style)")
            
            # Xaritani yaratish (O'zbekiston markazda)
            m = folium.Map(location=[41.311081, 69.240562], zoom_start=3, tiles="CartoDB dark_matter")
            
            # Namuna sifatida nuqtalar (aqicn.org dagi kabi)
            locations = [
                {"loc": [41.31, 69.24], "name": "Toshkent", "aqi": 155, "color": "red"},
                {"loc": [55.75, 37.61], "name": "Moskva", "aqi": 42, "color": "green"},
                {"loc": [48.85, 2.35], "name": "Parij", "aqi": 68, "color": "yellow"},
                {"loc": [40.71, -74.00], "name": "Nyu-York", "aqi": 35, "color": "green"}
            ]
            
            for l in locations:
                folium.CircleMarker(
                    location=l['loc'],
                    radius=10,
                    popup=f"{l['name']}: AQI {l['aqi']}",
                    color=l['color'],
                    fill=True,
                    fill_color=l['color']
                ).add_to(m)
            
            st_folium(m, width="100%", height=500)
            st.info("💡 Nuqtalar ustiga bossangiz havo ko'rsatkichlari chiqadi.")

    with right_col:
        st.subheader("📰 Yangiliklar")
        news_list = [
            {"date": "11.01.2026", "title": "O'zbekistonda havo sifati pasayishi kutilmoqda"},
            {"date": "10.01.2026", "title": "Yevropada yangi yashil energiya qonuni"},
            {"date": "09.01.2026", "title": "Arktika muzliklarining AI datchiklari orqali tahlili"}
        ]
        
        for n in news_list:
            if st.button(f"📄 {n['date']}: {n['title']}", key=n['title'], use_container_width=True):
                st.session_state.selected_news = n
                st.rerun()
