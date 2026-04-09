import streamlit as st
import g4f
import pyrebase

# --- FIREBASE CONFIG (Από τη φωτό σου) ---
firebase_config = {
    "apiKey": "AIzaSyCjYgrcFDBwx4CZtEt-bTFrAFdX1D64pMQ",
    "authDomain": "ai-nutrition-hub.firebaseapp.com",
    "projectId": "ai-nutrition-hub",
    "storageBucket": "ai-nutrition-hub.firebasestorage.app",
    "messagingSenderId": "955664360747",
    "appId": "1:955664360747:web:01794faf60b5001886916e",
    "databaseURL": "" 
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# --- ΛΕΞΙΚΟ ΓΛΩΣΣΩΝ ---
languages = {
    "Ελληνικά": {
        "title": "🥗 AI NUTRITION HUB",
        "sub": "Επαγγελματική Ανάλυση από Birbas",
        "log_sign": "🔐 Σύνδεση / Εγγραφή",
        "email": "Email", "pass": "Κωδικός",
        "btn_login": "Σύνδεση", "btn_signup": "Εγγραφή νέου χρήστη",
        "welcome": "Καλώς ήρθες", "logout": "Αποσύνδεση",
        "gender": "Φύλο", "age": "Ηλικία", "weight": "Βάρος (kg)", "height": "Ύψος (cm)",
        "activity": "Δραστηριότητα", "workout": "Προπονήσεις", "goal": "Στόχος",
        "med": "Αλλεργίες", "btn_plan": "🚀 Δημιουργία Πλάνου",
        "goals": ["Απώλεια Βάρους", "Απώλεια με Μυϊκή Μάζα", "Συντήρηση", "Χάσιμο Λίπους", "Αύξηση Μάζας", "Lean Bulk", "Άλλο"]
    },
    "English": {
        "title": "🥗 AI NUTRITION HUB",
        "sub": "Professional Analysis by Birbas",
        "log_sign": "🔐 Login / Sign Up",
        "email": "Email", "pass": "Password",
        "btn_login": "Login", "btn_signup": "Sign Up",
        "welcome": "Welcome", "logout": "Logout",
        "gender": "Gender", "age": "Age", "weight": "Weight (kg)", "height": "Height (cm)",
        "activity": "Activity", "workout": "Workouts", "goal": "Goal",
        "med": "Allergies", "btn_plan": "🚀 Create Plan",
        "goals": ["Weight Loss", "Weight Loss with Muscle Gain", "Maintenance", "Fat Loss", "Muscle Gain", "Lean Bulk", "Other"]
    }
}

st.set_page_config(page_title="AI NUTRITION HUB", page_icon="🥗", layout="wide")
sel_lang = st.sidebar.selectbox("🌐 Language", ["Ελληνικά", "English"])
t = languages[sel_lang]

# --- AUTH LOGIC ---
if 'user' not in st.session_state:
    st.session_state.user = None

st.sidebar.title(t["log_sign"])
if st.session_state.user is None:
    choice = st.sidebar.radio("Menu", [t["btn_login"], t["btn_signup"]])
    email = st.sidebar.text_input(t["email"])
    password = st.sidebar.text_input(t["pass"], type="password")

    if choice == t["btn_signup"]:
        if st.sidebar.button(t["btn_signup"]):
            try:
                user = auth.create_user_with_email_and_password(email, password)
                st.sidebar.success("Ο λογαριασμός δημιουργήθηκε! Κάνε Login.")
            except:
                st.sidebar.error("Η εγγραφή απέτυχε. Δες αν το email είναι σωστό.")
    else:
        if st.sidebar.button(t["btn_login"]):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.user = user
                st.rerun()
            except:
                st.sidebar.error("Λάθος Email ή Κωδικός.")
else:
    st.sidebar.write(f"✅ {t['welcome']}: {st.session_state.user['email']}")
    if st.sidebar.button(t["logout"]):
        st.session_state.user = None
        st.rerun()

# --- MAIN APP ---
st.title(t["title"])
st.subheader(t["sub"])

if st.session_state.user:
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox(t["gender"], ["Male", "Female"])
        age = st.number_input(t["age"], 10, 100, 25)
        weight = st.number_input(t["weight"], 30, 250, 75)
        height = st.number_input(t["height"], 100, 250, 175)
    with col2:
        activity = st.selectbox(t["activity"], ["Sedentary", "Light", "Moderate", "Very Active"])
        goal = st.selectbox(t["goal"], t["goals"])
        workout = st.text_area(t["workout"], "e.g. Gym 3x week")
        med = st.text_area(t["med"], "None")

    if st.button(t["btn_plan"]):
        with st.spinner("Analyzing..."):
            # Εδώ καλούμε την AI (όπως στον προηγούμενο κώδικα)
            prompt = f"Diet plan for {gender}, {weight}kg, goal: {goal}, workout: {workout}. Language: {sel_lang}"
            try:
                res = g4f.ChatCompletion.create(model=g4f.models.default, messages=[{"role": "user", "content": prompt}])
                st.markdown("---")
                st.markdown(res)
            except Exception as e:
                st.error(f"AI Error: {e}")
else:
    st.info("👋 " + t["warning"] if "warning" in t else "Please Login to continue.")

st.markdown("---")
st.caption("© 2026 AI NUTRITION HUB | Powered by Birbas")
