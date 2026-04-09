import streamlit as st
import g4f
import pyrebase

# --- FIREBASE CONFIG (Από τις φωτογραφίες σου) ---
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

# --- Η ΤΕΡΑΣΤΙΑ ΛΙΣΤΑ ΓΛΩΣΣΩΝ ---
all_languages = [
    "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani", "Basque", "Belarusian", "Bengali", 
    "Bosnian", "Bulgarian", "Catalan", "Cebuano", "Chichewa", "Chinese (Simplified)", "Chinese (Traditional)", 
    "Corsican", "Croatian", "Czech", "Danish", "Dutch", "English", "Esperanto", "Estonian", "Filipino", "Finnish", 
    "French", "Frisian", "Galician", "Georgian", "German", "Greek (Ελληνικά)", "Gujarati", "Haitian Creole", 
    "Hausa", "Hawaiian", "Hebrew", "Hindi", "Hmong", "Hungarian", "Icelandic", "Igbo", "Indonesian", "Irish", 
    "Italian", "Japanese", "Javanese", "Kannada", "Kazakh", "Khmer", "Kinyarwanda", "Korean", "Kurdish (Kurmanji)", 
    "Kyrgyz", "Lao", "Latin", "Latvian", "Lithuanian", "Luxembourgish", "Macedonian", "Malagasy", "Malay", 
    "Malayalam", "Maltese", "Maori", "Marathi", "Mongolian", "Myanmar (Burmese)", "Nepali", "Norwegian", "Odia", 
    "Pashto", "Persian", "Polish", "Portuguese", "Punjabi", "Romanian", "Russian", "Samoan", "Scots Gaelic", 
    "Serbian", "Sesotho", "Shona", "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali", "Spanish", "Sundanese", 
    "Swahili", "Swedish", "Tajik", "Tamil", "Tatar", "Telugu", "Thai", "Turkish", "Turkmen", "Ukrainian", "Urdu", 
    "Uyghur", "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yiddish", "Yoruba", "Zulu"
]

# --- ΛΕΞΙΚΟ ΓΙΑ ΤΙΣ ΒΑΣΙΚΕΣ ΓΛΩΣΣΕΣ ---
ui_translations = {
    "Greek (Ελληνικά)": {
        "log_sign": "🔐 Σύνδεση / Εγγραφή", "btn_login": "Σύνδεση", "btn_signup": "Εγγραφή",
        "gender": "Φύλο", "age": "Ηλικία", "weight": "Βάρος (kg)", "height": "Ύψος (cm)",
        "activity": "Δραστηριότητα", "goal": "Στόχος", "workout": "Προπονήσεις",
        "btn_plan": "🚀 Δημιουργία Πλάνου", "wait": "Η AI αναλύει...",
        "gender_ops": ["Άνδρας", "Γυναίκα"],
        "activity_ops": ["Καθιστική", "Ελαφριά", "Μέτρια", "Έντονη", "Πολύ Έντονη"],
        "goals": ["Απώλεια Βάρους", "Αύξηση Μάζας", "Συντήρηση", "Γράμμωση", "Άλλο"]
    },
    "Default": {
        "log_sign": "🔐 Login / Sign Up", "btn_login": "Login", "btn_signup": "Sign Up",
        "gender": "Gender", "age": "Age", "weight": "Weight (kg)", "height": "Height (cm)",
        "activity": "Activity", "goal": "Goal", "workout": "Workouts",
        "btn_plan": "🚀 Create Plan", "wait": "AI is analyzing...",
        "gender_ops": ["Male", "Female"],
        "activity_ops": ["Sedentary", "Light", "Moderate", "Active", "Extra Active"],
        "goals": ["Weight Loss", "Muscle Gain", "Maintenance", "Lean Bulk", "Other"]
    }
}

st.set_page_config(page_title="AI NUTRITION HUB", page_icon="🥗", layout="wide")

# --- ΑΝΑΖΗΤΗΣΗ ΓΛΩΣΣΑΣ ---
st.sidebar.markdown("### 🌐 Select Language")
selected_lang = st.sidebar.selectbox("Search your language...", all_languages, index=all_languages.index("Greek (Ελληνικά)"))

# Επιλογή μετάφρασης UI
t = ui_translations["Greek (Ελληνικά)"] if selected_lang == "Greek (Ελληνικά)" else ui_translations["Default"]

if 'user' not in st.session_state: st.session_state.user = None

# --- SIDEBAR LOGIN (FIREBASE) ---
st.sidebar.title(t["log_sign"])
if st.session_state.user is None:
    choice = st.sidebar.radio("Menu", [t["btn_login"], t["btn_signup"]])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if choice == t["btn_signup"]:
        if st.sidebar.button(t["btn_signup"]):
            try:
                auth.create_user_with_email_and_password(email, password)
                st.sidebar.success("Done! Now Login.")
            except Exception as e: st.sidebar.error(f"Error: {e}")
    else:
        if st.sidebar.button(t["btn_login"]):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.user = user
                st.rerun()
            except: st.sidebar.error("Check credentials.")
else:
    st.sidebar.write(f"✅ User: {st.session_state.user['email']}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

# --- MAIN APP ---
st.title("🥗 AI NUTRITION HUB")
st.subheader(f"Global Nutrition Analysis | Language: {selected_lang}")

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
        workout = st.text_area(t["workout"], "Describe your training...")
        
    if st.button(t["btn_plan"]):
        with st.spinner(t["wait"]):
            # Η ΕΝΤΟΛΗ ΠΡΟΣ ΤΗΝ AI ΓΙΑ ΤΗ ΓΛΩΣΣΑ
            prompt = f"Diet plan for {gender}, {weight}kg, {height}cm. Goal: {goal}. Workout: {workout}. IMPORTANT: The user speaks {selected_lang}. Respond entirely and professionally in {selected_lang}."
            try:
                res = g4f.ChatCompletion.create(model=g4f.models.default, messages=[{"role": "user", "content": prompt}])
                st.markdown("---")
                st.markdown(res)
            except Exception as e: st.error(f"AI Error: {e}")
else:
    st.info("Please Login to start your journey.")

st.markdown("---")
st.caption("© 2026 AI NUTRITION HUB | Global Platform by Birbas")
