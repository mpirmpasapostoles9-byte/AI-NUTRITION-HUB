import streamlit as st
import g4f

st.set_page_config(page_title="Apostolis AI Elite", page_icon="📅", layout="wide")

# --- SIDEBAR & ΓΛΩΣΣΑ ---
with st.sidebar:
    st.header("🌐 Language / Γλώσσα")
    lang = st.radio("Select Language:", ["Ελληνικά", "English"])

    # Μεταφράσεις
    t_login = "🔐 Σύνδεση" if lang == "Ελληνικά" else "🔐 Login"
    t_profile = "👤 Στοιχεία Πελάτη" if lang == "Ελληνικά" else "👤 Client Profile"
    t_schedule = "📅 Εβδομαδιαίο Πρόγραμμα" if lang == "Ελληνικά" else "📅 Weekly Schedule"
    t_goal = "🎯 Στόχος" if lang == "Ελληνικά" else "🎯 Goal"
    t_budget = "💰 Εβδομαδιαίο Budget (€):" if lang == "Ελληνικά" else "💰 Weekly Budget (€):"
    t_button = "🚀 Δημιουργία Πλάνου" if lang == "Ελληνικά" else "🚀 Generate Plan"

    st.header(t_login)
    user_email = st.text_input("Email:")
    user_password = st.text_input("Password:" if lang == "English" else "Κωδικός:", type="password")
    
    st.header(t_profile)
    age = st.number_input("Age" if lang == "English" else "Ηλικία:", 15, 100, 25)
    weight = st.number_input("Weight (kg)" if lang == "English" else "Βάρος (kg):", 30, 200, 75)
    height = st.number_input("Height (cm)" if lang == "English" else "Ύψος (cm):", 120, 230, 175)

    # --- ΝΕΟ: ΗΜΕΡΟΛΟΓΙΟ ΔΡΑΣΤΗΡΙΟΤΗΤΑΣ ---
    st.header(t_schedule)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] if lang == "English" else ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή", "Σάββατο", "Κυριακή"]
    
    # Λίστα με δραστηριότητες
    activities = ["Rest", "Gym / Weights", "Football", "Basketball", "Running", "Swimming", "Crossfit"] if lang == "English" else ["Ξεκούραση", "Γυμναστήριο / Βάρη", "Ποδόσφαιρο", "Μπάσκετ", "Τρέξιμο", "Κολύμβηση", "Crossfit"]
    
    user_schedule = {}
    for day in days:
        user_schedule[day] = st.selectbox(f"{day}:", activities, key=day)

    st.header(t_goal)
    goals_list = ["Fat Loss", "Recomposition", "Lean Bulk", "Maintenance"] if lang == "English" else ["Χάσιμο Λίπους", "Recomposition", "Lean Bulk", "Συντήρηση"]
    target = st.selectbox(t_goal, goals_list)
    budget = st.select_slider(t_budget, options=["10€-30€", "30€-50€", "50€-80€", "80€-120€", "120€+"])

# --- ΚΥΡΙΩΣ ΣΕΛΙΔΑ ---
st.title("🏅 Apostolis AI: Elite Nutrition Hub")

if user_email and user_password == "APO123":
    if st.button(t_button):
        with st.spinner('Analyzing your schedule...'):
            try:
                # Μετατροπή του schedule σε κείμενο για το AI
                schedule_text = "\n".join([f"{d}: {a}" for d, a in user_schedule.items()])
                
                prompt = f"""
                You are an elite sports nutritionist. 
                Client: {user_email}, {age} years old, {weight}kg, {height}cm.
                Weekly Schedule:
                {schedule_text}
                
                Goal: {target}. Weekly Budget: {budget}.
                
                INSTRUCTIONS:
                1. Adjust calories and macros PER DAY based on the activity. 
                   High intensity days (Football/Crossfit) need more carbs. 
                   Rest days need lower calories.
                2. Use Mediterranean snacks (yogurt, nuts, toast). No peanut butter/apple.
                3. Provide a full 7-day meal plan and a shopping list.
                4. Respond EXCLUSIVELY in: {lang}.
                """
                
                response = g4f.ChatCompletion.create(
                    model=g4f.models.default,
                    messages=[{"role": "user", "content": prompt}]
                )
                st.markdown("---")
                st.markdown(response)
                st.download_button("📥 Download Plan", response, f"athlete_plan_{user_email}.txt")
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.warning("Please enter your credentials / Παρακαλώ βάλτε τα στοιχεία σας.")