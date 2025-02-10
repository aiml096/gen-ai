from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key="AIzaSyBbc_9liLY5VVnkIbjT7Vg4U71PyD6vG2Q")


# Initialize Streamlit app
st.set_page_config(page_title="Gemini Chatbot", page_icon="💬")

st.title("🤖 Gemini AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to get Gemini AI response
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
input_text = st.chat_input("Type your message here...")

if input_text:
    # Display user message on the right
    st.chat_message("user").markdown(input_text)

    # Store user message in session history
    st.session_state.messages.append({"role": "user", "content": input_text})

    # Get AI response
    response = get_gemini_response(input_text)

    # Display AI response on the left
    with st.chat_message("assistant"):
        st.markdown(response)

    # Store AI response in session history
    st.session_state.messages.append({"role": "assistant", "content": response})
