import streamlit as st
import google.generativeai as genai
from datetime import datetime
import pandas as pd

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Risk AI", layout="wide")

# AI ni sozlash (Sizning API kalitingizni bu yerda ishlating)
# genai.configure(api_key="SIZNING_GEMINI_API_KEY")

# 2. SESSION STATE
if 'lang' not in st.session_state: st.session_state.lang = 'UZ'
if 'theme' not in st.session_state: st.session_state.theme = 'dark'
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'news_archive' not in st.session_state: st.session_state.news_archive = []

# 3. DIZAYN (YASHIL MENYU VA EKO-FON)
overlay = "rgba(0, 0, 0, 0.75)" if st.session_state.theme == 'dark' else "rgba(255, 255, 255, 0.5)"
text_color = "white" if st.session_state.theme == 'dark' else "black"

st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient({overlay}, {overlay}), 
                          url("https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?q=80&w=2074&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    [data-testid="stPopover"] {{ position: fixed; top: 20px; left: 20px; z-index: 99999; }}
    button[aria-haspopup="dialog"] {{ background-color: #065f46 !important; color: white !important; border: 2px solid #10b981 !important; border-radius: 10px !important; }}
    h1, h2, h3, .stMarkdown {{ color: {text_color} !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }}
    .footer {{ position: fixed; right: 20px; bottom: 20px; color: white; font-weight: bold; background: rgba(0,0,0,0.6); padding: 5px 15px; border-radius: 10px; }}
    [data-testid="stSidebar"] {{ display: none; }}
    </style>
    <div class="footer">by Abdubositxo'ja</div>
    """, unsafe_allow_html=True)

# 4. CHAP YASHIL MENYU (YANGILANGAN)
with st.popover("⋮"):
    st.write("### 🌐 Menu")
    c1, c2, c3 = st.columns(3)
    if c1.button("UZ"): st.session_state.lang = 'UZ'; st.rerun()
    if c2.button("RU"): st.session_state.lang = 'RU'; st.rerun()
    if c3.button("EN"): st.session_state.lang = 'EN'; st.rerun()
    
    st.markdown("---")
    if st.button("🎓 Muallif haqida"):
        st.info("Professor Egamberdiyev E.A. boshchiligidagi jamoa. PhD tadqiqotchi: Ataxo'jayev Abdubositxo'ja.")
    
    if st.button("🔑 Login/Logout"):
        st.session_state.logged_in = not st.session_state.logged_in
        st.rerun()

# 5. ASOSIY SAHIFA - YANGILIKLAR VA AI TAHLILI
st.title("🌍 Eko-Risk AI: Global Monitoring")

if not st.session_state.logged_in:
    # BOSH SAHIFA: YANGILIKLAR (Hamma ko'ra oladi)
    st.subheader("📰 So'nggi Ekologik Yangiliklar (AI Monitoring)")
    
    # AI orqali olingan simulyatsiya yangiliklari (Haqiqiy API bo'lsa jonli keladi)
    news_col1, news_col2 = st.columns(2)
    with news_col1:
        st.success(f"📌 **{datetime.now().strftime('%H:%M')}** - Orol dengizi havzasida namlik darajasi o'zgarishi AI tahlili yakunlandi.")
        st.write("Yashil qoplamaning ko'payishi qum bo'ronlari xavfini 15% ga kamaytirdi.")
    with news_col2:
        st.warning(f"📌 **{datetime.now().strftime('%H:%M')}** - Toshkent havosidagi PM2.5 miqdori nazoratga olindi.")
        st.write("AI tahlili: Transport oqimini kamaytirish tavsiya etiladi.")
    
    st.info("Batafsil tahlil va Arxivga kirish uchun menyudan tizimga kiring.")

else:
    # ICHKI SAHIFA: KATTA MA'LUMOTLAR VA ARXIV
    tab1, tab2, tab3 = st.tabs(["📊 Havoning ifloslanishi", "🐾 Hayvonot olami", "📂 Arxiv & Maqolalar"])
    
    with tab1:
        st.subheader("🌫 Havodagi zaharli moddalar tasnifi")
        data = {
            'Modda': ['PM2.5', 'CO2', 'NO2', 'SO2'],
            'Daraja': [45, 410, 20, 15],
            'Tavsif': ['Kichik chang zarralari (xavfli)', 'Issiqxona gazi', 'Avtomobil chiqindisi', 'Sanoat gazi']
        }
        st.table(pd.DataFrame(data))
        st.write("AI Izohi: Hozirgi kunda PM2.5 darajasi me'yordan biroz yuqori.")
        
    with tab2:
        st.subheader("🦅 Atrof-muhit va Hayvonlar muhofazasi")
        st.write("""
        AI qidiruvi natijalari:
        * **Qizil kitob:** O'zbekistonda noyob turlarni saqlash bo'yicha yangi AI algoritmlari qo'llanilmoqda.
        * **Monitoring:** Toshkent viloyati tog'li hududlarida qor qoplonlari harakati sun'iy intellekt orqali kuzatilmoqda.
        """)
        
    with tab3:
        st.subheader("📚 Arxivlangan ma'lumotlar va ilmiy maqolalar")
        st.write("Bu yerda har 2 soatda internetdan to'plangan maqolalar saqlanadi.")
        if st.button("Arxivni yangilash (AI Search)"):
            st.toast("AI internetdan yangi ma'lumotlarni qidirmoqda...")
            st.session_state.news_archive.append(f"Maqola {datetime.now()}")
        
        for item in st.session_state.news_archive:
            st.write(f"📁 {item}")
