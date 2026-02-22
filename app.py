import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
from datetime import datetime

# Charger le fichier .env
load_dotenv()

# Récupérer la clé API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configuration de la page
st.set_page_config(
    page_title="Ley.AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Traductions
TRANSLATIONS = {
    "Français": {
        "title": "Votre assistant personnel intelligent",
        "input_placeholder": "Posez-moi une question ou parlez...",
        "thinking": "Réflexion...",
        "save": "Sauvegarder",
        "clear": "Effacer",
        "help": "Aide",
        "messages": "Messages",
        "saved": "Conversation sauvegardée",
        "no_history": "Aucune conversation à sauvegarder !",
        "new_chat": "Nouvelle conversation démarrée !",
        "upload_image": "Télécharger une image",
        "upload_file": "Télécharger un fichier",
        "command_help": "Commandes disponibles",
        "personality": "Personnalité",
        "creativity": "Créativité",
        "commands": "Commandes",
        "stats": "Statistiques",
        "language": "Langue",
        "theme": "Thème",
        "dark": "Sombre",
        "light": "Clair",
        "auto": "Automatique",
    },
    "English": {
        "title": "Your personal AI assistant",
        "input_placeholder": "Ask me a question or speak...",
        "thinking": "Thinking...",
        "save": "Save",
        "clear": "Clear",
        "help": "Help",
        "messages": "Messages",
        "saved": "Conversation saved",
        "no_history": "No conversation to save!",
        "new_chat": "New conversation started!",
        "upload_image": "Upload an image",
        "upload_file": "Upload a file",
        "command_help": "Available commands",
        "personality": "Personality",
        "creativity": "Creativity",
        "commands": "Commands",
        "stats": "Statistics",
        "language": "Language",
        "theme": "Theme",
        "dark": "Dark",
        "light": "Light",
        "auto": "Auto",
    },
    "Español": {
        "title": "Tu asistente personal de IA",
        "input_placeholder": "Hazme una pregunta o habla...",
        "thinking": "Pensando...",
        "save": "Guardar",
        "clear": "Borrar",
        "help": "Ayuda",
        "messages": "Mensajes",
        "saved": "Conversación guardada",
        "no_history": "¡Sin conversación para guardar!",
        "new_chat": "¡Nueva conversación iniciada!",
        "upload_image": "Subir una imagen",
        "upload_file": "Subir un archivo",
        "command_help": "Comandos disponibles",
        "personality": "Personalidad",
        "creativity": "Creatividad",
        "commands": "Comandos",
        "stats": "Estadísticas",
        "language": "Idioma",
        "theme": "Tema",
        "dark": "Oscuro",
        "light": "Claro",
        "auto": "Automático",
    },
}

# Personnalités disponibles
PERSONALITIES = {
    "Français": {
        "Amical": """Tu es Ley.AI, un assistant conversationnel amical et serviable.
        Tu es chaleureux, patient et toujours souriant.
        Tu aimes aider les gens et tu réponds avec enthousiasme.""",
        
        "Professionnel": """Tu es Ley.AI, un assistant professionnel.
        Tu es précis, concis et敬.
        Tu donnes des réponses structurées et professionnelles.""",
        
        "Drôle": """Tu es Ley.AI, un assistant amusant et spirituel.
        Tu aimes faire des blagues et garder une ambiance légère.
        Tu es créatif et original dans tes réponses.""",
        
        "Tuteur": """Tu es Ley.AI, un professeur patient et encourageant.
        Tu expliques les choses clairement et simplement.
        Tu poses des questions pour aider à comprendre et donnes des exemples.""",
        
        "Expert": """Tu es Ley.AI, un expert en tout.
        Tu donnes des réponses détaillées et approfondies.
        Tu partages des connaissances avancées et des sources.""",
    },
    "English": {
        "Amical": """You are Ley.AI, a friendly and helpful conversational assistant.
        You are warm, patient, and always smiling.
        You love helping people and respond with enthusiasm.""",
        
        "Professionnel": """You are Ley.AI, a professional assistant.
        You are precise, concise, and敬.
        You give structured and professional answers.""",
        
        "Drôle": """You are Ley.AI, a fun and witty assistant.
        You love making jokes and keeping a light atmosphere.
        You are creative and original in your responses.""",
        
        "Tuteur": """You are Ley.AI, a patient and encouraging teacher.
        You explain things clearly and simply.
        You ask questions to help understand and give examples.""",
        
        "Expert": """You are Ley.AI, an expert in everything.
        You give detailed and in-depth answers.
        You share advanced knowledge and sources.""",
    },
    "Español": {
        "Amical": """Eres Ley.AI, un asistente conversacional amable y servicial.
        Eres cálido, paciente y siempre sonriente.
        Te encanta ayudar a las personas y respondes con entusiasmo.""",
        
        "Professionnel": """Eres Ley.AI, un asistente profesional.
        Eres preciso, conciso y敬.
        Das respuestas estructuradas y profesionales.""",
        
        "Drôle": """Eres Ley.AI, un asistente divertido y ingenioso.
        Te encanta hacer bromas y mantener un ambiente ligero.
        Eres creativo y original en tus respuestas.""",
        
        "Tuteur": """Eres Ley.AI, un profesor paciente y animador.
        Explicas las cosas de forma clara y sencilla.
        Haces preguntas para ayudar a entender y das ejemplos.""",
        
        "Expert": """Eres Ley.AI, un experto en todo.
        Das respuestas detalladas y profundas.
        Compartes conocimientos avanzados y fuentes.""",
    },
}

# Initialiser l'historique
if "history" not in st.session_state:
    st.session_state.history = []
if "personality" not in st.session_state:
    st.session_state.personality = "Amical"
if "chat_saved" not in st.session_state:
    st.session_state.chat_saved = False
if "language" not in st.session_state:
    st.session_state.language = "Français"
if "theme" not in st.session_state:
    st.session_state.theme = "Auto"

# Obtenir les traductions
t = TRANSLATIONS[st.session_state.language]
personality_dict = PERSONALITIES[st.session_state.language]

# Appliquer le thème
if st.session_state.theme == "Dark":
    st.markdown("""
    <style>
    .stApp {background-color: #0e1117;}
    section[data-testid="stSidebar"] {background-color: #1a1a2e;}
    </style>
    """, unsafe_allow_html=True)
elif st.session_state.theme == "Light":
    st.markdown("""
    <style>
    .stApp {background-color: #ffffff;}
    section[data-testid="stSidebar"] {background-color: #f0f0f0;}
    </style>
    """, unsafe_allow_html=True)

# Titre principal
st.title("🤖 Ley.AI")
st.caption(t["title"])

# Sidebar avec les options
with st.sidebar:
    st.header("⚙️ " + t["commands"])
    
    # Langue
    st.subheader("🌐 " + t["language"])
    language = st.selectbox(
        t["language"],
        ["Français", "English", "Español"],
        index=["Français", "English", "Español"].index(st.session_state.language)
    )
    
    if language != st.session_state.language:
        st.session_state.language = language
        st.rerun()
    
    # Thème
    st.subheader("🎨 " + t["theme"])
    theme = st.selectbox(
        t["theme"],
        [t["auto"], t["dark"], t["light"]],
        index=["Auto", "Dark", "Light"].index(st.session_state.theme)
    )
    
    if theme == t["dark"]:
        st.session_state.theme = "Dark"
    elif theme == t["light"]:
        st.session_state.theme = "Light"
    else:
        st.session_state.theme = "Auto"
    
    # Choisir la personnalité
    st.subheader("🎭 " + t["personality"])
    personality = st.selectbox(
        t["personality"],
        list(personality_dict.keys()),
        index=list(personality_dict.keys()).index(st.session_state.personality)
    )
    
    if personality != st.session_state.personality:
        st.session_state.personality = personality
        st.session_state.history = []
        st.rerun()
    
    # Température
    st.subheader("🌡️ " + t["creativity"])
    temperature = st.slider(t["creativity"], 0.0, 2.0, 0.7, 0.1)
    
    # Boutons de commandes
    st.subheader("📋 " + t["commands"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 " + t["save"]):
            if st.session_state.history:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"conversation_{timestamp}.txt"
                
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"Conversation with Ley.AI - {timestamp}\n")
                    f.write("=" * 50 + "\n\n")
                    for role, content in st.session_state.history:
                        role_name = "You" if role == "user" else "Ley.AI"
                        f.write(f"{role_name}: {content}\n\n")
                
                st.session_state.chat_saved = True
                st.success(f"💾 {t['saved']}: {filename}")
            else:
                st.warning(t["no_history"])
    
    with col2:
        if st.button("🗑️ " + t["clear"]):
            st.session_state.history = []
            st.session_state.chat_saved = False
            st.rerun()
    
    # Bouton aide
    if st.button("❓ " + t["help"]):
        st.info(f"""
        **{t['command_help']}**
        
        - {t['input_placeholder']}
        - /aide - {t['help']}
        - /save - {t['save']}
        - /clear - {t['clear']}
        - /new - {t['new_chat']}
        
        **{t['personality']}:**
        - Amical, Professionnel, Drôle, Tuteur, Expert
        """)
    
    # Statistiques
    st.subheader("📊 " + t["stats"])
    if st.session_state.history:
        st.write(f"{t['messages']}: {len(st.session_state.history) // 2}")
    else:
        st.write(f"{t['messages']}: 0")
    
    if st.session_state.chat_saved:
        st.success("✅ " + t["saved"])

# Afficher les messages
for role, content in st.session_state.history:
    with st.chat_message(role):
        st.write(content)

# Zone de saisie avec voix
st.subheader("💬 " + t["input_placeholder"])

# Option voix
use_voice = st.checkbox("🎤 Mode voix")

if use_voice:
    audio_value = st.audio_input("Parlez maintenant...")
    if audio_value:
        st.info("🎤 Voix détectée ! (La transcription sera bientôt disponible)")
        prompt = st.text_input(t["input_placeholder"], key="text_input")
    else:
        prompt = st.chat_input(t["input_placeholder"])
else:
    prompt = st.chat_input(t["input_placeholder"])

# Upload d'images
with st.expander("🖼️ " + t["upload_image"]):
    uploaded_image = st.file_uploader(t["upload_image"], type=["jpg", "jpeg", "png", "gif"])
    if uploaded_image:
        st.image(uploaded_image, caption="Image uploadée", use_container_width=True)

# Upload de fichiers
with st.expander("📁 " + t["upload_file"]):
    uploaded_file = st.file_uploader(t["upload_file"], type=["txt", "pdf", "doc", "py", "json", "csv"])
    if uploaded_file:
        st.success(f"📁 Fichier uploadé: {uploaded_file.name}")

# Traitement du message
if prompt:
    # Vérifier les commandes spéciales
    is_command = False
    
    if prompt.lower() in ["/aide", "/help", "/ayuda"]:
        st.info(f"""
        **{t['command_help']}**
        
        - {t['input_placeholder']}
        - /aide - {t['help']}
        - /save - {t['save']}
        - /clear - {t['clear']}
        - /new - {t['new_chat']}
        
        **{t['personality']}:**
        - Amical, Professionnel, Drôle, Tuteur, Expert
        """)
        is_command = True
    
    elif prompt.lower() in ["/save", "/sauvegarder", "/guardar"]:
        if st.session_state.history:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Conversation with Ley.AI - {timestamp}\n")
                f.write("=" * 50 + "\n\n")
                for role, content in st.session_state.history:
                    role_name = "You" if role == "user" else "Ley.AI"
                    f.write(f"{role_name}: {content}\n\n")
            st.success(f"💾 {t['saved']}: {filename}")
        else:
            st.warning(t["no_history"])
        is_command = True
    
    elif prompt.lower() in ["/clear", "/effacer", "/borrar"]:
        st.session_state.history = []
        st.session_state.chat_saved = False
        st.rerun()
        is_command = True
    
    elif prompt.lower() in ["/new", "/nouvelle", "/nueva"]:
        st.session_state.history = []
        st.session_state.chat_saved = False
        st.success("✨ " + t["new_chat"])
        is_command = True
    
    if not is_command:
        # Afficher le message de l'utilisateur
        with st.chat_message("user"):
            st.write(prompt)
        
        st.session_state.history.append(("user", prompt))
        
        # Envoyer à Groq
        with st.spinner("🤔 " + t["thinking"]):
            try:
                client = Groq(api_key=GROQ_API_KEY)
                
                messages = [{"role": "system", "content": personality_dict[personality]}]
                
                for role, content in st.session_state.history:
                    if role == "user":
                        messages.append({"role": "user", "content": content})
                    else:
                        messages.append({"role": "assistant", "content": content})
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=temperature
                )
                
                ai_response = response.choices[0].message.content
                
            except Exception as e:
                ai_response = f"Erreur : {str(e)}"
        
        # Afficher la réponse
        with st.chat_message("assistant"):
            st.write(ai_response)
        
        st.session_state.history.append(("assistant", ai_response))
