import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid

# Charger le fichier .env
load_dotenv()

# Récupérer la clé API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configuration de la page - Style ChatGPT
st.set_page_config(
    page_title="Ley.AI - Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS - Interface ChatGPT
st.markdown("""
<style>
    /* Import字体 */
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600&display=swap');
    
    /* Style général */
    * {
        font-family: 'Sora', sans-serif;
    }
    
    /* Fond sombre style ChatGPT */
    .stApp {
        background-color: #171717;
        color: #ececec;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #202123;
        width: 260px !important;
    }
    
    /* Messages utilisateur */
    div[data-testid="chat-message-user"] {
        background-color: #2f2f2f !important;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    /* Messages assistant */
    div[data-testid="chat-message-assistant"] {
        background-color: #171717 !important;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    /* Zone de saisie */
    div[data-testid="stChatInput"] {
        background-color: #2f2f2f;
        border-radius: 12px;
        border: 1px solid #3f3f3f;
    }
    
    /* Boutons sidebar */
    .sidebar-button {
        background-color: transparent;
        border: 1px solid #3f3f3f;
        border-radius: 8px;
        padding: 12px;
        width: 100%;
        text-align: left;
        color: #ececec;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .sidebar-button:hover {
        background-color: #2f2f2f;
    }
    
    /* Nouveau chat button */
    .new-chat-btn {
        background-color: #10a37f;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px;
        width: 100%;
        font-weight: 600;
        cursor: pointer;
    }
    
    .new-chat-btn:hover {
        background-color: #0d8b6e;
    }
    
    /* Titres */
    h1, h2, h3 {
        color: #ececec !important;
    }
    
    /* Description sidebar */
    .sidebar-section {
        padding: 10px;
        color: #8e8e8e;
        font-size: 12px;
    }
    
    /* Input focus */
    textarea:focus {
        outline: 2px solid #10a37f !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #171717;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3f3f3f;
        border-radius: 4px;
    }
    
    /* Chat input container */
    .chat-input-container {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        max-width: 800px;
    }
    
    /* Logo style */
    .logo-text {
        font-size: 20px;
        font-weight: 700;
        color: #ececec;
    }
    
    /* Settings panel */
    .settings-panel {
        background-color: #2f2f2f;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Personnalités disponibles
PERSONALITIES = {
    "🤖 Assistant": """Tu es Ley.AI, un assistant intelligent et utile.
    Tu réponds de manière claire, concise et helpful.
    Tu es toujours poli et professionnel.""",
    
    "😊 Amical": """Tu es Ley.AI, un ami virtuel chaleureux et attentionné.
    Tu es toujours de bonne humeur et aimes discuter.""",
    
    "🎓 Tuteur": """Tu es Ley.AI, un professeur patient et pédagogue.
    Tu expliques tout en détail et tu adaptes ton niveau.""",
    
    "😄 Drôle": """Tu es Ley.AI, un ami spirituel et marrant.
    Tu fais des blagues et garderas toujours une ambiance légère.""",
    
    "💼 Professionnel": """Tu es Ley.AI, un expert professionnel.
    Tu donnes des réponses structurées et très détaillées.""",
}

# Langues
LANGUAGES = {
    "Français": "fr",
    "English": "en", 
    "Español": "es",
}

# Initialiser les sessions
if "conversations" not in st.session_state:
    st.session_state.conversations = {}
    st.session_state.current_conversation = None

if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = str(uuid.uuid4())
    st.session_state.conversations[st.session_state.current_conversation] = {
        "messages": [],
        "personality": "🤖 Assistant"
    }

if "show_settings" not in st.session_state:
    st.session_state.show_settings = False

# Obtenir la conversation actuelle
current_conv = st.session_state.conversations[st.session_state.current_conversation]

# Fonction pour créer une nouvelle conversation
def new_chat():
    new_id = str(uuid.uuid4())
    st.session_state.conversations[new_id] = {
        "messages": [],
        "personality": "🤖 Assistant"
    }
    st.session_state.current_conversation = new_id
    st.rerun()

# Fonction pour changer de conversation
def switch_conversation(conv_id):
    st.session_state.current_conversation = conv_id
    st.rerun()

# SIDEBAR - Style ChatGPT
with st.sidebar:
    # Logo
    st.markdown(f"""
    <div style="padding: 10px; text-align: center;">
        <span class="logo-text">🤖 Ley.AI</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Bouton nouveau chat
    if st.button("➕ Nouveau Chat", key="new_chat"):
        new_chat()
    
    st.markdown("---")
    
    # Titre conversations
    st.markdown("### 🗂️ Conversations")
    
    # Liste des conversations
    for conv_id, conv_data in reversed(st.session_state.conversations.items()):
        conv_title = f"Chat {list(st.session_state.conversations.keys()).index(conv_id) + 1}"
        
        if len(conv_data["messages"]) > 0:
            # Prendre le premier message comme titre
            first_msg = conv_data["messages"][0][1][:30] + "..."
            conv_title = first_msg
        
        btn_key = f"conv_{conv_id}"
        
        if st.button(f"💬 {conv_title}", key=btn_key):
            switch_conversation(conv_id)
    
    st.markdown("---")
    
    # Paramètres
    if st.button("⚙️ Paramètres"):
        st.session_state.show_settings = not st.session_state.show_settings
    
    if st.session_state.show_settings:
        st.markdown("### ⚙️ Paramètres")
        
        # Personnalité
        selected_personality = st.selectbox(
            "Personnalité",
            list(PERSONALITIES.keys()),
            index=list(PERSONALITIES.keys()).index(current_conv["personality"])
        )
        
        if selected_personality != current_conv["personality"]:
            current_conv["personality"] = selected_personality
            st.rerun()
        
        # Température
        temperature = st.slider("Créativité", 0.0, 2.0, 0.7, 0.1)
        
        # Effacer conversation
        if st.button("🗑️ Effacer cette conversation"):
            if len(st.session_state.conversations) > 1:
                del st.session_state.conversations[st.session_state.current_conversation]
                new_chat()
            else:
                current_conv["messages"] = []
                st.rerun()

# MAIN CHAT AREA
# Titre de la conversation
st.markdown(f"""
<div style="padding: 20px; text-align: center;">
    <h2 style="margin: 0;">{current_conv['personality']}</h2>
</div>
""", unsafe_allow_html=True)

# Afficher les messages
chat_container = st.container()

with chat_container:
    for role, content in current_conv["messages"]:
        with st.chat_message(role):
            st.write(content)

# Zone de saisie en bas
st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

# Input area style ChatGPT
col1, col2, col3 = st.columns([8, 1, 1])

with col1:
    prompt = st.chat_input("Envoyez un message à Ley.AI...")

with col2:
    if st.button("🎤"):
        st.info("Mode voix bientôt disponible!")

with col3:
    if st.button("📎"):
        st.info("Upload de fichiers bientôt disponible!")

# Traiter le message
if prompt:
    # Ajouter le message utilisateur
    current_conv["messages"].append(("user", prompt))
    
    # Envoyer à Groq
    with st.spinner("Réflexion..."):
        try:
            client = Groq(api_key=GROQ_API_KEY)
            
            messages = [{"role": "system", "content": PERSONALITIES[current_conv["personality"]]}]
            
            for role, content in current_conv["messages"]:
                messages.append({"role": role, "content": content})
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=temperature
            )
            
            ai_response = response.choices[0].message.content
            
        except Exception as e:
            ai_response = f"Erreur: {str(e)}"
    
    # Ajouter la réponse
    current_conv["messages"].append(("assistant", ai_response))
    
    # Rerun pour afficher
    st.rerun()

# Premier message d'accueil
if len(current_conv["messages"]) == 0:
    st.markdown("""
    <div style="text-align: center; padding: 50px 20px;">
        <h1 style="font-size: 60px;">🤖</h1>
        <h2>Comment puis-je vous aider aujourd'hui ?</h2>
        <p style="color: #8e8e8e;">
            Vous pouvez me poser des questions, me demander de vous aider avec du code,<br>
            de l'écriture, ou simplement discuter!
        </p>
    </div>
    """, unsafe_allow_html=True)
