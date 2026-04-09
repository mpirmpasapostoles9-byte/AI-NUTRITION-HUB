import streamlit as st
import g4f

# 1. ΠΛΗΡΕΣ ΛΕΞΙΚΟ ΓΙΑ 100% ΚΑΘΑΡΗ ΓΛΩΣΣΑ
languages = {
    "Ελληνικά": {
        "title": "🥗 AI NUTRITION HUB",
        "sub": "Επαγγελματική Ανάλυση Διατροφής από τον Birbas",
        "login": "🔐 Είσοδος",
        "welcome": "Καλώς ήρθες",
        "gender": "Φύλο",
        "age": "Ηλικία",
        "weight": "Βάρος (kg)",
        "height": "Ύψος (cm)",
        "activity": "Γενική Δραστηριότητα",
        "workout": "Περιγράψτε τα αθλήματα/προπονήσεις σας",
        "workout_ex": "π.χ. Ποδόσφαιρο 2 φορές την εβδομάδα, Γυμναστήριο 3 φορές",
        "goal": "Στόχος",
        "other_goal": "Γράψτε τον δικό σας στόχο",
        "med": "Αλλεργίες ή Ιατρικά Θέματα",
        "med_ex": "Κανένα",
        "lang_sel": "Γλώσσα",
        "btn": "🚀 Δημιουργία Επαγγελματικού Πλάνου",
        "wait": "Η AI αναλύει τα δεδομένα σας...",
        "warning": "Παρακαλώ εισάγετε το Email και τον Κωδικό σας αριστερά.",
        "download": "💾 Λήψη Πλάνου (PDF/Text)",
        "goals": ["Απώλεια Βάρους", "Απώλεια Βάρους με Αύξηση Μυϊκής Μάζας", "Συντήρηση", "Χάσιμο Λίπους", "Αύξηση Μυϊκής Μάζας", "Lean Bulk (Καθαρή Αύξηση)", "Άλλο (Γράψτε παρακάτω)"]
    },
    "English": {
        "title": "🥗 AI NUTRITION HUB",
        "sub": "Professional Nutrition Analysis by Birbas",
        "login": "🔐 Login",
        "welcome": "Welcome",
        "gender": "Gender",
        "age": "Age",
        "weight": "Weight (kg)",
        "height": "Height (cm)",
        "activity": "Activity Level",
        "workout": "Describe your sports/workouts",
        "workout_ex": "e.g. Football 2x week, Gym 3x week",
        "goal": "Goal",
        "other_goal": "Write your custom goal",
        "med": "Allergies or Medical Issues",
        "med_ex": "None",
        "lang_sel": "Language",
        "btn": "🚀 Create Professional Plan",
        "wait": "AI is analyzing your data...",
        "warning": "Please enter your Email and Password on the left sidebar.",
        "download": "💾 Download Plan",
        "goals": ["Weight Loss", "Weight Loss with Muscle Gain", "Maintenance", "Fat Loss", "Muscle Gain", "Lean Bulk", "Other (Write below)"]
    }
}

st.set_page_config(page_title="AI NUTRITION HUB", page_icon="🥗", layout="wide")

# Επιλογή Γλώσσας
sel_lang = st.sidebar.selectbox("🌐 Language / Γλώσσα", ["Ελληνικά", "English"])
t = languages[sel_lang]

# Sidebar Login
st.sidebar.title(t["login"])
email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

def generate_plan(gender, age, weight, height, activity_level, workout_desc, final_goal, medical_history, lang_name):
    # Υπολογισμοί
    if "Άνδρας" in gender or "Male" in gender:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    mult = 1.2
    if "Active" in activity_level or "Ελαφριά" in activity_level: mult = 1.375
    if "Moderately" in activity_level or "Μέτρια" in activity_level: mult = 1.55
    if "Very" in activity_level or "Έντονη" in activity_level: mult = 1.725
    if "Extra" in activity_level or "Πολύ Έντονη" in activity_level: mult = 1.9
    
    tdee = bmr * mult
    target_calories = tdee
    if any(x in final_goal for x in ["Loss", "Απώλεια", "Χάσιμο", "Fat"]): target_calories = tdee - 500
    elif any(x in final_goal for x in ["Gain", "Αύξηση", "Bulk"]): target_calories = tdee + 400

    prompt = f"""
    Role: Professional Nutritionist. Target: {target_calories:.0f} kcal.
    User: {gender}, {age}yo, {weight}kg, {height}cm.
    Activity: {activity_level}. Workout Details: {workout_desc}.
    Goal: {final_goal}. Allergies: {medical_history}.
    Provide a detailed 7-day meal plan with macros and shopping list.
    Language: Strictly in {lang_name}.
    """

    try:
        response = g4f.ChatCompletion.create(model=g4f.models.default, messages=[{"role": "user", "content": prompt}])
        return response, bmr, tdee, target_calories
    except Exception as e:
        return f"Error: {e}", 0, 0, 0

# --- UI ---
st.title(t["title"])
st.subheader(t["sub"])

if email and password == "APO123":
    st.success(f"{t['welcome']}, {email}!")
    col1, col2 = st.columns(2)
    
    with col1:
        gender_opt = ["Άνδρας (Male)", "Γυναίκα (Female)"] if sel_lang == "Ελληνικά" else ["Male", "Female"]
        gender = st.selectbox(t["gender"], gender_opt)
        age = st.number_input(t["age"], min_value=10, max_value=100, value=25)
        weight = st.number_input(t["weight"], min_value=30, max_value=250, value=75)
        height = st.number_input(t["height"], min_value=100, max_value=250, value=175)

    with col2:
        activity_opt = [
            "Καθιστική (Sedentary)", "Ελαφριά (Lightly Active)", 
            "Μέτρια (Moderately Active)", "Έντονη (Very Active)", "Πολύ Έντονη (Extra Active)"
        ]
        activity_level = st.selectbox(t["activity"], activity_opt)
        goal_selection = st.selectbox(t["goal"], t["goals"])
        
        final_goal = goal_selection
        if "Άλλο" in goal_selection or "Other" in goal_selection:
            final_goal = st.text_input(t["other_goal"])
            
        workout_desc = st.text_area(t["workout"], value=t["workout_ex"])
        medical_history = st.text_area(t["med"], value=t["med_ex"])

    if st.button(t["btn"]):
        with st.spinner(t["wait"]):
            result, bmr_val, tdee_val, target_val = generate_plan(gender, age, weight, height, activity_level, workout_desc, final_goal, medical_history, sel_lang)
            st.markdown("---")
            c1, c2, c3 = st.columns(3)
            c1.metric("BMR", f"{bmr_val:.0f} kcal")
            c2.metric("TDEE", f"{tdee_val:.0f} kcal")
            c3.metric(t["goal"], f"{target_val:.0f} kcal")
            st.markdown("---")
            st.markdown(result)
            st.download_button(t["download"], result, file_name="nutrition_plan.md")
else:
    st.warning(t["warning"])

st.markdown("---")
st.caption(f"© 2026 AI NUTRITION HUB | Powered by Birbas")
