import streamlit as st

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Eko-Risk AI", layout="wide")

# 2. Session State - Barcha holatlarni tekshirish
if 'lang' not in st.session_state: st.session_state.lang = 'UZ'
if 'theme' not in st.session_state: st.session_state.theme = 'dark'
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# Matnlar lug'ati
content = {
    'UZ': {
        'title': "🌍 Global Ekologik Risklar va AI Tahlili",
        'login': "Kirish",
        'logout': "Chiqish",
        'theme_btn': "Mavzu",
        'about_btn': "Muallif haqida",
        'status': "✅ Tizim faol. Tahlil boshlashga tayyor.",
        'about_text': """Toshkent davlat texnika universiteti Texnika fanlari doktori, professor **Egamberdiyev Elmurod Abduqodirovich** boshchiligidagi jamoa ishladi. 
        
        Ushbu loyiha ustida Toshkent davlat texnika universiteti PhD tadqiqotchisi **Ataxo'jayev Abdubositxo'ja Abdulaxatxo'ja o'g'li** ilmiy izlanishlar olib bormoqda."""
    },
    'RU': {
        'title': "🌍 Глобальные эко-риски и ИИ анализ",
        'login': "Вход",
        'logout': "Выйти",
        'theme_btn': "Тема",
        'about_btn': "Об авторе",
        'status': "✅ Система активна. Готова к анализу.",
        'about_text': "Команда под руководством профессора Эгамбердиева Э.А. Исследователь: Атаходжаев А.А."
    }
}
t = content.get(st.session_state.lang, content['UZ'])

# 3. YASHIL EKO-DIZAYN (CSS)
overlay = "rgba(0, 0, 0, 0.7)" if st.session_state.theme == 'dark' else "rgba(255, 255, 255, 0.5)"
text_color = "white" if st.session_state.theme == 'dark' else "black"

st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient({overlay}, {overlay}), 
                          url("https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?q=80&w=2074&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    
    /* Yashil Popover Tugmasi */
    [data-testid="stPopover"] {{
        position: fixed; top: 20px; left: 20px; z-index: 999999;
    }}
    
    button[aria-haspopup="dialog"] {{
        background-color: #065f46 !important;
        color: white !important;
        border: 2px solid #10b981 !important;
        border-radius: 10px !important;
    }}

    h1, h2, h3, .stMarkdown {{
        color: {text_color} !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}
    
    .footer {{
        position: fixed; right: 20px; bottom: 20px;
        color: white; font-weight: bold; background: rgba(0,0,0,0.6);
        padding: 5px 15px; border-radius: 10px;
    }}
    [data-testid="stSidebar"] {{ display: none; }}
    </style>
    <div class="footer">by Abdubositxo'ja</div>
    """, unsafe_allow_html=True)

# 4. CHAP YASHIL MENYU
with st.popover("⋮"):
    st.write("### 🌐 Languages")
    c1, c2, c3 = st.columns(3)
    if c1.button("UZ"): st.session_state.lang = 'UZ'; st.rerun()
    if c2.button("RU"): st.session_state.lang = 'RU'; st.rerun()
    if c3.button("EN"): st.session_state.lang = 'EN'; st.rerun()
    
    st.markdown("---")
    if st.button(f"🎓 {t['about_btn']}"):
        st.info(t['about_text'])
        
    st.markdown("---")
    
    # Login/Logout Mantiqi
    col_a, col_b = st.columns(2)
    with col_a:
        theme_icon = "☀️" if st.session_state.theme == 'dark' else "🌙"
        if st.button(f"{theme_icon}"):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()
    with col_b:
        if not st.session_state.logged_in:
            if st.button("🔑"):
                st.session_state.logged_in = True
                st.rerun()
        else:
            if st.button("🚪"):
                st.session_state.logged_in = False
                st.rerun()

# 5. ASOSIY SAHIFA - DINAMIK O'ZGARISH
st.title(t['title'])

if st.session_state.logged_in:
    # BU YERDA SAYTNING ASOSIY BASHORAT QISMI BOSHLANADI
    st.success(t['status'])
    
    st.markdown("---")
    col_graph1, col_graph2 = st.columns(2)
    with col_graph1:
        st.subheader("📈 Ekologik o'zgarishlar")
        st.line_chart([10, 20, 15, 30, 25])
    with col_graph2:
        st.subheader("🌍 Havoning ifloslanishi")
        st.bar_chart([5, 12, 18, 10, 15])
else:
    # Kirish qilinmaganda faqat rasm va sarlavha turadi, ortiqcha yozuvlarsiz
    st.write("")
