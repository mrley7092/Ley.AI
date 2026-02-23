import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import uuid

# Charger le fichier .env
load_dotenv()

# Récupérer la clé API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configuration de la page
st.set_page_config(
    page_title="Ley.AI - Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== STYLES CSS AVEC THEMES =====
THEMES = {
    "ChatGPT (Sombre)": {
        "bg": "#171717", "sidebar": "#202123", "user_msg": "#2f2f2f", 
        "text": "#ececec", "accent": "#10a37f"
    },
    "Bleu Nuit": {
        "bg": "#0a0e1f", "sidebar": "#0d1425", "user_msg": "#1a2744",
        "text": "#e0e6ed", "accent": "#3b82f6"
    },
    "Violet Dream": {
        "bg": "#1a1025", "sidebar": "#251535", "user_msg": "#352045",
        "text": "#e0d0f0", "accent": "#a855f7"
    },
    "Vert Nature": {
        "bg": "#0a1a0f", "sidebar": "#0f2515", "user_msg": "#153525",
        "text": "#d0f0d8", "accent": "#22c55e"
    },
    "Coucher de Soleil": {
        "bg": "#1a0f0a", "sidebar": "#251510", "user_msg": "#352015",
        "text": "#f0e0d0", "accent": "#f97316"
    },
    "Clair": {
        "bg": "#ffffff", "sidebar": "#f5f5f5", "user_msg": "#e5e5e5",
        "text": "#1a1a1a", "accent": "#10a37f"
    },
}

# Thème actuel
if "theme" not in st.session_state:
    st.session_state.theme = "ChatGPT (Sombre)"

theme = THEMES[st.session_state.theme]

# Appliquer le thème
st.markdown(f"""
<style>
    .stApp {{
        background-color: {theme['bg']};
        color: {theme['text']};
    }}
    
    section[data-testid="stSidebar"] {{
        background-color: {theme['sidebar']};
        width: 260px !important;
    }}
    
    div[data-testid="chat-message-user"] {{
        background-color: {theme['user_msg']} !important;
        padding: 15px 20px;
        border-radius: 12px;
    }}
    
    div[data-testid="chat-message-assistant"] {{
        background-color: {theme['bg']} !important;
        padding: 15px 20px;
        border-radius: 12px;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .animated {{
        animation: fadeIn 0.3s ease-in-out;
    }}
    
    .badge {{
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin: 3px;
        background-color: {theme['accent']};
    }}
</style>
""", unsafe_allow_html=True)

# ===== TRADUCTIONS =====
TRANSLATIONS = {
    "Français": {"welcome": "Comment puis-je vous aider ?", "thinking": "Réflexion..."},
    "English": {"welcome": "How can I help you?", "thinking": "Thinking..."},
    "Español": {"welcome": "¿Cómo puedo ayudarte?", "thinking": "Pensando..."},
}

# ===== PERSONNALITÉS =====
PERSONALITIES = {
    "🤖 Assistant": "Tu es Ley.AI, un assistant intelligent et utile.",
    "😊 Amical": "Tu es Ley.AI, un ami chaleureux et attentionné.",
    "🎓 Tuteur": "Tu es Ley.AI, un professeur patient.",
    "😄 Drôle": "Tu es Ley.AI, un ami spirituel.",
    "💼 Professionnel": "Tu es Ley.AI, un expert professionnel.",
}

# ===== INITIALISER SESSIONS =====
if "conversations" not in st.session_state:
    st.session_state.conversations = {}
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = str(uuid.uuid4())
if st.session_state.current_conversation not in st.session_state.conversations:
    st.session_state.conversations[st.session_state.current_conversation] = {
        "messages": [], "personality": "🤖 Assistant"
    }
if "stats" not in st.session_state:
    st.session_state.stats = {"messages": 0, "chats": 1}
if "language" not in st.session_state:
    st.session_state.language = "Français"
if "calc_result" not in st.session_state:
    st.session_state.calc_result = ""

current_conv = st.session_state.conversations[st.session_state.current_conversation]

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown(f"""<h2 style='text-align:center;'>🤖 Ley.AI</h2>""", unsafe_allow_html=True)
    
    # Badges statistiques
    st.markdown(f"""
    <div style='text-align:center;'>
        <span class='badge'>💬 {st.session_state.stats['messages']} msgs</span>
        <span class='badge'>🔥 {st.session_state.stats['chats']} chats</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("➕ Nouveau Chat", key="new_chat"):
        new_id = str(uuid.uuid4())
        st.session_state.conversations[new_id] = {"messages": [], "personality": "🤖 Assistant"}
        st.session_state.current_conversation = new_id
        st.session_state.stats["chats"] += 1
        st.rerun()
    
    st.markdown("---")
    
    # Paramètres
    st.markdown("### ⚙️ Paramètres")
    
    # Thème
    theme_name = st.selectbox("🎨 Thème", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.theme), key="theme_select")
    if theme_name != st.session_state.theme:
        st.session_state.theme = theme_name
        st.rerun()
    
    # Personnalité
    personality = st.selectbox("🎭 Personnalité", list(PERSONALITIES.keys()), 
                               index=list(PERSONALITIES.keys()).index(current_conv["personality"]), key="personality_select")
    if personality != current_conv["personality"]:
        current_conv["personality"] = personality
    
    # Créativité
    temperature = st.slider("🌡️ Créativité", 0.0, 2.0, 0.7, 0.1, key="temp_slider")
    
    # Langue
    lang = st.selectbox("🌐 Langue", ["Français", "English", "Español"], 
                       index=["Français", "English", "Español"].index(st.session_state.language), key="lang_select")
    if lang != st.session_state.language:
        st.session_state.language = lang
        st.rerun()
    
    # Effacer
    if st.button("🗑️ Effacer", key="clear_btn"):
        current_conv["messages"] = []
        st.rerun()

# ===== MAIN CHAT =====
t = TRANSLATIONS[st.session_state.language]

st.markdown(f"""<h2 style='text-align:center;'>{current_conv['personality']}</h2>""", unsafe_allow_html=True)

# Afficher messages
for role, content in current_conv["messages"]:
    with st.chat_message(role):
        st.write(content)

# Zone saisie
prompt = st.chat_input(t["welcome"])

if prompt:
    current_conv["messages"].append(("user", prompt))
    st.session_state.stats["messages"] += 1
    
    with st.spinner(t["thinking"]):
        try:
            client = Groq(api_key=GROQ_API_KEY)
            messages = [{"role": "system", "content": PERSONALITIES[personality]}]
            for r, c in current_conv["messages"]:
                messages.append({"role": r, "content": c})
            
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
    st.markdown(f"""
    <div class="animated" style="text-align:center;padding:50px;">
        <h1 style="font-size:60px;">🤖</h1>
        <h2>{t['welcome']}</h2>
    </div>
    """, unsafe_allow_html=True)
