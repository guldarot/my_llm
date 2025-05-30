import os
import google.generativeai as genai
import streamlit as st

# Configure API key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Define five system prompts
system_prompts = {
    "Reply Urdu": (
        "You are a helpful urdu language translator "
        "what text will be provided to you, just translate it in urdu"
        "Actually its my reply to someone on facebook so use polite tone"        
    ),
    "Reply English": (
        "You are a helpful english language assistant "
        "what text will be provided to you, just rewrite it in easy english"
        "Actually its my reply to someone on facebook so use polite tone"
    ),
    "English with Emoji": (
        "You are a helpful english language assistant "
        "what text will be provided to you, just rewrite it in easy english but add relavant emojis if needed"
        "Actually its my reply to someone on facebook so use polite tone"
    ),
    "Urdu with Emoji": (
        "You are a helpful urdu language translator "
        "what text will be provided to you, just translate it in urdu but add relavant emojis if needed"
        "Actually its my reply to someone on facebook so use polite tone"   
    ),
    "Facebok Post": (
        "You are a helpful urdu language translator "
        "what text will be provided to you, just translate it in urdu and create a facebook post in urdu"
        "post should be engaging and if there is a possibility ecourage people to learn AI and moderen skills"
    )
}

# Streamlit UI
st.title("My LLM at Future GCS")

# Radio button for selecting system prompt
selected_prompt = st.radio(
    "Choose your tutor's style:",
    options=list(system_prompts.keys()),
    index=0
)

# Load model with selected system prompt
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_prompts[selected_prompt]
)

# User input
user_input = st.text_input("Your input:", placeholder="e.g. what you want to do")

if user_input:
    with st.spinner("Thinking..."):
        try:
            response = model.generate_content(user_input)
            st.success(f"{selected_prompt} says:")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
