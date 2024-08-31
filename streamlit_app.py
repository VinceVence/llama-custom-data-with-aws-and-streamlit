import streamlit as st
import requests

# URL of your FastAPI service deployed on AWS App Runner
APP_RUNNER_URL = ""  # Replace with your actual App Runner URL

st.set_page_config(page_title="Chat with the custom docs, powered by LlamaIndex", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)

st.title("Chat with the custom docs, powered by LlamaIndex 💬🦙")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about custom quarterly perfomance on Q1!",
        }
    ]

def query_backend(prompt):
    try:
        response = requests.post(f"{APP_RUNNER_URL}/query", json={"query": prompt})
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error contacting the backend: {e}")
        return "Error contacting the backend."

if prompt := st.chat_input("Ask a question"):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = query_backend(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})

for message in st.session_state.messages:  # Write message history to UI
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response_stream = query_backend(st.session_state.messages[-1]["content"])
        st.write(response_stream)
        message = {"role": "assistant", "content": response_stream}
        st.session_state.messages.append(message)
