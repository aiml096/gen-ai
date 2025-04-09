import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from googletrans import Translator


API_KEY = "AIzaSyBfibfGmL8oDwnLQGd62iB6LXfTfNQQG38"
genai.configure(api_key=API_KEY)


translator = Translator()


st.set_page_config(page_title="Desha Bhasalu - Telugu AI", page_icon="🌍", layout="wide")


st.markdown(
    """
    <style>
        [data-testid="stChatInputContainer"] {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: white;
            padding: 10px;
            box-shadow: 0px -2px 10px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
        }
        input[type="text"] {
            flex: 1;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 20px;
            margin-right: 10px;
        }
        button {
            padding: 10px 20px;
            border: none;
            background-color: #007AFF;
            color: white;
            font-size: 16px;
            border-radius: 20px;
            cursor: pointer;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🗣️ నమస్కారం! తెలుగు భాషలో చర్చించండి")


if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to get Gemini AI response
def get_gemini_response(question, image=None):
    model_name = "gemini-1.5-flash" if image else "gemini-2.0-flash"
    model = genai.GenerativeModel(model_name)
    response = model.generate_content([question, image] if image else question)
    return response.text

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Bar Like ChatGPT
with st.container():
    col1, col2 = st.columns([5, 1])
    with col1:
        input_text = st.text_input("", placeholder="📤 తెలుగులో మీ సందేశాన్ని టైప్ చేయండి...", key="input")
    with col2:
        uploaded_file = st.camera_input("📷", label_visibility="collapsed")

# Handle Image Upload
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📷 అప్‌లోడ్ చేయబడిన చిత్రం", use_column_width=True)

# Process User Input
if (input_text and input_text.strip()) or image:
    translated_input = translator.translate(input_text, src="te", dest="en").text if input_text else "Describe this image."
    
    # Display user message
    st.session_state.messages.append({"role": "user", "content": input_text if input_text else "📷 [Image Uploaded]"})
    st.chat_message("user").markdown(input_text if input_text else "📷 [Image Uploaded]")
    
    # Get AI response
    ai_response_en = get_gemini_response(translated_input, image)
    
    # Translate AI response back to Telugu
    ai_response_te = translator.translate(ai_response_en, src="en", dest="te").text
    
    # Display AI response
    st.session_state.messages.append({"role": "assistant", "content": ai_response_te})
    st.chat_message("assistant").markdown(ai_response_te)
