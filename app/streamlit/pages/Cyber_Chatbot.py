
import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page title
st.title("🛡 Cybersecurity AI Assistant")

# Initialize session state with system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """
You are a cybersecurity expert assistant.
- Analyze incidents and threats
- Provide technical guidance
- Explain attack vectors and mitigations
- Use standard terminology (MITRE ATT&CK, CVE)
- Prioritize actionable recommendations

Tone: Professional, technical
Format: Clear, structured responses
"""
        }
    ]

# Display chat history (skip system message)
for message in st.session_state.messages:
    if message["role"] != "system":  # Don't show system prompt
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Get user prompt
prompt = st.chat_input("Ask about cybersecurity...")

if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Call OpenAI API
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=st.session_state.messages
    )

    # Extract assistant response
    response = completion.choices[0].message.content

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
