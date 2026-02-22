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

# Styles CSS personnalisés
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
    }
    
    h1 {
        color: #FF4B4B;
        text-align: center;
    }
    
    .stCaption {
        text-align: center;
        color: #888;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #1a1a2e;
    }
</style>
""", unsafe_allow_html=True)

# Personnalités disponibles
PERSONALITIES = {
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
}

# Initialiser l'historique
if "history" not in st.session_state:
    st.session_state.history = []
if "personality" not in st.session_state:
    st.session_state.personality = "Amical"
if "chat_saved" not in st.session_state:
    st.session_state.chat_saved = False

# Titre principal
st.title("🤖 Ley.AI")
st.caption("Votre assistant personnel intelligent")

# Sidebar avec les options
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    # Choisir la personnalité
    st.subheader("🎭 Personnalité")
    personality = st.selectbox(
        "Choisissez une personnalité",
        list(PERSONALITIES.keys()),
        index=list(PERSONALITIES.keys()).index(st.session_state.personality)
    )
    
    if personality != st.session_state.personality:
        st.session_state.personality = personality
        st.session_state.history = []
        st.rerun()
    
    # Température
    st.subheader("🌡️ Créativité")
    temperature = st.slider("Température", 0.0, 2.0, 0.7, 0.1)
    
    # Boutons de commandes
    st.subheader("📋 Commandes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Sauvegarder"):
            if st.session_state.history:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"conversation_{timestamp}.txt"
                
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"Conversation avec Ley.AI - {timestamp}\n")
                    f.write("=" * 50 + "\n\n")
                    for role, content in st.session_state.history:
                        role_name = "Vous" if role == "user" else "Ley.AI"
                        f.write(f"{role_name}: {content}\n\n")
                
                st.session_state.chat_saved = True
                st.success(f"💾 Sauvegardé dans {filename}")
            else:
                st.warning("Aucune conversation à sauvegarder !")
    
    with col2:
        if st.button("🗑️ Effacer"):
            st.session_state.history = []
            st.session_state.chat_saved = False
            st.rerun()
    
    # Bouton aide
    if st.button("❓ Aide"):
        st.info("""
        **Commandes disponibles :**
        
        - Tapez normalement pour discuter
        - /aide - Afficher cette aide
        - /sauvegarder - Sauvegarder la conversation
        - /effacer - Effacer l'historique
        - /nouvelle - Nouvelle conversation
        
        **Personnalités disponibles :**
        - Amical, Professionnel, Drôle, Tuteur, Expert
        """)
    
    # Statistiques
    st.subheader("📊 Statistiques")
    if st.session_state.history:
        st.write(f"Messages : {len(st.session_state.history) // 2}")
    else:
        st.write("Messages : 0")
    
    if st.session_state.chat_saved:
        st.success("✅ Conversation sauvegardée")

# Afficher les messages
for role, content in st.session_state.history:
    with st.chat_message(role):
        st.write(content)

# Zone de saisie
if prompt := st.chat_input("Posez-moi une question..."):
    # Vérifier les commandes spéciales
    is_command = False
    
    if prompt.lower() == "/aide":
        st.info("""
        **Commandes disponibles :**
        
        - Tapez normalement pour discuter
        - /aide - Afficher cette aide
        - /sauvegarder - Sauvegarder la conversation
        - /effacer - Effacer l'historique
        - /nouvelle - Nouvelle conversation
        
        **Personnalités disponibles :**
        - Amical, Professionnel, Drôle, Tuteur, Expert
        """)
        is_command = True
    
    elif prompt.lower() == "/sauvegarder":
        if st.session_state.history:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Conversation avec Ley.AI - {timestamp}\n")
                f.write("=" * 50 + "\n\n")
                for role, content in st.session_state.history:
                    role_name = "Vous" if role == "user" else "Ley.AI"
                    f.write(f"{role_name}: {content}\n\n")
            st.success(f"💾 Sauvegardé dans {filename}")
        else:
            st.warning("Aucune conversation à sauvegarder !")
        is_command = True
    
    elif prompt.lower() == "/effacer":
        st.session_state.history = []
        st.session_state.chat_saved = False
        st.rerun()
        is_command = True
    
    elif prompt.lower() == "/nouvelle":
        st.session_state.history = []
        st.session_state.chat_saved = False
        st.success("✨ Nouvelle conversation démarrée !")
        is_command = True
    
    # Si c'est une commande, on arrête ici
    if is_command:
        pass
    
    else:
        # Afficher le message de l'utilisateur
        with st.chat_message("user"):
            st.write(prompt)
        
        st.session_state.history.append(("user", prompt))
        
        # Envoyer à Groq
        with st.spinner("🤔 Réflexion..."):
            try:
                client = Groq(api_key=GROQ_API_KEY)
                
                messages = [{"role": "system", "content": PERSONALITIES[personality]}]
                
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
