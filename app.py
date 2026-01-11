import streamlit as st

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Eko-Risk AI", layout="wide")

# 2. Session State - Til va Mavzu
if 'lang' not in st.session_state: st.session_state.lang = 'UZ'
if 'theme' not in st.session_state: st.session_state.theme = 'dark'

# Professor va jamoa haqida matnlar
about_text_uz = """
Toshkent davlat texnika universiteti Texnika fanlari doktori, professor **Egamberdiyev Elmurod Abduqodirovich** boshchiligidagi jamoa ishladi. 

Ushbu loyiha ustida Toshkent davlat texnika universiteti PhD tadqiqotchisi **Ataxo'jayev Abdubositxo'ja Abdulaxatxo'ja o'g'li** ilmiy izlanishlar olib bormoqda.
"""

content = {
    'UZ': {
        'title': "🌍 Global Ekologik Risklar va AI Tahlili",
        'login': "Kirish",
        'theme_btn': "Mavzu rejimi",
        'about_btn': "Muallif haqida",
        'about_text': about_text_uz
    },
    'RU': {
        'title': "🌍 Глобальные эко-риски и ИИ анализ",
        'login': "Вход",
        'theme_btn': "Режим темы",
        'about_btn': "Об авторе",
        'about_text': "Над проектом работала команда под руководством доктора технических наук, профессора ТГТУ Эгамбердиева Эльмурода Абдукодировича. Исследование проводит PhD исследователь Атаходжаев Абдубоситхожда."
    },
    'EN': {
        'title': "🌍 Global Eco Risks & AI Analysis",
        'login': "Login",
        'theme_btn': "Theme mode",
        'about_btn': "About Author",
        'about_text': "Team led by Professor Egamberdiyev Elmurod Abduqodirovich. Conducted by PhD researcher Atakhodjayev Abdubositkhoja."
    }
}
t = content[st.session_state.lang]

# 3. ZAMONAVIY EKO-DIZAYN (CSS)
overlay = "rgba(0, 0, 0, 0.7)" if st.session_state.theme == 'dark' else "rgba(255, 255, 255, 0.4)"
text_color = "white" if st.session_state.theme == 'dark' else "black"

st.markdown(f"""
    <style>
    /* Orqa fondagi statik Yer rasmi */
    .stApp {{
        background-image: linear-gradient({overlay}, {overlay}), 
                          url("https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?q=80&w=2074&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Tugmani chapga o'tkazish va EKO-Yashil qilish */
    [data-testid="stPopover"] {{
        position: fixed;
        top: 15px;
        left: 15px;
        z-index: 999999;
    }}
    
    button[aria-haspopup="dialog"] {{
        background-color: #065f46 !important; /* To'q eko yashil */
        color: white !important;
        border-radius: 8px !important;
        border: 1px solid #10b981 !important;
        font-size: 20px !important;
    }}

    h1, h2, h3, p, .stMarkdown {{
        color: {text_color} !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}
    
    .footer {{
        position: fixed; right: 20px; bottom: 20px;
        color: white; font-weight: bold;
        background: rgba(0,0,0,0.6);
        padding: 5px 15px; border-radius: 10px;
    }}
    
    /* Sidebar-ni butunlay yashirish */
    [data-testid="stSidebar"] {{ display: none; }}
    </style>
    <div class="footer">by Abdubositxo'ja</div>
    """, unsafe_allow_html=True)

# 4. CHAP YUQORI BURCHAKDAGI MENYU (⋮)
with st.popover("⋮"):
    st.write("### 🌐 Languages")
    c1, c2, c3 = st.columns(3)
    if c1.button("UZ"): st.session_state.lang = 'UZ'; st.rerun()
    if c2.button("RU"): st.session_state.lang = 'RU'; st.rerun()
    if c3.button("EN"): st.session_state.lang = 'EN'; st.rerun()
    
    st.markdown("---")
    
    # Muallif haqida (Professor va Jamoa ma'lumotlari bilan)
    if st.button(f"🎓 {t['about_btn']}"):
        st.info(t['about_text'])
        
    st.markdown("---")
    
    # Mavzu rejimi (Eng pastda)
    theme_icon = "☀️" if st.session_state.theme == 'dark' else "🌙"
    if st.button(f"{theme_icon} {t['theme_btn']}"):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()
        
    if st.button(f"🔑 {t['login']}"):
        st.session_state['logged_in'] = True
        st.toast("Muvaffaqiyatli kirildi!")

# 5. ASOSIY SAHIFA
st.title(t['title'])

if st.session_state.get('logged_in'):
    st.success("Platforma tahlil uchun tayyor.")
else:
    st.info("Chap yuqori burchakdagi yashil menyu orqali tizimga kiring.")
