import streamlit as st
import g4f

# 1. Λεξικό Γλωσσών (Μετάφραση όλου του site)
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
        "goal": "Στόχος",
        "other_goal": "Γράψτε τον δικό σας στόχο",
        "med": "Αλλεργίες ή Ιατρικά Θέματα",
        "lang_sel": "Γλώσσα Σελίδας / Page Language",
        "btn": "🚀 Δημιουργία Επαγγελματικού Πλάνου",
        "wait": "Γίνεται ανάλυση...",
        "warning": "Παρακαλώ εισάγετε τα διαπιστευτήριά σας αριστερά.",
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
        "goal": "Goal",
        "other_goal": "Write your custom goal",
        "med": "Allergies or Medical Issues",
        "lang_sel": "Γλώσσα Σελίδας / Page Language",
        "btn": "🚀 Create Professional Plan",
        "wait": "Analyzing...",
        "warning": "Please enter your credentials on the left.",
        "goals": ["Weight Loss", "Weight Loss with Muscle Gain", "Maintenance", "Fat Loss", "Muscle Gain", "Lean Bulk", "Other (Write below)"]
    }
}

# 2. Ρύθμιση Σελίδας
st.set_page_config(page_title="AI NUTRITION HUB", page_icon="🥗", layout="wide")

# Επιλογή Γλώσσας (Πρώτα από όλα)
sel_lang = st.sidebar.selectbox("Language", ["Ελληνικά", "English"])
t = languages[sel_lang]

# 3. Sidebar Login
st.sidebar.title(t["login"])
email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

def generate_plan(gender, age, weight, height, activity_level, workout_desc, final_goal, medical_history, lang_name):
    # --- ΥΠΟΛΟΓΙΣΜΟΣ ΜΕΤΑΒΟΛΙΣΜΟΥ ---
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
    
    # Προσαρμογή θερμίδων βάσει στόχου
    target_calories = tdee
    if "Loss" in final_goal or "Απώλεια" in final_goal or "Χάσιμο" in final_goal: target_calories = tdee - 500
    elif "Gain" in final_goal or "Αύξηση" in final_goal or "Bulk" in final_goal: target_calories = tdee + 400

    prompt = f"""
    Role: Professional Clinical Nutritionist at AI NUTRITION HUB.
    Stats: BMR: {bmr:.0f}, TDEE: {tdee:.0f}, Target: {target_calories:.0f} kcal.
    Profile: {gender}, {age}yo, {weight}kg, {height}cm.
    Workout: {workout_desc}
    Goal: {final_goal}
    Medical: {medical_history}
    Instructions: 7-day plan, P/C/F analysis, Shopping list.
    IMPORTANT: Respond strictly in {lang_name}.
    """

    try:
        response = g4f.ChatCompletion.create(model=g4f.models.default, messages=[{"role": "user", "content": prompt}])
        return response, bmr, tdee, target_calories
    except Exception as e:
        return f"Error: {e}", 0, 0, 0

# --- ΚΥΡΙΩΣ ΕΦΑΡΜΟΓΗ ---
st.title(t["title"])
st.subheader(t["sub"])

if email and password == "APO123":
    st.success(f"{t['welcome']}, {email}")
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox(t["gender"], ["Άνδρας (Male)", "Γυναίκα (Female)"])
        age = st.number_input(t["age"], min_value=10, max_value=100, value=25)
        weight = st.number_input(t["weight"], min_value=30, max_value=250, value=75)
        height = st.number_input(t["height"], min_value=100, max_value=250, value=175)

    with col2:
        activity_level = st.selectbox(t["activity"], [
            "Καθιστική (Sedentary)", "Ελαφριά (Lightly Active)", 
            "Μέτρια (Moderately Active)", "Έντονη (Very Active)", "Πολύ Έντονη (Extra Active)"
        ])
        goal_selection = st.selectbox(t["goal"], t["goals"])
        
        # Αν επιλέξει "Άλλο", εμφανίζεται νέο κουτί
        final_goal = goal_selection
        if "Άλλο" in goal_selection or "Other" in goal_selection:
            final_goal = st.text_input(t["other_goal"])
            
        workout_desc = st.text_area(t["workout"], "e.g. Football 2x week, Gym 3x week")
        medical_history = st.text_area(t["med"], "None")

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
            st.download_button("💾 Download", result, file_name="plan.md")
else:
    st.warning(t["warning"])

st.markdown("---")
st.caption(f"© 2026 AI NUTRITION HUB | Powered by Birbas")
