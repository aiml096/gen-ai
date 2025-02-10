
import streamlit as st
import os
import google.generativeai as genai
from googletrans import Translator  # Import translation module

# Load environment variables


# Configure Gemini API
genai.configure(api_key="AIzaSyBbc_9liLY5VVnkIbjT7Vg4U71PyD6vG2Q")

# Initialize translator
translator = Translator()

# Initialize Streamlit app
st.set_page_config(page_title="Telugu AI Chatbot", page_icon="🌍")

st.title("🗣️ Gemini AI Telugu Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to get Gemini AI response
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
input_text = st.chat_input("తెలుగులో మీ సందేశాన్ని టైప్ చేయండి... (Type your message in Telugu)")

if input_text:
    # Translate Telugu to English
    translated_input = translator.translate(input_text, src="te", dest="en").text

    # Display user message on the right
    st.chat_message("user").markdown(input_text)
    st.session_state.messages.append({"role": "user", "content": input_text})

    # Get AI response in English
    ai_response_en = get_gemini_response(translated_input)

    # Translate AI response back to Telugu
    ai_response_te = translator.translate(ai_response_en, src="en", dest="te").text

    # Display AI response on the left
    with st.chat_message("assistant"):
        st.markdown(ai_response_te)

    # Store AI response in session history
    st.session_state.messages.append({"role": "assistant", "content": ai_response_te})
