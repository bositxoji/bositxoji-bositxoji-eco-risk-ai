import streamlit as st
from groq import Groq
from fpdf import FPDF
import pandas as pd

# 1. SAHIFA SOZLAMALARI VA TIL TANLASH
st.set_page_config(page_title="Eko-Portal AI 2.0", layout="wide")

# Til sozlamalari lug'ati
lang_dict = {
    "UZ": {"title": "Boshqaruv", "map_btn": "🌡 Havo Sifati", "ai_btn": "🤖 AI Risk Analizi", "upload": "Fayl yuklash (CSV/Excel)", "download": "PDF yuklab olish", "author": "Loyiha mualliflari"},
    "EN": {"title": "Navigation", "map_btn": "🌡 Air Quality", "ai_btn": "🤖 AI Risk Analysis", "upload": "Upload File (CSV/Excel)", "download": "Download PDF", "author": "Authors"},
    "RU": {"title": "Навигация", "map_btn": "🌡 Качество воздуха", "ai_btn": "🤖 ИИ Анализ рисков", "upload": "Загрузить файл (CSV/Excel)", "download": "Скачать PDF", "author": "Авторы"}
}

# Sidebar-da tilni tanlash
lang = st.sidebar.selectbox("🌐 Til / Language / Язык", ["UZ", "EN", "RU"])
t = lang_dict[lang]

# 2. AI FUNKSIYASI (Groq Llama 3)
def get_ai_analysis(prompt):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# 3. PDF YARATISH FUNKSIYASI
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# 4. SIDEBAR - TUGMALAR VA MUALLIFLAR
with st.sidebar:
    st.title(f"🚀 {t['title']}")
    if st.button(t['map_btn'], use_container_width=True):
        st.session_state.page = "map"
    if st.button(t['ai_btn'], use_container_width=True):
        st.session_state.page = "ai"
    
    st.markdown("---")
    st.write(f"🎓 **{t['author']}:**")
    st.caption("Prof. Egamberdiyev Elmurod A.")
    st.caption("PhD Ataxo'jayev Abdubositxo'ja")

# 5. ASOSIY OYNA
if 'page' not in st.session_state: st.session_state.page = "map"

# --- A. XARITA BO'LIMI ---
if st.session_state.page == "map":
    st.header(t['map_btn'])
    st.components.v1.iframe("https://aqicn.org/map/world/", height=750)

# --- B. AI RISK ANALIZI (FILE UPLOAD & PDF) ---
elif st.session_state.page == "ai":
    st.header(t['ai_btn'])
    
    # 1-TAKLIFF: Fayl yuklash
    uploaded_file = st.file_uploader(t['upload'], type=['csv', 'xlsx'])
    file_content = ""
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        st.write("Yuklangan ma'lumotlar:", df.head())
        file_content = f"\nYuklangan ma'lumotlar tahlili: {df.to_string()}"

    user_input = st.text_area("Mavzu:", height=150, placeholder="Tahlil uchun ma'lumot kiriting...")
    
    if st.button("Tahlilni tayyorlash", use_container_width=True):
        full_prompt = f"{user_input} {file_content} bo'yicha {lang} tilida ilmiy risk analizi va maqola tayyorla."
        with st.spinner("AI tahlil qilmoqda..."):
            st.session_state.ai_result = get_ai_analysis(full_prompt)
    
    if 'ai_result' in st.session_state:
        st.markdown("---")
        st.markdown(st.session_state.ai_result)
        
        # 2-TAKLIFF: PDF Eksport
        pdf_data = create_pdf(st.session_state.ai_result)
        st.download_button(label=f"📥 {t['download']}", data=pdf_data, file_name="eko_risk_report.pdf", mime="application/pdf")
