import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import uuid
import json
from datetime import datetime

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
        "text": "#ececec", "accent": "#10a37f", "font": "Sora"
    },
    "Bleu Nuit": {
        "bg": "#0a0e1f", "sidebar": "#0d1425", "user_msg": "#1a2744",
        "text": "#e0e6ed", "accent": "#3b82f6", "font": "Sora"
    },
    "Violet Dream": {
        "bg": "#1a1025", "sidebar": "#251535", "user_msg": "#352045",
        "text": "#e0d0f0", "accent": "#a855f7", "font": "Sora"
    },
    "Vert Nature": {
        "bg": "#0a1a0f", "sidebar": "#0f2515", "user_msg": "#153525",
        "text": "#d0f0d8", "accent": "#22c55e", "font": "Sora"
    },
    "Coucher de Soleil": {
        "bg": "#1a0f0a", "sidebar": "#251510", "user_msg": "#352015",
        "text": "#f0e0d0", "accent": "#f97316", "font": "Sora"
    },
    "Rose Bonbon": {
        "bg": "#1a0f15", "sidebar": "#25101a", "user_msg": "#351525",
        "text": "#f0d0e0", "accent": "#ec4899", "font": "Sora"
    },
    "Clair": {
        "bg": "#ffffff", "sidebar": "#f5f5f5", "user_msg": "#e5e5e5",
        "text": "#1a1a1a", "accent": "#10a37f", "font": "Sora"
    },
}

# Thème actuel
if "theme" not in st.session_state:
    st.session_state.theme = "ChatGPT (Sombre)"

theme = THEMES[st.session_state.theme]

# Appliquer le thème
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600&display=swap');
    
    * {{ font-family: '{theme['font']}', sans-serif; }}
    
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
    
    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .animated {{
        animation: fadeIn 0.3s ease-in-out;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
    
    .pulse:hover {{
        animation: pulse 1s infinite;
    }}
    
    /* Badge style */
    .badge {{
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin: 3px;
        background-color: {theme['accent']};
    }}
    
    /* Stats cards */
    .stat-card {{
        background-color: {theme['user_msg']};
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 5px 0;
    }}
    
    /* Tool buttons */
    .tool-btn {{
        background-color: {theme['user_msg']};
        border: none;
        border-radius: 8px;
        padding: 10px 15px;
        cursor: pointer;
        color: {theme['text']};
        transition: all 0.2s;
    }}
    
    .tool-btn:hover {{
        background-color: {theme['accent']};
        transform: scale(1.05);
    }}
</style>
""", unsafe_allow_html=True)

# ===== TRADUCTIONS =====
TRANSLATIONS = {
    "Français": {"welcome": "Comment puis-je vous aider ?", "thinking": "Réflexion..."},
    "English": {"welcome": "How can I help you?", "thinking": "Thinking..."},
    "Español": {"welcome": "¿Cómo puedo ayudarte?", "thinking": "Pensando..."},
}

# ===== FONCTIONS =====
PERSONALITIES = {
    "🤖 Assistant": """Tu es Ley.AI, un assistant intelligent et utile.""",
    "😊 Amical": """Tu es Ley.AI, un ami chaleureux et attentionné.""",
    "🎓 Tuteur": """Tu es Ley.AI, un professeur patient.""",
    "😄 Drôle": """Tu es Ley.AI, un ami spirituel.""",
    "💼 Professionnel": """Tu es Ley.AI, un expert professionnel.""",
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
    st.session_state.stats = {"messages": 0, "chats": 1, "words": 0}
if "calculator_show" not in st.session_state:
    st.session_state.calculator_show = False
if "translator_show" not in st.session_state:
    st.session_state.translator_show = False
if "weather_show" not in st.session_state:
    st.session_state.weather_show = False
if "language" not in st.session_state:
    st.session_state.language = "Français"

current_conv = st.session_state.conversations[st.session_state.current_conversation]

# ===== FONCTIONS OUTILS =====
def calculator():
    st.markdown("### 🔢 Calculatrice")
    col1, col2, col3, col4 = st.columns(4)
    
    if 'calc_display' not in st.session_state:
        st.session_state.calc_display = ""
    
    display = st.text_input("", st.session_state.calc_display, key="calc_input")
    
    cols = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "=", "+"]
    ]
    
    for row in cols:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button(row[0]):
                st.session_state.calc_display += row[0]
                st.rerun()
        with c2:
            if st.button(row[1]):
                st.session_state.calc_display += row[1]
                st.rerun()
        with c3:
            if st.button(row[2]):
                st.session_state.calc_display += row[2]
                st.rerun()
        with c4:
            if st.button(row[3]):
                st.session_state.calc_display += row[3]
                st.rerun()
    
    if st.button("C"):
        st.session_state.calc_display = ""
        st.rerun()
    
    if st.button("="):
        try:
            result = eval(st.session_state.calc_display)
            st.session_state.calc_display = str(result)
        except:
            st.session_state.calc_display = "Erreur"
        st.rerun()

def translator():
    st.markdown("### 🌐 Traducteur")
    
    col1, col2 = st.columns(2)
    with col1:
        text = st.text_area("Texte à traduire")
        lang_from = st.selectbox("De", ["Français", "English", "Español", "Allemand", "Italien", "Portugais"])
    with col2:
        lang_to = st.selectbox("Vers", ["English", "Français", "Español", "Allemand", "Italien", "Portugais"], index=1)
    
    if st.button("Traduire") and text:
        st.info(f"Traduction de {lang_from} vers {lang_to}...")
        # Ici on utilise Groq pour traduire
        try:
            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": f"Traduis ce texte du {lang_from} vers {lang_to}: {text}"},
                          {"role": "user", "content": text}]
            )
            st.success(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Erreur: {str(e)}")

def weather():
    st.markdown("### 🌤️ Météo")
    
    city = st.text_input("Entrez une ville")
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if st.button("Voir la météo") and city:
        if api_key:
            try:
                import requests
                r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
                data = r.json()
                
                if data["cod"] == 200:
                    st.success(f"""
                    **🌡️ Température:** {data['main']['temp']}°C
                    **💧 Humidité:** {data['main']['humidity']}%
                    **🌬️ Vent:** {data['wind']['speed']} m/s
                    **☁️ Temps:** {data['weather'][0]['description']}
                    """)
                else:
                    st.error("Ville non trouvée")
            except:
                st.error("Erreur de connexion")
        else:
            st.warning("API météo non configurée. Demandez au développeur!")

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
    
    if st.button("➕ Nouveau Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.conversations[new_id] = {"messages": [], "personality": "🤖 Assistant"}
        st.session_state.current_conversation = new_id
        st.session_state.stats["chats"] += 1
        st.rerun()
    
    st.markdown("---")
    
    # Outils
    st.markdown("### 🛠️ Outils")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔢"):
            st.session_state.calculator_show = not st.session_state.calculator_show
    with col2:
        if st.button("🌐"):
            st.session_state.translator_show = not st.session_state.translator_show
    
    if st.button("🌤️"):
        st.session_state.weather_show = not st.session_state.weather_show
    
    st.markdown("---")
    
    # Paramètres
    st.markdown("### ⚙️")
    
    # Thème
    theme_name = st.selectbox("🎨 Thème", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.theme))
    if theme_name != st.session_state.theme:
        st.session_state.theme = theme_name
        st.rerun()
    
    # Personnalité
    personality = st.selectbox("🎭 Personnalité", list(PERSONALITIES.keys()), 
                               index=list(PERSONALITIES.keys()).index(current_conv["personality"]))
    if personality != current_conv["personality"]:
        current_conv["personality"] = personality
    
    # Créativité
    temperature = st.slider("🌡️ Créativité", 0.0, 2.0, 0.7, 0.1)
    
    # Langue
    lang = st.selectbox("🌐 Langue", ["Français", "English", "Español"], 
                       index=["Français", "English", "Español"].index(st.session_state.language))
    if lang != st.session_state.language:
        st.session_state.language = lang
        st.rerun()
    
    # Effacer
    if st.button("🗑️ Effacer"):
        current_conv["messages"] = []
        st.rerun()

# ===== OUTILS VISIBLES =====
if st.session_state.calculator_show:
    calculator()

if st.session_state.translator_show:
    translator()

if st.session_state.weather_show:
    weather()

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
    st.session_state.stats["words"] += len(prompt.split())
    
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
