import streamlit as st
import g4f
import pyrebase

# --- FIREBASE CONFIG (Διορθωμένο για να αποφύγουμε το KeyError) ---
firebase_config = {
    "apiKey": "AIzaSyCjYgrcFDBwx4CZtEt-bTFrAFdX1D64pMQ",
    "authDomain": "ai-nutrition-hub.firebaseapp.com",
    "projectId": "ai-nutrition-hub",
    "storageBucket": "ai-nutrition-hub.firebasestorage.app",
    "messagingSenderId": "955664360747",
    "appId": "1:955664360747:web:01794faf60b5001886916e",
    "databaseURL": "" # Πρέπει να υπάρχει ως κλειδί, έστω και κενό
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# --- ΠΛΗΡΕΣ ΛΕΞΙΚΟ ΓΙΑ ΕΛΛΗΝΙΚΑ & ΑΓΓΛΙΚΑ ---
languages = {
    "Ελληνικά": {
        "log_sign": "🔐 Σύνδεση / Εγγραφή", "btn_login": "Σύνδεση", "btn_signup": "Εγγραφή",
        "welcome": "Καλώς ήρθες", "logout": "Αποσύνδεση",
        "gender": "Φύλο", "age": "Ηλικία", "weight": "Βάρος (kg)", "height": "Ύψος (cm)",
        "activity": "Δραστηριότητα", "goal": "Στόχος", "workout": "Προπονήσεις",
        "btn_plan": "🚀 Δημιουργία Πλάνου", "wait": "Η AI αναλύει...",
        "gender_ops": ["Άνδρας", "Γυναίκα"],
        "activity_ops": ["Καθιστική", "Ελαφριά", "Μέτρια", "Έντονη", "Πολύ Έντονη"],
        "goals": ["Απώλεια Βάρους", "Αύξηση Μάζας", "Συντήρηση", "Γράμμωση", "Lean Bulk", "Άλλο"],
        "workout_ex": "π.χ. Γυμναστήριο 3 φορές την εβδομάδα",
        "warn": "Παρακαλώ συνδεθείτε για να συνεχίσετε."
    },
    "English": {
        "log_sign": "🔐 Login / Sign Up", "btn_login": "Login", "btn_signup": "Sign Up",
        "welcome": "Welcome", "logout": "Logout",
        "gender": "Gender", "age": "Age", "weight": "Weight (kg)", "height": "Height (cm)",
        "activity": "Activity", "goal": "Goal", "workout": "Workouts",
        "btn_plan": "🚀 Create Plan", "wait": "AI is analyzing...",
        "gender_ops": ["Male", "Female"],
        "activity_ops": ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"],
        "goals": ["Weight Loss", "Muscle Gain", "Maintenance", "Fat Loss", "Lean Bulk", "Other"],
        "workout_ex": "e.g. Gym 3x week",
        "warn": "Please Login to continue."
    }
}

# Λίστα για την αναζήτηση (Extra γλώσσες που χρησιμοποιούν το English UI ως βάση)
extra_langs = [
    "Spanish", "French", "German", "Italian", "Portuguese", "Russian", "Arabic", 
    "Turkish", "Chinese", "Japanese", "Dutch", "Swedish", "Polish", "Norwegian"
]
all_options = list(languages.keys()) + extra_langs

st.set_page_config(page_title="AI NUTRITION HUB", page_icon="🥗", layout="wide")

# --- SIDEBAR: ΑΝΑΖΗΤΗΣΗ ΓΛΩΣΣΑΣ ---
st.sidebar.markdown("### 🌐 Language / Γλώσσα")
sel_lang = st.sidebar.selectbox("Search language...", all_options, index=0)

# Επιλογή μετάφρασης UI
t = languages.get(sel_lang, languages["English"])

if 'user' not in st.session_state: st.session_state.user = None

# --- SIDEBAR AUTHENTICATION ---
st.sidebar.title(t["log_sign"])
if st.session_state.user is None:
    choice = st.sidebar.radio("Menu", [t["btn_login"], t["btn_signup"]])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if choice == t["btn_signup"]:
        if st.sidebar.button(t["btn_signup"]):
            try:
                auth.create_user_with_email_and_password(email, password)
                st.sidebar.success("Επιτυχία! Κάντε Login.")
            except Exception as e: st.sidebar.error(f"Error: {e}")
    else:
        if st.sidebar.button(t["btn_login"]):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.user = user
                st.rerun()
            except: st.sidebar.error("Λάθος στοιχεία.")
else:
    st.sidebar.write(f"✅ {t['welcome']}: {st.session_state.user['email']}")
    if st.sidebar.button(t["logout"]):
        st.session_state.user = None
        st.rerun()

# --- MAIN APP ---
st.title("🥗 AI NUTRITION HUB")
# Εδώ μπήκε το όνομά σου στην κορυφή όπως το ζήτησες!
st.subheader(f"Professional Analysis by Birbas | 🌐 {sel_lang}")

if st.session_state.user:
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox(t["gender"], t["gender_ops"])
        age = st.number_input(t["age"], 10, 100, 25)
        weight = st.number_input(t["weight"], 30, 250, 75)
        height = st.number_input(t["height"], 100, 250, 175)
    with col2:
        activity = st.selectbox(t["activity"], t["activity_ops"])
        goal = st.selectbox(t["goal"], t["goals"])
        workout = st.text_area(t["workout"], t["workout_ex"])
        
    if st.button(t["btn_plan"]):
        with st.spinner(t["wait"]):
            # Η AI θα απαντάει στη γλώσσα που επιλέχθηκε από την αναζήτηση
            prompt = f"Diet plan for {gender}, {weight}kg, {height}cm. Goal: {goal}. Workout: {workout}. Respond strictly in {sel_lang}."
            try:
                res = g4f.ChatCompletion.create(model=g4f.models.default, messages=[{"role": "user", "content": prompt}])
                st.markdown("---")
                st.markdown(res)
            except Exception as e: st.error(f"Error: {e}")
else:
    st.info(t["warn"])

st.markdown("---")
st.caption(f"© 2026 AI NUTRITION HUB | Powered by Birbas")
