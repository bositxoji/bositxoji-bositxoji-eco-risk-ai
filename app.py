import streamlit as st
from groq import Groq

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Portal AI", layout="wide")

# 2. GROQ AI FUNKSIYASI (Siz bergan gsk_... kaliti bilan ishlaydi)
def get_ai_analysis(prompt):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI xatolik: {str(e)}"

# 3. YON PANEL (SIDEBAR) - FAQAT TUGMALAR VA MUALLIFLAR
with st.sidebar:
    st.title("🚀 Boshqaruv")
    
    # Havo sifati tugmasi
    if st.button("🌡 Havo Sifati (Xarita)", use_container_width=True):
        st.session_state.page = "map"
        
    # AI Risk Analizi tugmasi
    if st.button("🤖 AI Risk Analizi", use_container_width=True):
        st.session_state.page = "ai"

    st.markdown("---")
    # Mualliflar bo'limi
    st.write("🎓 **Loyiha mualliflari:**")
    st.caption("Prof. Egamberdiyev Elmurod A.")
    st.caption("PhD Ataxo'jayev Abdubositxo'ja")

# 4. ASOSIY OYNA LOGIKASI
if 'page' not in st.session_state: st.session_state.page = "map" # Sayt xarita bilan ochiladi

# A. XARITA BO'LIMI
if st.session_state.page == "map":
    st.header("🗺 Global Havo Sifati Monitoringi (Real-vaqt)")
    # aqicn.org xaritasi butun ekranni egallaydi
    st.components.v1.iframe("https://aqicn.org/map/world/", height=800)

# B. AI RISK ANALIZI BO'LIMI
elif st.session_state.page == "ai":
    st.header("🤖 Sun'iy Intellekt: Risk Analizi va Maqola")
    st.write("Mavzu yoki ekologik ma'lumotlarni kiriting, AI sizga tahliliy maqola va grafik ko'rinishida natija beradi.")
    
    user_input = st.text_area("Tahlil uchun ma'lumot kiriting:", height=200, placeholder="Masalan: Orol bo'yi hududidagi chang miqdori tahlili...")
    
    if st.button("Tahlilni va maqolani tayyorlash", use_container_width=True):
        if user_input:
            with st.spinner("Llama 3 AI ma'lumotlarni tahlil qilmoqda..."):
                # Professional tahlil uchun buyruq
                prompt = f"{user_input} bo'yicha ekologik risk analizi o'tkaz, batafsil maqola yoz va raqamli ko'rsatkichlarni matnli grafik (ASCII) ko'rinishida bayon qil."
                res = get_ai_analysis(prompt)
                st.markdown("---")
                st.markdown(res)
        else:
            st.warning("Iltimos, tahlil uchun ma'lumot kiriting.")

st.markdown("---")
st.caption("Eko-Risk AI Global Monitoring Portali | 2026")
