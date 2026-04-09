import streamlit as st
import g4f

# 1. Ρύθμιση Σελίδας
st.set_page_config(page_title="AI NUTRITION HUB", page_icon="🥗", layout="wide")

# 2. Sidebar για Είσοδο (Προσωρινό Login μέχρι το Firebase)
st.sidebar.title("🔐 Login")
email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

def generate_plan(gender, age, weight, height, activity, goal, medical_history, lang):
    # --- ΥΠΟΛΟΓΙΣΜΟΣ ΜΕΤΑΒΟΛΙΣΜΟΥ ---
    if "Άνδρας" in gender or "Male" in gender:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    activity_map = {
        "Καθιστική (Sedentary)": 1.2,
        "Ελαφριά (Lightly Active)": 1.375,
        "Μέτρια (Moderately Active)": 1.55,
        "Έντονη (Very Active)": 1.725,
        "Πολύ Έντονη (Extra Active)": 1.9
    }
    
    multiplier = activity_map.get(activity, 1.2)
    tdee = bmr * multiplier
    
    if "Απώλεια" in goal:
        target_calories = tdee - 500
    elif "Αύξηση" in goal:
        target_calories = tdee + 400
    else:
        target_calories = tdee

    # --- ΕΝΙΣΧΥΜΕΝΟ PROMPT ΓΙΑ ΤΗΝ AI ---
    prompt = f"""
    Είσαι ο κορυφαίος κλινικός διατροφολόγος του AI NUTRITION HUB.
    
    ΑΝΑΛΥΣΗ ΜΕΤΑΒΟΛΙΣΜΟΥ ΠΕΛΑΤΗ:
    - Βασικός Μεταβολισμός (BMR): {bmr:.0f} kcal
    - Θερμίδες Συντήρησης (TDEE): {tdee:.0f} kcal
    - ΣΤΟΧΟΣ ΗΜΕΡΗΣΙΩΝ ΘΕΡΜΙΔΩΝ: {target_calories:.0f} kcal
    
    ΣΤΟΙΧΕΙΑ ΠΕΛΑΤΗ:
    - Φύλο: {gender}, Ηλικία: {age}, Βάρος: {weight}kg, Ύψος: {height}cm.
    - Στόχος: {goal}.
    - Ιατρικό Ιστορικό/Αλλεργίες: {medical_history}.
    
    ΟΔΗΓΙΕΣ:
    1. Φτιάξε ένα πλήρες πλάνο 7 ημερών βασισμένο ΑΥΣΤΗΡΑ στις {target_calories:.0f} θερμίδες.
    2. Ανάλυση Πρωτεΐνης, Υδατανθράκων και Λίπους για κάθε γεύμα.
    3. Συμπερίλαβε μια πλήρη Λίστα Αγορών (Shopping List).
    4. Απάντησε με επαγγελματικό ύφος στα {lang}.
    """

    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}]
        )
        return response, bmr, tdee, target_calories
    except Exception as e:
        return f"Error: {e}", 0, 0, 0

# --- ΚΥΡΙΩΣ ΕΦΑΡΜΟΓΗ ---
st.title("🥗 AI NUTRITION HUB")
st.subheader("Professional Nutrition Analysis by Birbas")

if email and password == "APO123":
    st.success(f"Καλώς ήρθες, {email}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox("Φύλο", ["Άνδρας (Male)", "Γυναίκα (Female)"])
        age = st.number_input("Ηλικία", min_value=10, max_value=100, value=25)
        weight = st.number_input("Βάρος (kg)", min_value=30, max_value=250, value=75)
        height = st.number_input("Ύψος (cm)", min_value=100, max_value=250, value=175)

    with col2:
        activity = st.selectbox("Επίπεδο Δραστηριότητας", [
            "Καθιστική (Sedentary)", 
            "Ελαφριά (Lightly Active)", 
            "Μέτρια (Moderately Active)", 
            "Έντονη (Very Active)", 
            "Πολύ Έντονη (Extra Active)"
        ])
        goal = st.selectbox("Στόχος", ["Απώλεια Βάρους", "Συντήρηση", "Αύξηση Μυϊκής Μάζας"])
        medical_history = st.text_area("Αλλεργίες ή Ιατρικά Θέματα", "Κανένα")
        lang = st.selectbox("Γλώσσα Απάντησης", ["Ελληνικά", "English"])

    if st.button("🚀 Δημιουργία Επαγγελματικού Πλάνου"):
        with st.spinner("Γίνεται υπολογισμός μεταβολισμού και σχεδιασμός πλάνου..."):
            result, bmr_val, tdee_val, target_val = generate_plan(gender, age, weight, height, activity, goal, medical_history, lang)
            
            # Εμφάνιση Μετρήσεων
            st.markdown("---")
            c1, c2, c3 = st.columns(3)
            c1.metric("BMR (Μεταβολισμός)", f"{bmr_val:.0f} kcal")
            c2.metric("TDEE (Συντήρηση)", f"{tdee_val:.0f} kcal")
            c3.metric("Στόχος Θερμίδων", f"{target_val:.0f} kcal", delta=f"{target_val-tdee_val:.0f}")
            
            st.markdown("---")
            st.markdown(result)
            
            st.download_button("💾 Download Plan", result, file_name="nutrition_plan.md")

else:
    st.warning("Παρακαλώ εισάγετε τα διαπιστευτήριά σας στο μενού αριστερά.")

# Footer
st.markdown("---")
st.caption("© 2026 AI NUTRITION HUB | Advanced AI Systems | Powered by Birbas")
