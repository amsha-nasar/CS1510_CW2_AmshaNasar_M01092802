
import streamlit as st
from openai import OpenAI
from oop.services.ai_assiatnt import DomainAssistant


if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("You must log in to access this page.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


if "chatbot" not in st.session_state:
    st.session_state.chatbot = DomainAssistant(
        api_key=st.secrets["OPENAI_API_KEY"],
        domain="cyber"  # default domain
    )

chatbot: DomainAssistant = st.session_state.chatbot
st.set_page_config(page_title="🛡 AI Assistant", page_icon="🛡️", layout="wide")
st.title("🛡 Multi-Domain AI Assistant")

st.subheader("Choose domain:")

if st.button("Cybersecurity"):
    chatbot.set_domain("cyber")
    st.success("Switched to Cybersecurity Assistant")

if st.button("Data Science"):
    chatbot.set_domain("data_science")
    st.success("Switched to Data Science Assistant")

if st.button("IT"):
    chatbot.set_domain("it")
    st.success("Switched to IT Assistant")

st.subheader("Conversation:")

for msg in chatbot.get_history():
    # Skip system messages
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Get user prompt 
prompt = st.chat_input("Ask the chatbot...")

if prompt: # Display user message 
   with st.chat_message("user"): 
    st.markdown(prompt)
    
chatbot.add_user_message(prompt)
response=chatbot.generate_response()

with st.chat_message("assistant"):
    st.markdown(response)