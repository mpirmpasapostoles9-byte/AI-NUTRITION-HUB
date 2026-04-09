import streamlit as st
import g4f
import pyrebase

# --- FIREBASE CONFIG (Από τις φωτό σου) ---
firebase_config = {
    "apiKey": "AIzaSyCjYgrcFDBwx4CZtEt-bTFrAFdX1D64pMQ",
    "authDomain": "ai-nutrition-hub.firebaseapp.com",
    "projectId": "ai-nutrition-hub",
    "storageBucket": "ai-nutrition-hub.firebasestorage.app",
    "messagingSenderId": "955664360747",
    "appId": "1:955664360747:web:01794faf60b5001886916e"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# --- Η ΛΙΣΤΑ ΜΕ ΤΙΣ ΓΛΩΣΣΕΣ ---
all_langs = [
    "Greek", "English", "Spanish", "French", "German", "Italian", "Portuguese", 
    "Russian", "Chinese", "Japanese", "Arabic", "Turkish", "Hindi", "Dutch", 
    "Swedish", "Norwegian", "Danish", "Finnish", "Polish", "Romanian"
] # Μπορείς να προσθέσεις όσες θέλεις

# --- ΜΗΧΑΝΙΣΜΟΣ ΔΥΝΑΜΙΚΗΣ ΜΕΤΑΦΡΑΣΗΣ UI ---
# Εδώ ορίζουμε τις βασικές λέξεις. Η AI θα αναλάβει να τις "μεταφράσει" στο UI.
def get_ui_translation(lang):
    translations = {
        "Greek": {
            "title": "🥗 AI NUTRITION HUB", "login": "Είσοδος", "signup": "Εγγραφή",
            "gender": "Φύλο", "age": "Ηλικία", "weight": "Βάρος", "height": "Ύψος",
            "activity": "Δραστηριότητα", "goal": "Στόχος", "workout": "Προπονήσεις",
            "btn": "🚀 Δημιουργία Πλάνου", "logout": "Αποσύνδεση"
        },
        "English": {
            "title": "🥗 AI NUTRITION HUB", "login": "Login", "signup": "Sign Up",
            "gender": "Gender", "age": "Age", "weight": "Weight", "height": "Height",
            "activity": "Activity", "goal": "Goal", "workout": "Workouts",
            "btn": "🚀 Create Plan", "logout": "Logout"
        },
        "Spanish": {
            "title": "🥗 AI NUTRITION HUB", "login": "Acceso", "signup": "Registro",
            "gender": "Género", "age": "Edad", "weight": "Peso", "height": "Altura",
            "activity": "Actividad", "goal": "Objetivo", "workout": "Entrenamiento",
            "btn": "🚀 Crear Plan", "logout": "Cerrar sesión"
        },
        "French": {
            "title": "🥗 AI NUTRITION HUB", "login": "Connexion", "signup": "S'inscrire",
            "gender": "Genre", "age": "Âge", "weight": "Poids", "height": "Taille",
            "activity": "Activité", "goal": "Objectif", "workout": "Entraînement",
            "btn": "🚀 Créer le Plan", "logout": "Déconnexion"
        },
        "German": {
            "title": "🥗 AI NUTRITION HUB", "login": "Anmelden", "signup": "Registrieren",
            "gender": "Geschlecht", "age": "Alter", "weight": "Gewicht", "height": "Größe",
            "activity": "Aktivität", "goal": "Ziel", "workout": "Training",
            "btn": "🚀 Plan erstellen", "logout": "Abmelden"
        }
    }
    # Αν η γλώσσα δεν υπάρχει στις πάνω, δίνουμε Αγγλικά ως βάση
    return translations.get(lang, translations["English"])

st.set_page_config(page_title="AI NUTRITION HUB", layout="wide")

# --- SIDEBAR: ΑΝΑΖΗΤΗΣΗ ΓΛΩΣΣΑΣ ---
st.sidebar.title("🌐 Language Settings")
user_lang = st.sidebar.selectbox("Choose Language", all_langs, index=0)
t = get_ui_translation(user_lang)

if 'user' not in st.session_state: st.session_state.user = None

# --- AUTHENTICATION ---
st.sidebar.markdown("---")
if st.session_state.user is None:
    mode = st.sidebar.radio("Mode", [t["login"], t["signup"]])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button(mode):
        try:
            if mode == t["signup"]:
                auth.create_user_with_email_and_password(email, password)
                st.sidebar.success("Success! Now Login.")
            else:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.user = user
                st.rerun()
        except Exception as e: st.sidebar.error(f"Error: {e}")
else:
    st.sidebar.write(f"✅ {st.session_state.user['email']}")
    if st.sidebar.button(t["logout"]):
        st.session_state.user = None
        st.rerun()

# --- MAIN PAGE ---
st.title(t["title"])

if st.session_state.user:
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox(t["gender"], ["Male/Homme/Άνδρας", "Female/Femme/Γυναίκα"])
        st.number_input(t["age"], 10, 100, 25)
        st.number_input(t["weight"], 30, 250, 75)
    with col2:
        st.number_input(t["height"], 100, 250, 175)
        st.selectbox(t["activity"], ["1", "2", "3", "4"])
        st.text_input(t["goal"])
    
    workout = st.text_area(t["workout"])

    if st.button(t["btn"]):
        with st.spinner("Generating..."):
            prompt = f"Create a nutrition plan. Language: {user_lang}. User info: {workout}"
            try:
                res = g4f.ChatCompletion.create(model=g4f.models.default, messages=[{"role": "user", "content": prompt}])
                st.markdown("---")
                st.write(res)
            except: st.error("AI Busy, try again.")
else:
    st.warning("Please Login / Παρακαλώ συνδεθείτε")
