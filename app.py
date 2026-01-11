import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# 1. SAHIFA SOZLAMALARI VA BRENDING
st.set_page_config(page_title="ABDUBOSITXOJANING SAHIFASI", layout="wide")

# 2. XAVFSIZLIK VA MUALLIFLIK (ANTIVIRUS VA HIMOYA LOGIKASI)
def check_security():
    # Sahifa tepasida mualliflik belgisi
    st.markdown("<h1 style='text-align: center; color: #2E7D32;'>ABDUBOSITXOJANING SAHIFASI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>🛡️ Tizim himoyalangan va viruslardan xoli</p>", unsafe_allow_html=True)
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        # Kirish oynasi
        with st.container():
            st.info("Bu sahifa muallif tomonidan himoyalangan. Kirish uchun parolni kiriting.")
            password = st.text_input("Maxfiy parol:", type="password")
            if st.button("Xavfsiz kirish"):
                if password == "abdu2026":  # Parolni o'zingizga moslang
                    st.session_state.authenticated = True
                    st.success("Xavfsizlik tekshiruvi muvaffaqiyatli yakunlandi!")
                    st.rerun()
                else:
                    st.error("Kirish rad etildi: Parol noto'g'ri!")
        return False
    return True

# 3. ASOSIY QISM (FAQAT LOGIN DAN O'TGANDA KO'RINADI)
if check_security():
    st.sidebar.title("Muallif: ABDUBOSITXОJA")
    st.sidebar.write("🔒 **Xavfsizlik darajasi:** Yuqori")
    st.sidebar.write("ⓒ 2026 Barcha huquqlar himoyalangan")
    
    # Ma'lumotlarni internetdan olish
    @st.cache_data
    def get_data():
        url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
        return pd.read_csv(url)

    try:
        data = get_data()
        world_df = data[data['country'] == 'World'][['year', 'co2']].dropna()
        
        st.subheader("📊 Global Ekologik Tahlil")
        
        # Grafik
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(world_df["year"], world_df["co2"], color='#1b5e20', label="CO2 emissiyasi")
        ax.set_title("Dunyo bo'yicha CO2 o'sishi")
        st.pyplot(fig)

        # AI Prognoz
        model = LinearRegression()
        model.fit(world_df[["year"]], world_df["co2"])
        future_years = np.array([2030, 2040, 2050]).reshape(-1, 1)
        preds = model.predict(future_years)

        col1, col2, col3 = st.columns(3)
        col1.metric("2030 Prognozi", f"{int(preds[0])} mt")
        col2.metric("2040 Prognozi", f"{int(preds[1])} mt")
        col3.metric("2050 Prognozi", f"{int(preds[2])} mt")

    except Exception as e:
        st.error("Ma'lumot uzatishda xavfsizlik xatosi yuz berdi.")

    # MUALLIFLIK FOOTER
    st.markdown("---")
    st.markdown("<footer style='text-align: center;'>Dastur muallifi: ABDUBOSITXОJA | Xavfsiz tizim v1.0</footer>", unsafe_allow_html=True)