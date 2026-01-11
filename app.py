import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_google_auth import Authenticate

# --- 1. SOZLAMALAR ---
# Google Cloud-dan olgan kalitlaringizni shu yerga qo'ying
CLIENT_ID = "SIZNING_CLIENT_ID"
CLIENT_SECRET = "SIZNING_CLIENT_SECRET"

st.set_page_config(page_title="Eko-Risk AI O'zbekiston", layout="wide")

# Google Auth sozlamasi
auth = Authenticate(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="https://eko-risk-ai-uz.streamlit.app",
    cookie_name="google_auth_cookie"
)

auth.check_authentification()

def main():
    user_info = st.session_state.get('user_info')
    
    # Sidebar: Foydalanuvchi va Chiqish
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2913/2913520.png", width=100)
    st.sidebar.success(f"Foydalanuvchi: {user_info.get('name')}")
    if st.sidebar.button("Tizimdan chiqish"):
        auth.logout()

    # --- 2. ASOSIY SAHIFA: DUNYO XARITASI VA ANALIZ ---
    st.title("🌍 Global Ekologik Risklar va AI Tahlili")
    
    tabs = st.tabs(["📊 Global Xarita", "🔬 AI Risk Analizi", "⚖️ Qonuniy Mezonlar"])

    with tabs[0]:
        st.subheader("Dunyo bo'yicha ekologik holat (Interaktiv)")
        # Namuna uchun dunyo davlatlari bo'yicha eko-ma'lumotlar
        df_map = pd.DataFrame({
            'Davlat': ['Uzbekistan', 'Brazil', 'China', 'USA', 'Germany', 'India'],
            'Eko_Risk': [75, 45, 85, 60, 30, 80], # Risk darajasi (0-100)
            'lat': [41.3, -14.2, 35.8, 37.0, 51.1, 20.5],
            'lon': [69.2, -51.9, 104.1, -95.7, 10.4, 78.9]
        })
        fig = px.scatter_geo(df_map, locations="Davlat", locationmode='country names',
                             color="Eko_Risk", hover_name="Davlat", 
                             size="Eko_Risk", projection="natural earth",
                             title="Global Eko-Risk Darajasi (AI bashorati)")
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        st.subheader("O'zbekiston hududlari bo'yicha tahlil")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Suv tanqisligi prognozi")
            chart_data = pd.DataFrame(np.random.randn(20, 2), columns=['Hozirgi', '2030-yil'])
            st.area_chart(chart_data)
        with col2:
            st.write("Havo ifloslanishi darajasi")
            st.bar_chart(np.random.randint(1, 100, 12))

    with tabs[2]:
        st.subheader("📜 Sayt foydalanish qonunlari va mezonlari")
        st.markdown("""
        ### 1. Ma'lumotlar daxlsizligi
        Ushbu platforma Google OAuth 2.0 protokoli orqali foydalanuvchilarni taniydi. 
        Biz foydalanuvchilarning parollarini saqlamaymiz.
        
        ### 2. Ekologik Ma'lumotlar Mezonlari
        * Saytda ko'rsatilgan tahlillar Ochiq ma'lumotlar portali va AI modellariga asoslangan.
        * Ma'lumotlardan faqat ilmiy va o'quv maqsadlarida foydalanish mumkin.
        
        ### 3. Foydalanuvchi mas'uliyati
        Platformadan foydalanishda O'zbekiston Respublikasining "Kiberxavfsizlik to'g'risida"gi 
        qonuni va xalqaro axborot xavfsizligi normalariga rioya qilinishi shart.
        """)
        st.info("Barcha huquqlar himoyalangan © 2026 | Abdubositxoja")

# --- 3. KIRISH EKRANI ---
if not st.session_state.get('connected'):
    st.markdown("<h1 style='text-align: center;'>🌿 Eko-Risk AI O'zbekiston</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&q=80&w=1000", use_container_width=True)
    st.warning("Diqqat! Saytning barcha imkoniyatlaridan foydalanish uchun xavfsiz login tizimi orqali kiring.")
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        auth.login()
else:
    main()
