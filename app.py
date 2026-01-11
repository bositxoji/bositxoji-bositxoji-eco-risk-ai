import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from docx import Document
import PyPDF2
import json
import re

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Portal Academic AI", layout="wide")

# Til va terminologiya bazasi (Imloviy xatolarni oldini olish uchun)
lang_dict = {
    "UZ": {"title": "Boshqaruv", "map": "🌡 Havo Sifati", "ai": "🤖 Akademik Risk Analizi", "upload": "Hujjat yuklash", "btn": "Chuqur tahlilni boshlash"},
    "EN": {"title": "Navigation", "map": "🌡 Air Quality", "ai": "🤖 Academic Risk Analysis", "upload": "Upload Document", "btn": "Start Deep Analysis"},
    "RU": {"title": "Навигация", "map": "🌡 Качество воздуха", "ai": "🤖 Академический анализ рисков", "upload": "Загрузить документ", "btn": "Начать глубокий анализ"}
}

lang = st.sidebar.selectbox("🌐 Til / Language", ["UZ", "EN", "RU"])
t = lang_dict[lang]

# 2. AI FUNKSIYASI (Yuqori akademik daraja uchun)
def get_academic_analysis(prompt):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        # Llama 3-70b modeli akademik tahlil uchun eng kuchlisi
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Sen ekologiya sohasidagi PhD darajasidagi ilmiy xodimisan. Foydalanuvchi ma'lumotlarini {lang} tilida akademik uslubda, imloviy xatolarsiz tahlil qil. Javobingda maqola, tahliliy jadval va grafik uchun JSON ma'lumotlar bo'lsin."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3 # Aniqlikni oshirish uchun
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# 3. SIDEBAR
with st.sidebar:
    st.title(f"🚀 {t['title']}")
    page = st.radio("Bo'limlar:", [t['map'], t['ai']])
    st.markdown("---")
    st.write("🎓 **Mualliflar:**")
    st.caption("Prof. Egamberdiyev Elmurod A.")
    st.caption("PhD Ataxo'jayev Abdubositxo'ja")

# 4. ASOSIY QISM
if page == t['map']:
    st.header(t['map'])
    st.components.v1.iframe("https://aqicn.org/map/world/", height=800)

elif page == t['ai']:
    st.header(t['ai'])
    
    col1, col2 = st.columns([0.4, 0.6])
    
    with col1:
        st.subheader("📥 Ma'lumotlar manbai")
        uploaded_file = st.file_uploader(t['upload'], type=['csv', 'xlsx', 'docx', 'pdf'])
        user_context = st.text_area("Tahlil uchun qo'shimcha ilmiy kontekst yoki gipoteza:", height=150)
        
        start_analysis = st.button(t['btn'], use_container_width=True)

    with col2:
        if start_analysis:
            with st.spinner("AI akademik tahlil va grafiklar tayyorlamoqda..."):
                # Akademik prompt strukturasi
                academic_prompt = f"""
                Mavzu bo'yicha {lang} tilida 1000 ta so'zdan kam bo'lmagan ilmiy maqola yoz. 
                Tarkibi: 
                1. Annotatsiya. 
                2. Metodologiya. 
                3. Risk faktorlari tahlili. 
                4. SWOT tahlili (jadval ko'rinishida). 
                5. Kelajakdagi prognozlar.
                
                Muhim: Maqola oxirida '---DATA---' belgisidan keyin grafik chizish uchun quyidagi formatda JSON ma'lumot ber:
                {{"labels": ["A", "B", "C"], "values": [10, 20, 30], "title": "Risk darajasi"}}
                
                Kontekst: {user_context}
                """
                
                full_res = get_academic_analysis(academic_prompt)
                
                # Matn va JSONni ajratish
                if "---DATA---" in full_res:
                    parts = full_res.split("---DATA---")
                    st.markdown(parts[0]) # Maqola qismi
                    
                    try:
                        # Grafikni chizish
                        data_json = json.loads(parts[1].strip())
                        fig = px.bar(x=data_json['labels'], y=data_json['values'], title=data_json['title'], color=data_json['values'])
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Tahliliy jadval
                        st.subheader("📊 Raqamli ko'rsatkichlar tahlili")
                        st.table(pd.DataFrame({"Ko'rsatkich": data_json['labels'], "Qiymat": data_json['values']}))
                    except:
                        st.info("Grafik ma'lumotlarini yuklashda texnik cheklov.")
                else:
                    st.markdown(full_res)

# Footer
st.markdown("---")
st.center = st.caption("© 2026 Eko-Risk AI Academic Portal. Barcha huquqlar himoyalangan.")
