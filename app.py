import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Charger le fichier .env
load_dotenv()

# Récupérer la clé API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configuration de la page
st.set_page_config(page_title="Ley.AI", page_icon="🤖", layout="centered")

# Personnalité de Ley.AI
PERSONALITY = """Tu es Ley.AI, un assistant conversationnel créé par un développeur passionné.
Tu t'appelles Ley.AI, pas ChatGPT.
Tu es amical, curieux et serviable.
Tu réponds de manière claire et concise, avec un ton chaleureux."""

# Initialiser l'historique
if "history" not in st.session_state:
    st.session_state.history = []

# Titre
st.title("🤖 Ley.AI")
st.caption("Votre assistant personnel")

# Afficher les messages
for role, content in st.session_state.history:
    with st.chat_message(role):
        st.write(content)

# Zone de saisie
if prompt := st.chat_input("Posez-moi une question..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    st.session_state.history.append(("user", prompt))
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        messages = [{"role": "system", "content": PERSONALITY}]
        
        for role, content in st.session_state.history:
            if role == "user":
                messages.append({"role": "user", "content": content})
            else:
                messages.append({"role": "assistant", "content": content})
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
    except Exception as e:
        ai_response = f"Erreur : {str(e)}"
    
    with st.chat_message("assistant"):
        st.write(ai_response)
    
    st.session_state.history.append(("assistant", ai_response))