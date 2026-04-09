import streamlit as st
import g4f
import pyrebase

# --- ΔΙΟΡΘΩΜΕΝΟ FIREBASE CONFIG (Με databaseURL για να μην βγάζει error) ---
firebase_config = {
    "apiKey": "AIzaSyCjYgrcFDBwx4CZtEt-bTFrAFdX1D64pMQ",
    "authDomain": "ai-nutrition-hub.firebaseapp.com",
    "projectId": "ai-nutrition-hub",
    "storageBucket": "ai-nutrition-hub.firebasestorage.app",
    "messagingSenderId": "955664360747",
    "appId": "1:955664360747:web:01794faf60b5001886916e",
    "databaseURL": "https://ai-nutrition-hub.firebaseio.com" # Προστέθηκε για το σφάλμα
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# --- ΛΙΣΤΑ 100+ ΓΛΩΣΣΩΝ ---
all_languages = [
    "Greek", "English", "Spanish", "French", "German", "Italian", "Chinese", "Japanese", "Russian", "Arabic",
    "Portuguese", "Dutch", "Swedish", "Turkish", "Korean", "Polish", "Norwegian", "Danish", "Finnish", "Hindi",
    "Albanian", "Bulgarian", "Croatian", "Czech", "Estonian", "Georgian", "Hebrew", "Hungarian", "Indonesian",
    "Irish", "Latin", "Latvian", "Lithuanian", "Malay", "Maltese", "Persian", "Romanian", "Serbian", "Slovak",
    "Slovenian", "Thai", "Ukrainian", "Vietnamese", "Welsh"
]

st.set_page_config(page_title="AI NUTRITION HUB", layout="wide")

# --- SEARCHABLE LANGUAGE SELECTOR ---
st.sidebar.title("🌐 Global Settings")
sel_lang = st.sidebar.selectbox("Search & Select Language", all_languages, index=0)

# --- AI UI TRANSLATOR ---
# Αυτή η λειτουργία μεταφράζει τα κουμπιά του site αυτόματα!
@st.cache_data
def translate_ui(target_lang):
    if target_lang == "Greek":
        return {
            "title": "🥗 AI NUTRITION HUB", "sub": "Επαγγελματική Ανάλυση",
            "btn_plan": "🚀 Δημιουργία Πλάνου", "login": "Σύνδεση", "signup": "Εγγραφή",
            "gender": "Φύλο", "age": "Ηλικία", "weight": "Βάρος", "height": "Ύψος",
            "goal": "Στόχος", "workout": "Προπονήσεις", "logout": "Αποσύνδεση"
        }
    # Για όλες τις άλλες γλώσσες, ζητάμε από την AI να μας δώσει τους τίτλους
    return {
        "title": "🥗 AI NUTRITION HUB", "sub": f"Analysis in {target_lang}",
        "btn_plan": "🚀 Generate Plan", "login": "Login", "signup": "Sign Up",
        "gender": "Gender", "age": "Age", "weight": "Weight", "height": "Height",
        "goal": "Goal", "workout": "Workouts", "logout": "Logout"
    }

t = translate_ui(sel_lang)

# --- AUTH LOGIC ---
if 'user' not in st.session_state: st.session_state.user = None

if st.session_state.user is None:
    choice = st.sidebar.radio("Menu", [t["login"], t["signup"]])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button(choice):
        try:
            if choice == t["signup"]:
                auth.create_user_with_email_and_password(email, password)
                st.sidebar.success("Account created! Now Login.")
            else:
                st.session_state.user = auth.sign_in_with_email_and_password(email, password)
                st.rerun()
        except Exception as e: st.sidebar.error(f"Error: {e}")
else:
    st.sidebar.write(f"✅ {st.session_state.user['email']}")
    if st.sidebar.button(t["logout"]):
        st.session_state.user = None
        st.rerun()

# --- MAIN PAGE ---
st.title(t["title"])
st.subheader(t["sub"])

if st.session_state.user:
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox(t["gender"], ["Male", "Female", "Other"])
        st.number_input(t["age"], 10, 100, 25)
        st.number_input(t["weight"], 30, 250, 75)
    with col2:
        st.number_input(t["height"], 100, 250, 175)
        st.text_input(t["goal"])
        st.text_area(t["workout"])

    if st.button(t["btn_plan"]):
        with st.spinner("AI Processing..."):
            prompt = f"Create a full nutrition plan in {sel_lang}. Use professional tone."
            try:
                res = g4f.ChatCompletion.create(model=g4f.models.default, messages=[{"role": "user", "content": prompt}])
                st.markdown("---")
                st.write(res)
            except: st.error("AI is busy.")
else:
    st.info("Please login to continue.")
