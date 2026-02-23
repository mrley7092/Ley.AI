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
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600&display=swap');
    
    * {
        font-family: 'Sora', sans-serif;
    }
    
    .stApp {
        background-color: #171717;
        color: #ececec;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #202123;
        width: 260px !important;
    }
    
    div[data-testid="chat-message-user"] {
        background-color: #2f2f2f !important;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    div[data-testid="chat-message-assistant"] {
        background-color: #171717 !important;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    h1, h2, h3 {
        color: #ececec !important;
    }
    
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
</style>
""", unsafe_allow_html=True)

# Personnalités disponibles
PERSONALITIES = {
    "🤖 Assistant": """Tu es Ley.AI, un assistant intelligent et utile.
    Tu réponds de manière claire, concise et helpful.""",
    
    "😊 Amical": """Tu es Ley.AI, un ami virtuel chaleureux et attentionné.
    Tu es toujours de bonne humeur.""",
    
    "🎓 Tuteur": """Tu es Ley.AI, un professeur patient et pédagogue.
    Tu expliques tout en détail.""",
    
    "😄 Drôle": """Tu es Ley.AI, un ami spirituel et marrant.
    Tu fais des blagues.""",
    
    "💼 Professionnel": """Tu es Ley.AI, un expert professionnel.
    Tu donnes des réponses structurées.""",
}

# Initialiser les sessions - CORRECTION
if "conversations" not in st.session_state:
    st.session_state.conversations = {}

if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = str(uuid.uuid4())

# Créer la conversation si elle n'existe pas
if st.session_state.current_conversation not in st.session_state.conversations:
    st.session_state.conversations[st.session_state.current_conversation] = {
        "messages": [],
        "personality": "🤖 Assistant"
    }

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

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px; text-align: center;">
        <h2 style="margin: 0;">🤖 Ley.AI</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("➕ Nouveau Chat"):
        new_chat()
    
    st.markdown("### 🗂️ Conversations")
    
    for conv_id in list(st.session_state.conversations.keys())[-5:]:
        conv_num = list(st.session_state.conversations.keys()).index(conv_id) + 1
        if st.button(f"💬 Chat {conv_num}"):
            st.session_state.current_conversation = conv_id
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Paramètres")
    
    selected_personality = st.selectbox(
        "Personnalité",
        list(PERSONALITIES.keys()),
        index=list(PERSONALITIES.keys()).index(current_conv["personality"])
    )
    
    if selected_personality != current_conv["personality"]:
        current_conv["personality"] = selected_personality
    
    temperature = st.slider("Créativité", 0.0, 2.0, 0.7, 0.1)
    
    if st.button("🗑️ Effacer"):
        current_conv["messages"] = []
        st.rerun()

# MAIN CHAT
st.markdown(f"""
<div style="padding: 20px; text-align: center;">
    <h2>{current_conv['personality']}</h2>
</div>
""", unsafe_allow_html=True)

# Afficher les messages
for role, content in current_conv["messages"]:
    with st.chat_message(role):
        st.write(content)

# Zone de saisie
prompt = st.chat_input("Envoyez un message à Ley.AI...")

# Traiter le message
if prompt:
    current_conv["messages"].append(("user", prompt))
    
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
    
    current_conv["messages"].append(("assistant", ai_response))
    st.rerun()

# Message d'accueil
if len(current_conv["messages"]) == 0:
    st.markdown("""
    <div style="text-align: center; padding: 50px 20px;">
        <h1 style="font-size: 60px;">🤖</h1>
        <h2>Comment puis-je vous aider aujourd'hui ?</h2>
    </div>
    """, unsafe_allow_html=True)
