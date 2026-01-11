import streamlit as st
from groq import Groq
from fpdf import FPDF
import pandas as pd
from docx import Document
import PyPDF2
import io

# 1. SAHIFA SOZLAMALARI VA TIL
st.set_page_config(page_title="Eko-Portal AI 2.1", layout="wide")

lang_dict = {
    "UZ": {"title": "Boshqaruv", "map_btn": "🌡 Havo Sifati", "ai_btn": "🤖 AI Risk Analizi", "upload": "Faylni tanlang (CSV, Excel, Word, PDF)", "download": "PDF hisobotni yuklash", "author": "Loyiha mualliflari"},
    "EN": {"title": "Navigation", "map_btn": "🌡 Air Quality", "ai_btn": "🤖 AI Risk Analysis", "upload": "Select File (CSV, Excel, Word, PDF)", "download": "Download PDF Report", "author": "Authors"},
    "RU": {"title": "Навигация", "map_btn": "🌡 Качество воздуха", "ai_btn": "🤖 ИИ Анализ рисков", "upload": "Выберите файл (CSV, Excel, Word, PDF)", "download": "Скачать PDF отчет", "author": "Авторы"}
}

lang = st.sidebar.selectbox("🌐 Til", ["UZ", "EN", "RU"])
t = lang_dict[lang]

# 2. FAYLLARDAN MATNNI O'QISH FUNKSIYALARI
def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# 3. AI FUNKSIYASI (Groq - Llama 3)
def get_ai_analysis(prompt):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"

# 4. SIDEBAR
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

# 5. ASOSIY QISM
if 'page' not in st.session_state: st.session_state.page = "map"

if st.session_state.page == "map":
    st.header(t['map_btn'])
    st.components.v1.iframe("https://aqicn.org/map/world/", height=750)

elif st.session_state.page == "ai":
    st.header(t['ai_btn'])
    
    # Fayl yuklash bo'limi yangilandi
    uploaded_file = st.file_uploader(t['upload'], type=['csv', 'xlsx', 'docx', 'pdf'])
    file_content = ""

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.docx'):
                file_content = read_docx(uploaded_file)
                st.success("Word fayl yuklandi")
            elif uploaded_file.name.endswith('.pdf'):
                file_content = read_pdf(uploaded_file)
                st.success("PDF fayl yuklandi")
            elif uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                file_content = df.to_string()
                st.dataframe(df.head())
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                file_content = df.to_string()
                st.dataframe(df.head())
        except Exception as e:
            st.error(f"Faylni o'qishda xatolik: {e}")

    user_input = st.text_area("Qo'shimcha izoh yoki mavzu:", height=100)
    
    if st.button("Tahlilni va maqolani tayyorlash", use_container_width=True):
        if user_input or file_content:
            with st.spinner("AI barcha ma'lumotlarni umumlashtirib tahlil qilmoqda..."):
                full_prompt = f"Quyidagi ma'lumotlar va mavzu bo'yicha {lang} tilida professional ekologik risk analizi va maqola tayyorla: \nMavzu: {user_input} \nFayl ma'lumotlari: {file_content[:5000]}" # 5000 belgi limit
                st.session_state.ai_result = get_ai_analysis(full_prompt)
        else:
            st.warning("Iltimos, ma'lumot kiriting yoki fayl yuklang.")
    
    if 'ai_result' in st.session_state:
        st.markdown("---")
        st.markdown(st.session_state.ai_result)
        
        # PDF yuklab olish (Natijani)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=st.session_state.ai_result.encode('latin-1', 'replace').decode('latin-1'))
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button(label=t['download'], data=pdf_output, file_name="eko_report.pdf", mime="application/pdf")
