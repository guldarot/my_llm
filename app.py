import os
import google.generativeai as genai
import streamlit as st

# Configure API key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Define system prompts
system_prompts = {
    "1": "You are a helpful assistant that provides concise and accurate answers.",
    "2": "You are a creative writer, crafting engaging and imaginative responses.",
    "3": "You are a technical expert, providing detailed and precise technical explanations.",
    "4": "You are a friendly tutor, explaining concepts in a simple and approachable way.",
    "5": "You are a humorous assistant, adding wit and humor to your responses.",
    "6": "You are a professional consultant, offering formal and structured advice.",
    "7": "You are a storyteller, weaving narrative-driven responses.",
    "8": "You are a critical thinker, providing in-depth analysis and reasoning.",
    "9": "You are a motivational coach, inspiring and encouraging in your responses.",
    "10": "You are a concise fact-checker, verifying information with brevity."
}

# Streamlit app configuration
st.set_page_config(page_title="Gemini Chat Interface", layout="wide")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title and description
st.title("Gemini Chat Interface")
st.markdown("Select a system prompt and interact with the AI assistant.")

# Sidebar for system prompt selection
with st.sidebar:
    st.header("System Prompt Selection")
    selected_prompt = st.radio(
        "Choose a system prompt:",
        options=list(system_prompts.keys()),
        format_func=lambda x: f"Prompt {x}: {system_prompts[x]}"
    )

# Chat interface
st.subheader("Chat with the AI")
user_input = st.text_input("Your message:", key="user_input")

# Button to send message
if st.button("Send"):
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Prepare the prompt with system instruction and conversation history
        conversation = f"System: {system_prompts[selected_prompt]}\n\n"
        for message in st.session_state.messages:
            role = "User" if message["role"] == "user" else "Assistant"
            conversation += f"{role}: {message['content']}\n\n"

        try:
            # Initialize Gemini model
            model = genai.GenerativeModel('gemini-1.5-pro')  # Replace with desired Gemini model
            response = model.generate_content(
                conversation,
                generation_config={
                    "max_output_tokens": 500,
                    "temperature": 0.7
                }
            )
            # Add assistant response to chat history
            assistant_response = response.text
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**You**: {message['content']}")
    else:
        st.markdown(f"**AI**: {message['content']}")

# Clear chat history button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()
