import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from googletrans import Translator

# Configure Gemini API
API_KEY = os.getenv("GOOGLE_API_KEY")  # Ensure your .env file has the correct API key
genai.configure(api_key=API_KEY)

# Initialize translator
translator = Translator()

# Set up Streamlit UI
st.set_page_config(page_title="Desha Bhasalu - Telugu AI", page_icon="🌍")

# Custom Styling
st.markdown(
    """
    <style>
        .stTextInput > div > div > input {
            padding-left: 35px;
        }
        .stButton button {
            width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🗣️ నమస్కారం! తెలుగు భాషలో చర్చించండి")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to get Gemini AI response
def get_gemini_response(question, image=None):
    model_name = "gemini-1.0-pro-vision" if image else "gemini-1.0-pro"
    model = genai.GenerativeModel(model_name)
    response = model.generate_content([question, image] if image else question)
    return response.text

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input and Image Upload in a Single Row
col1, col2 = st.columns([5, 1])
with col1:
    input_text = st.text_input("📤 తెలుగులో మీ సందేశాన్ని టైప్ చేయండి...", key="input")

with col2:
    uploaded_file = st.file_uploader("📷", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

# Handle Image Upload
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📷 అప్‌లోడ్ చేయబడిన చిత్రం", use_column_width=True)

# Process User Input
if (input_text and input_text.strip()) or image:
    translated_input = translator.translate(input_text, src="te", dest="en").text if input_text else "Describe this image."

    # Display user message
    st.chat_message("user").markdown(input_text if input_text else "📷 [Image Uploaded]")
    st.session_state.messages.append({"role": "user", "content": input_text if input_text else "📷 [Image Uploaded]"})

    # Get AI response
    ai_response_en = get_gemini_response(translated_input, image)

    # Translate AI response back to Telugu
    ai_response_te = translator.translate(ai_response_en, src="en", dest="te").text

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response_te)
    
    st.session_state.messages.append({"role": "assistant", "content": ai_response_te})
