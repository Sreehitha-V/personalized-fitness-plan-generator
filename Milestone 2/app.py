import streamlit as st
import re  # Aggressive text cleaning
from prompt_builder import build_prompt
from model_api import query_model

# Page Config
st.set_page_config(page_title="PERSONALIZED FITPLAN", layout="centered")

# --- PROFESSIONAL CSS: NO GAPS, NO MESS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)), 
                     url("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=2070");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Global Text Styling */
    h1, h2, h3, label, p, span {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        text-transform: uppercase;
    }
    /* THE SUBMIT BUTTON - SOLID BLACK WITH WHITE TEXT */
    div.stButton > button:first-child {
        width: 100% !important;
        background-color: #000000 !important; 
        color: #FFFFFF !important;            
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        height: 60px !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 10px !important;
    }
    /* Tab Styling visibility */
    .stTabs [aria-selected="true"] { background-color: #FFFFFF !important; }
    .stTabs [aria-selected="true"] p { color: #000000 !important; }
    /* PROFESSIONAL OUTPUT BOX - FORCES TIGHT SPACING */
    .workout-container {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FFFFFF;
        color: #FFFFFF;
        line-height: 1.3 !important; /* Tight spacing to remove gaps */
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'workout_plan' not in st.session_state:
    st.session_state.workout_plan = ""
if 'bmi_info' not in st.session_state:
    st.session_state.bmi_info = ""
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

st.title("🏋️ PERSONALIZED FITPLAN")

tab1, tab2 = st.tabs(["📝 ATHLETE PROFILE", "🏆 YOUR WORKOUT PLAN"])

with tab1:
    st.header("Build Your Profile")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("NAME (Required)")
        gender = st.selectbox("GENDER", ["Male", "Female", "Other"])
        height_cm = st.number_input("HEIGHT (CM)", min_value=1.0)
    with col2:
        age = st.number_input("AGE (Required)", min_value=1)
        weight_kg = st.number_input("WEIGHT (KG)", min_value=1.0)
        goal = st.selectbox("GOAL", ["Build Muscle", "Weight Loss", "Strength", "Abs", "Flexible"])

    level = st.selectbox("LEVEL", ["Beginner", "Intermediate", "Advanced"])
    equipment = st.multiselect("EQUIPMENT", ["Dumbbells", "Barbell", "Kettlebells", "Yoga Mat", "Pull-up Bar", "No Equipment"])

    if st.button("SUBMIT PROFILE"):
        if not name or height_cm <= 1 or weight_kg <= 1:
            st.error("🚨 PLEASE FILL IN ALL FIELDS.")
        else:
            with st.spinner("GENERATING..."):
                # Call prompt_builder with the 8 arguments you added
                prompt, bmi, bmi_status = build_prompt(name, gender, height_cm, weight_kg, goal, level, equipment, age)
                
                # Fetch raw response
                raw_output = query_model(prompt)
                
                # --- THE HARD CLEANUP: NO STARS, NO GAPS ---
                # 1. Delete every asterisk (*)
                clean_text = re.sub(r'\*', '', raw_output)
                # 2. Collapse 3 or more newlines into just 2 (Standard spacing)
                clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)
                # 3. Trim edge spaces
                clean_text = clean_text.strip()
                
                st.session_state.workout_plan = clean_text
                st.session_state.bmi_info = f"BMI: {bmi:.2f} | {bmi_status.upper()}"
                st.session_state.user_name = name.upper()
                st.success("PROFILE SUBMITTED!")

with tab2:
    if st.session_state.workout_plan:
        st.header(f"🔥 HELLO {st.session_state.user_name}!")
        st.info(f"📊 {st.session_state.bmi_info}")
        st.markdown("---")
        
        # We use unsafe_allow_html with a custom div to bypass Streamlit's default spacing
        st.markdown(f'<div class="workout-container">{st.session_state.workout_plan}</div>', unsafe_allow_html=True)
    else:
        st.warning("PLEASE SUBMIT YOUR PROFILE FIRST.")
