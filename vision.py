from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = "AIzaSyBfibfGmL8oDwnLQGd62iB6LXfTfNQQG38"
if not api_key:
    st.error("API key not found. Make sure to set GOOGLE_API_KEY in .env")
    st.stop()
genai.configure(api_key=api_key)

# Initialize model
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to get Gemini response
def get_gemini_response(input_text, image):
    response = model.generate_content([input_text, image] if input_text else [image])
    return response.text

# Streamlit UI setup
st.set_page_config(page_title="Gemini Image Describer")
st.header("Gemini Application")

# User input
input_text = st.text_input("Input Prompt:", key="input")

# Image upload
upload_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None
if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Submit button
if st.button("Tell me about the image"):
    if not image:
        st.warning("Please upload an image first.")
    else:
        response = get_gemini_response(input_text, image)
        st.subheader("The response is:")
        st.write(response)
