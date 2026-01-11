import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Eko-Risk AI Platforma", layout="wide")

# Session State - Arxiv va Kirish holati
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'lang' not in st.session_state: st.session_state.lang = 'UZ'
if 'archive' not in st.session_state: st.session_state.archive = []

# 2. DIZAYN (YASHIL EKO-USLUB)
st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                          url("https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?q=80&w=2074&auto=format&fit=crop");
        background-size: cover; background-attachment: fixed;
    }}
    [data-testid="stPopover"] {{ position: fixed; top: 20px; left: 20px; z-index: 99999; }}
    button[aria-haspopup="dialog"] {{ background-color: #065f46 !important; color: white !important; border: 2px solid #10b981 !important; border-radius: 10px !important; }}
    .footer {{ position: fixed; right: 20px; bottom: 20px; color: white; background: rgba(0,0,0,0.6); padding: 5px 15px; border-radius: 10px; }}
    </style>
    <div class="footer">by Abdubositxo'ja</div>
    """, unsafe_allow_html=True)

# 3. CHAP YASHIL MENYU
with st.popover("⋮"):
    st.write("🌐 Tilni tanlang")
    c1, c2, c3 = st.columns(3)
    if c1.button("UZ"): st.session_state.lang = 'UZ'; st.rerun()
    if c2.button("RU"): st.session_state.lang = 'RU'; st.rerun()
    if c3.button("EN"): st.session_state.lang = 'EN'; st.rerun()
    st.markdown("---")
    if st.button("🎓 Muallif haqida"):
        st.info("Professor Egamberdiyev E.A. boshchiligidagi jamoa. PhD tadqiqotchi: Ataxo'jayev Abdubositxo'ja.")
    if st.button("🔑 Kirish / Chiqish"):
        st.session_state.logged_in = not st.session_state.logged_in
        st.rerun()

# 4. ASOSIY OYNA - YANGILIKLAR (HAR 2 SOATDA YANGILANADI)
st.title("🌍 Global Ekologik Monitoring va AI")

# Yangiliklar simulyatsiyasi (AI orqali internetdan qidirish prototipi)
last_update = (datetime.now()).strftime("%H:00")
st.subheader(f"📰 So'nggi Yangiliklar (Oxirgi yangilanish: {last_update})")

news_data = [
    {"mavzu": "Havo ifloslanishi", "xabar": "Toshkentda PM2.5 darajasi AI nazoratida.", "vaqt": "1 soat oldin"},
    {"mavzu": "Atrof-muhit", "xabar": "Yangi ekologik filtrlar sanoat hududlariga o'rnatildi.", "vaqt": "2 soat oldin"}
]

for n in news_data:
    with st.expander(f"📌 {n['mavzu']} - {n['vaqt']}"):
        st.write(n['xabar'])

st.markdown("---")

# 5. KIRISH QILINGANDA OCHILADIGAN KATTA MA'LUMOTLAR
if st.session_state.logged_in:
    tab1, tab2, tab3 = st.tabs(["🌫 Havo Tahlili", "🐾 Hayvonot olami", "📂 Maqolalar Arvixi"])
    
    with tab1:
        st.subheader("🧪 Ifloslantiruvchi moddalar tasnifi")
        pollutants = pd.DataFrame({
            'Modda': ['PM2.5', 'CO2 (Karbonat angidrid)', 'NO2 (Azot dioksidi)', 'SO2 (Oltingugurt dioksidi)'],
            'Tasnif': ['Kichik chang zarralari, nafas yo\'llariga kiradi', 'Asosiy issiqxona gazi, haroratni oshiradi', 'Transport chiqindisi, o\'pka uchun zararli', 'Sanoat chiqindisi, kislotali yomg\'irga sababchi'],
            'Holat': ['⚠️ Yuqori', '✅ Me\'yorda', '🟡 O\'rtacha', '✅ Past']
        })
        st.table(pollutants)
        
    with tab2:
        st.subheader("🦁 Hayvonlar va Atrof-muhit Muhofazasi")
        st.write("AI Monitoringi: O'zbekiston hududidagi noyob turlar (Qoplon, Buxoro bug'usi) soni 3% ga oshgan.")
        st.image("https://images.unsplash.com/photo-1564349683136-77e08bef1ef1?q=80&w=2070&auto=format&fit=crop", caption="Tabiat muhofazasi AI nazoratida")
        
    with tab3:
        st.subheader("📚 Ilmiy Maqolalar va Ma'lumotlar Arvixi")
        if st.button("AI orqali yangi maqola qidirish"):
            new_art = f"Ekologik Tadqiqot #{len(st.session_state.archive)+1}: {datetime.now().date()}"
            st.session_state.archive.append(new_art)
        
        for art in st.session_state.archive:
            st.write(f"📄 {art}")
