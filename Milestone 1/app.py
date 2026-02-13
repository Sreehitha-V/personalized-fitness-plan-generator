import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="PERSONALIZED FITPLAN", layout="centered")

# 2. Clean Styling: Extra Bold Typography & Standard Borders for Visibility
st.markdown("""
    <style>
    /* Dark Gym Background Overlay */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=2070");
        background-size: cover;
    }
    
    /* Extra Bold White Text for Clarity */
    h1, h2, h3, label, p, span, .stMarkdown {
        color: #FFFFFF !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Clean Input Boxes - Standard border for full spelling visibility */
    .stTextInput>div>div>input, 
    .stNumberInput>div>div>input, 
    .stSelectbox>div>div>div {
        background-color: #111111 !important;
        color: #00FF00 !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        height: 55px !important;
        border-radius: 8px !important;
    }

    /* Full-width Neon Submit Button */
    .stButton>button {
        width: 100%;
        background-color: #00FF00 !important;
        color: #000000 !important;
        font-weight: 900 !important;
        height: 60px;
        border: none;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Main Dashboard Header
st.title("🏋️ PERSONALIZED FITPLAN")
st.markdown("---")

# 4. Athlete Profile Form
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

# Expanded Equipment List
equipment_options = [
    "Dumbbells", "Barbell", "Kettlebells", "Weight Plates", 
    "Resistance Band", "Yoga Mat", "Pull-up Bar", "Bench Press", "No Equipment"
]
equipment = st.multiselect("AVAILABLE EQUIPMENT", equipment_options)

st.markdown("---")

# 5. Logic and Results
if st.button("SUBMIT PROFILE"):
    # Validation: Ensures no empty name or zero/negative values
    if not name or height_cm <= 0 or weight_kg <= 0:
        st.error("🚨 VALIDATION FAILED: PLEASE PROVIDE NAME, HEIGHT, AND WEIGHT.")
    else:
        # Convert height to meters and calculate BMI
        height_m = height_cm / 100
        bmi_val = round(weight_kg / (height_m ** 2), 2)

        # Classify BMI Category
        if bmi_val < 18.5: category = "Underweight"
        elif 18.5 <= bmi_val < 24.9: category = "Normal"
        elif 25 <= bmi_val < 29.9: category = "Overweight"
        else: category = "Obese"

        # SUCCESS BOX: Personalized with the user's name
        st.success(f"PROFILE SUBMITTED SUCCESSFULLY! HELLO {name.upper()}")

        # Dashboard Result Display
        st.markdown(f"### BMI: {bmi_val} | CATEGORY: {category.upper()}")

        # JSON Output matching your requirement screenshot
        athlete_data = {
            "Name": name,
            "Gender": gender,
            "BMI": bmi_val,
            "Goal": goal,
            "Fitness Level": level,
            "Equipment": equipment
        }
        st.json(athlete_data)
