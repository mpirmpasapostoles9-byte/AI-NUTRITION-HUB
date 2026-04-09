import streamlit as st
import streamlit.components.v1 as components
import g4f
import pyrebase

# --- SEO & GOOGLE VERIFICATION ---
st.set_page_config(
    page_title="AI NUTRITION HUB | Birbas Professional Analysis",
    page_icon="🥗",
    layout="wide"
)

# Εδώ μπήκε ο κωδικός που μου έστειλες για τη Google
components.html(
    """
    <meta name="google-site-verification" content="swSdGZxobI8CS_1mu9oVQkRuoMWxBidSdhGY3TNoAaM" />
    """,
    height=0,
)

# --- FIREBASE CONFIG (Διορθωμένο για το KeyError) ---
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

extra_langs = ["Spanish", "French", "German", "Italian", "Portuguese", "Russian", "Arabic", "Turkish", "Chinese", "Japanese"]
all_options = list(languages.keys()) + extra_langs

# --- SIDEBAR: ΑΝΑΖΗΤΗΣΗ ΓΛΩΣΣΑΣ ---
st.sidebar.markdown("### 🌐 Language / Γλώσσα")
sel_lang = st.sidebar.selectbox("Search language...", all_options, index=0)
t = languages.get(sel_lang, languages["English"])

if 'user' not in st.session_state: st.session_state.user = None

# --- SIDEBAR AUTH ---
st.sidebar.title(t["log_sign"])
if st.session_state.user is None:
    choice = st.sidebar.radio("Menu", [t["btn_login"], t["btn_signup"]])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button(choice):
        try:
            if choice == t["btn_signup"]:
                auth.create_user_with_email_and_password(email, password)
                st.sidebar.success("Done! Login now.")
            else:
                st.session_state.user = auth.sign_in_with_email_and_password(email, password)
                st.rerun()
        except Exception as e: st.sidebar.error(f"Error: {e}")
else:
    st.sidebar.write(f"✅ {t['welcome']}: {st.session_state.user['email']}")
    if st.sidebar.button(t["logout"]):
        st.session_state.user = None
        st.rerun()

# --- MAIN APP ---
st.title("🥗 AI NUTRITION HUB")
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
            prompt = f"Diet plan for {gender}, {weight}kg, {height}cm. Goal: {goal}. Workout: {workout}. Respond in {sel_lang}."
            try:
                res = g4f.ChatCompletion.create(model=g4f.models.default, messages=[{"role": "user", "content": prompt}])
                st.markdown("---")
                st.markdown(res)
            except: st.error("AI Busy.")
else:
    st.info(t["warn"])

st.markdown("---")
st.caption(f"© 2026 AI NUTRITION HUB | Powered by Birbas")
