import streamlit as st
from PIL import Image
import google.generativeai as genai
from googletrans import Translator

# ✅ Set page config as the first command
st.set_page_config(page_title="Desha Bhasalu - Telugu AI", page_icon="🌍", layout="wide")

# Configure API
API_KEY = "AIzaSyBX0e2zJR3GpjnuFfVL099qFKr3O3OnfhQ"
genai.configure(api_key=API_KEY)

translator = Translator()

st.title("🗣️ నమస్కారం! తెలుగు భాషలో చర్చించండి")

if "messages" not in st.session_state:
    st.session_state.messages = []


def get_gemini_response(question, image=None):
    model_name = "gemini-1.5-flash" if image else "gemini-2.0-flash"
    model = genai.GenerativeModel(model_name)
    response = model.generate_content([question, image] if image else question)
    return response.text

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# User Input
input_text = st.text_input("📤 తెలుగులో మీ సందేశాన్ని టైప్ చేయండి...", key="input")
uploaded_file = st.file_uploader("📷 చిత్రాన్ని అప్‌లోడ్ చేయండి", type=["jpg", "png", "jpeg"])

# Handle Image Upload
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📷 అప్‌లోడ్ చేసిన చిత్రం", use_column_width=True)

# Process User Input
if input_text.strip() or image:
    translated_input = translator.translate(input_text, src="te", dest="en").text if input_text else "Describe this image."
    
    # Display User Message
    st.session_state.messages.append({"role": "user", "content": input_text if input_text else "📷 [Image Uploaded]"})
    st.chat_message("user").markdown(input_text if input_text else "📷 [Image Uploaded]")
    
    # Get AI response
    ai_response_en = get_gemini_response(translated_input, image)
    
    # Translate AI response back to Telugu
    ai_response_te = translator.translate(ai_response_en, src="en", dest="te").text
    
    # Ensure response is relevant
    if "ICE" in ai_response_te or "నిధి" in ai_response_te:  # Detect hallucinated output
        ai_response_te = "⚠️ క్షమించండి, కానీ AI సరైన సమాధానం ఇవ్వలేదు. దయచేసి మరోసారి ప్రయత్నించండి."

    # Translation Option
    translate_to_english = st.checkbox("Would you like the response in English?")

    # Format Response
    markdown_response = f"**🤖 AI Response (Telugu):**\n\n{ai_response_te}"
    if translate_to_english:
        markdown_response += f"\n\n---\n\n**🌍 AI Response (English):**\n\n{ai_response_en}"

    # Display AI Response
    st.session_state.messages.append({"role": "assistant", "content": markdown_response})
    st.chat_message("assistant").markdown(markdown_response, unsafe_allow_html=True)

