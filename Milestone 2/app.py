import streamlit as st
from prompt_builder import build_prompt
from model_api import query_model

# Page Config
st.set_page_config(page_title="PERSONALIZED FITPLAN", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=2070");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    h1, h2, h3, label, p, span, .stMarkdown {
        color: #FFFFFF !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stTextInput>div>div>input, 
    .stNumberInput>div>div>input, 
    .stSelectbox>div>div>div {
        background-color: #111111 !important;
        color: #00FF00 !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        height: 55px !important;
        border-radius: 8px !important;
    }
    .stButton>button {
        width: 100%;
        background-color: #00FF00 !important;
        color: #000000 !important;
        font-weight: 900 !important;
        height: 60px;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🏋️ PERSONALIZED FITPLAN")
st.markdown("---")

# Athlete Profile
st.header("Athlete Profile")
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("NAME (Required)")
    gender = st.selectbox("GENDER", ["Male", "Female", "Other"])
    height_cm = st.number_input("HEIGHT (CM) (Required)", min_value=0.0, step=0.1)

with col2:
    weight_kg = st.number_input("WEIGHT (KG) (Required)", min_value=0.0, step=0.1)
    goal = st.selectbox("FITNESS GOAL", ["Build Muscle", "Weight Loss", "Strength Gain", "Abs Building", "Flexible"])
    level = st.selectbox("FITNESS LEVEL", ["Beginner", "Intermediate", "Advanced"])

equipment_options = [
    "Dumbbells", "Barbell", "Kettlebells", "Weight Plates",
    "Resistance Band", "Yoga Mat", "Pull-up Bar", "Bench Press", "No Equipment"
]
equipment = st.multiselect("AVAILABLE EQUIPMENT", equipment_options)

st.markdown("---")

if st.button("SUBMIT PROFILE"):

    if not name or height_cm <= 0 or weight_kg <= 0:
        st.error("🚨 VALIDATION FAILED: PLEASE PROVIDE NAME, HEIGHT, AND WEIGHT.")
    else:
        prompt, bmi, bmi_status = build_prompt(
            name,
            gender,
            height_cm,
            weight_kg,
            goal,
            level,
            equipment
        )

        st.success(f"PROFILE SUBMITTED SUCCESSFULLY! HELLO {name.upper()}")
        st.markdown(f"### BMI: {bmi:.2f} | CATEGORY: {bmi_status.upper()}")
        st.markdown("---")

        with st.spinner("Generating your workout plan..."):
            workout_plan = query_model(prompt)

        # Clean unwanted markdown symbols
        workout_plan = workout_plan.replace("**", "")

        st.markdown("## 🏆 YOUR 5-DAY WORKOUT PLAN")
        st.markdown("---")
        st.markdown(workout_plan)
