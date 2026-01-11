import streamlit as st
from streamlit_echarts import st_echarts

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Eko-Risk Global AI", layout="wide")

# Session State
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'lang' not in st.session_state: st.session_state.lang = 'UZ'

# 2. DIZAYN (YASHIL NEON VA QORA FON)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* 3 TA NUQTA MENYUSI - HAR DOIM KO'RINARLI */
    [data-testid="stPopover"] {
        position: fixed; top: 20px; left: 20px; z-index: 1000000;
    }
    button[aria-haspopup="dialog"] {
        background-color: #10b981 !important; /* Zumrad yashil */
        color: white !important;
        border-radius: 50% !important;
        width: 60px !important; height: 60px !important;
        font-size: 25px !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 0 15px #10b981;
    }
    h1 { color: #10b981 !important; text-align: center; font-family: 'Arial'; }
    .footer { position: fixed; right: 20px; bottom: 20px; color: #10b981; font-weight: bold; }
    </style>
    <div class="footer">by Abdubositxo'ja</div>
    """, unsafe_allow_html=True)

# 3. CHAP YASHIL MENYU (3 TA NUQTA)
with st.popover("⋮"):
    st.subheader("Boshqaruv Paneli")
    st.session_state.lang = st.selectbox("Tilni tanlang", ["UZ", "RU", "EN"])
    st.markdown("---")
    if st.button("🎓 Muallif haqida"):
        st.info("Professor Egamberdiyev E.A. va PhD Ataxo'jayev Abdubositxo'ja")
    if st.button("🔑 Kirish / Chiqish"):
        st.session_state.logged_in = not st.session_state.logged_in
        st.rerun()

st.title("🌍 Global Eko-Monitoring AI Platformasi")

# 4. INTERAKTIV 3D GLOBUS (ECHarts)
# Bu globusda davlatlar chegaralari bilan ko'rinadi
options = {
    "backgroundColor": "#000",
    "globe": {
        "baseTexture": "https://echarts.apache.org/examples/data-gl/asset/earth.jpg",
        "heightTexture": "https://echarts.apache.org/examples/data-gl/asset/bathymetry_bw_composite.jpg",
        "displacementScale": 0.1,
        "shading": "lambert",
        "environment": "https://echarts.apache.org/examples/data-gl/asset/starfield.jpg",
        "light": {
            "main": {"intensity": 1.5, "shadow": True},
            "ambient": {"intensity": 0.3}
        },
        "viewControl": {"autoRotate": True, "autoRotateAfterStill": 3}
    },
    "visualMap": {
        "show": False,
        "min": 0,
        "max": 100,
        "inRange": {"color": ["#10b981", "#fbbf24", "#ef4444"]}
    },
    "series": [{
        "type": "scatter3D",
        "coordinateSystem": "globe",
        "symbolSize": 10,
        "label": {"show": True, "formatter": "{b}"},
        "itemStyle": {"color": "#10b981"},
        "data": [
            {"name": "Uzbekistan: 22°C, Xavf: Past", "value": [69.24, 41.29, 50]},
            {"name": "Japan: 15°C, Zilzila: 4.2", "value": [139.69, 35.68, 50]},
            {"name": "USA: 10°C, Xavf: O'rta", "value": [-74.00, 40.71, 50]},
            {"name": "Brazil: 30°C, Namlik: Yuqori", "value": [-47.88, -15.79, 50]}
        ]
    }]
}

st_echarts(options=options, height="600px")

# 5. MA'LUMOTLAR BO'LIMI
if st.session_state.logged_in:
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.success("📊 **Ekologik Bashorat (AI)**")
        st.write("Dunyodagi o'rtacha harorat ko'tarilishi: +0.02°C (bugun)")
    with col2:
        st.warning("⚠️ **Favqulodda Holatlar**")
        st.write("Tinch okeani mintaqasida seysmik faollik oshgan.")
else:
    st.markdown("<h3 style='text-align: center;'>Batafsil tahlil uchun menyudan tizimga kiring</h3>", unsafe_allow_html=True)
