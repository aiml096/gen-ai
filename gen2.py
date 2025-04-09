import streamlit as st
from PIL import Image
import google.generativeai as genai
from googletrans import Translator
import io

# --- API Key and Setup ---
API_KEY = "AIzaSyBfibfGmL8oDwnLQGd62iB6LXfTfNQQG38"  # Replace with your actual API key
genai.configure(api_key=API_KEY)
translator = Translator()

# --- Page Configuration ---
st.set_page_config(page_title="తెలుగు AI సంభాషణ", page_icon="🇮🇳", layout="wide")

# --- CSS Styling ---
st.markdown("""
    <style>
    .app-title {
        font-size: 2.5rem;
        color: #28a745;
        text-align: center;
        margin-top: 10px;
    }
    .subheader {
        font-size: 1.1rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 20px;
    }
    .user-message {
        text-align: right;
        background-color: #e6f7ff;
        padding: 10px 15px;
        border-radius: 12px;
        margin: 5px 0;
        max-width: 70%;
        margin-left: auto;
        color: #000;
    }
    .ai-message {
        text-align: left;
        background-color: #f0f2f5;
        padding: 10px 15px;
        border-radius: 12px;
        margin: 5px 0;
        max-width: 70%;
        margin-right: auto;
        color: #000;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Title and Subheader ---
st.markdown("<div class='app-title'>🇮🇳 తెలుగు AI సంభాషణ</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>మీ ఆలోచనలను తెలుగులో పంచుకోండి, AI ప్రతిస్పందిస్తుంది!</div>", unsafe_allow_html=True)

# --- Session State Initialization ---
for key in ["messages", "chat_history", "input_text", "uploaded_image", "show_camera"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key in ["messages", "chat_history"] else (False if key == "show_camera" else None)

# --- Gemini API Function ---
def get_gemini_response(question, image=None):
    model_name = "gemini-1.5-flash" if image else "gemini-2.0-flash"
    model = genai.GenerativeModel(model_name)

    prompt_parts = [question]

    if image:
        try:
            # ✅ Convert image bytes to PIL.Image
            pil_image = Image.open(io.BytesIO(image.getvalue()))
            prompt_parts = [question, pil_image]
        except Exception as e:
            return f"చిత్రాన్ని ప్రాసెస్ చేయడంలో లోపం: {e}"

    try:
        response = model.generate_content(prompt_parts)
        return getattr(response, "text", str(response)).replace("***", "").strip()
    except Exception as e:
        return f"క్షమించండి, లోపం జరిగింది: {e}"

# --- Chat Processing ---
def send_message():
    user_input = st.session_state.input_text
    image = st.session_state.uploaded_image

    if user_input or image:
        user_message = user_input if user_input else "📷 చిత్రం"
        translated_input = (
            translator.translate(user_input, src="te", dest="en").text
            if user_input
            else "Describe this image."
        )

        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_message})

        with st.spinner("AI స్పందిస్తోంది..."):
            ai_response_en = get_gemini_response(translated_input, image)
            ai_response_te = translator.translate(ai_response_en, src="en", dest="te").text

        # Add AI response
        st.session_state.messages.append({"role": "assistant", "content": ai_response_te})

        # Save history
        st.session_state.chat_history.append(st.session_state.messages.copy())

        # Reset inputs
        st.session_state.input_text = ""
        st.session_state.uploaded_image = None
        st.session_state.show_camera = False

# --- Display Chat Messages (Formatted) ---
st.divider()
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='ai-message'>{message['content']}</div>", unsafe_allow_html=True)
st.divider()

# --- Input Text ---
st.text_input("మీ సందేశం", placeholder="ఇక్కడ టైప్ చేయండి...", key="input_text")

# --- Camera Toggle ---
if st.button("📸 కెమెరాను తెరవండి"):
    st.session_state.show_camera = not st.session_state.show_camera

# --- Conditional Camera Input ---
if st.session_state.show_camera:
    st.session_state.uploaded_image = st.camera_input("చిత్రాన్ని ఎంచుకోండి", key="camera_input")

# --- Send Button ---
st.button("పంపు", on_click=send_message)

# --- Sidebar Chat History ---
with st.sidebar:
    st.markdown("## చరిత్ర")
    if st.session_state.chat_history:
        for idx, session in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"సంభాషణ {len(st.session_state.chat_history) - idx}"):
                for msg in session:
                    st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")
    else:
        st.info("ఇక్కడ చరిత్ర లేదు.")

