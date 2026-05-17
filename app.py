import streamlit as st
from groq import Groq

# ======================
# PAGE SETTINGS
# ======================

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 AI Chatbot")

# ======================
# API KEY INPUT
# ======================

api_key = st.text_input(
    "Enter Groq API Key",
    type="password"
)

# ======================
# CHAT HISTORY
# ======================

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ======================
# USER INPUT
# ======================

prompt = st.chat_input("Type your message...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        if not api_key:
            response = "Please enter API key."

        else:
            try:
                client = Groq(api_key=api_key)

                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=1024
                )

                response = completion.choices[0].message.content

            except Exception as e:
                response = f"Error: {e}"

        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })