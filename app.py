import streamlit as st

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Eko-Risk AI", layout="wide")

# 2. Session State - Til va Mavzu
if 'lang' not in st.session_state: st.session_state.lang = 'UZ'
if 'theme' not in st.session_state: st.session_state.theme = 'dark'

content = {
    'UZ': {
        'title': "🌍 Global Ekologik Risklar va AI Tahlili",
        'login': "Kirish",
        'theme_btn': "Mavzu rejimi",
        'about_btn': "Muallif haqida",
        'about_text': """Toshkent davlat texnika universiteti Texnika fanlari doktori, professor **Egamberdiyev Elmurod Abduqodirovich** boshchiligidagi jamoa ishladi. 
        
        Ushbu loyiha ustida Toshkent davlat texnika universiteti PhD tadqiqotchisi **Ataxo'jayev Abdubositxo'ja Abdulaxatxo'ja o'g'li** ilmiy izlanishlar olib bormoqda."""
    },
    'RU': {
        'title': "🌍 Глобальные эко-риски и ИИ анализ",
        'login': "Вход",
        'theme_btn': "Режим темы",
        'about_btn': "Об авторе",
        'about_text': "Над проектом работала команда под руководством доктора технических наук, профессора Ташкентского государственного технического университета **Эгамбердиева Эльмурода Абдукодировича**. Исследование проводит PhD исследователь ТГТУ **Атаходжаев Абдубоситходжа Абдулахатходжа угли**."
    },
    'EN': {
        'title': "🌍 Global Eco Risks & AI Analysis",
        'login': "Login",
        'theme_btn': "Theme mode",
        'about_btn': "About Author",
        'about_text': "The team led by Doctor of Technical Sciences, Professor of Tashkent State Technical University **Egamberdiyev Elmurod Abduqodirovich** worked on this project. Research is conducted by TSTU PhD researcher **Atakhodjayev Abdubositkhoja Abdulakhatkhoja ugli**."
    }
}
t = content[st.session_state.lang]

# 3. EKO-DIZAYN (CSS)
overlay = "rgba(0, 0, 0, 0.7)" if st.session_state.theme == 'dark' else "rgba(255, 255, 255, 0.4)"
text_color = "white" if st.session_state.theme == 'dark' else "black"

st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient({overlay}, {overlay}), 
                          url("https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?q=80&w=2074&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    /* Zamonaviy Eko-Yashil Popover */
    button[aria-haspopup="dialog"] {{
        background-color: #10B981 !important; /* Zamonaviy Emerald Green */
        color: white !important;
        border-radius: 50% !important;
        width: 45px !important; height: 45px !important;
        border: 2px solid #059669 !important;
    }}
    h1, h2, h3, p, .stMarkdown {{
        color: {text_color} !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}
    .footer {{
        position: fixed; right: 20px; bottom: 20px;
        color: white; font-weight: bold; background: rgba(0,0,0,0.6);
        padding: 5px 15px; border-radius: 10px; z-index: 1000;
    }}
    [data-testid="stSidebar"] {{ display: none; }}
    </style>
    <div class="footer">by Abdubositxo'ja</div>
    """, unsafe_allow_html=True)

# 4. CHAP YUQORI BUNCHAKDAGI MENYU
col1, col2 = st.columns([0.1, 0.9])
with col1:
    with st.popover("⋮"):
        st.write("🌐 Languages")
        cl1, cl2, cl3 = st.columns(3)
        if cl1.button("UZ"): st.session_state.lang = 'UZ'; st.rerun()
        if cl2.button("RU"): st.session_state.lang = 'RU'; st.rerun()
        if cl3.button("EN"): st.session_state.lang = 'EN'; st.rerun()
        
        st.markdown("---")
        
        # Muallif haqida tugmasi
        if st.button(f"🎓 {t['about_btn']}"):
            st.info(t['about_text'])
            
        st.markdown("---")
        
        # Mavzu va Login
        theme_icon = "☀️" if st.session_state.theme == 'dark' else "🌙"
        if st.button(f"{theme_icon} {t['theme_btn']}"):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()
            
        if st.button(f"🔑 {t['login']}"):
            st.session_state['logged_in'] = True
            st.rerun()

# 5. ASOSIY SAHIFA
st.title(t['title'])

if st.session_state.get('logged_in'):
    st.success("Tizim faol!")
else:
    st.info("Log in via the Emerald menu (top-left) to see details.")
