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

# Load model
model = genai.GenerativeModel(
    model_name = "gemini-1.5-flash",
    system_instruction=system_prompt
)

# Streamlit app configuration
st.set_page_config(page_title="My LLM Interface", layout="wide")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title and description
st.title("LLM Chat Interface")
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

        # Prepare messages for OpenAI API
        messages = [
            {"role": "system", "content": system_prompts[selected_prompt]},
            *st.session_state.messages
        ]

        try:
            # Call OpenAI API (using a placeholder model, replace with desired model)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Replace with your preferred model
                messages=messages,
                max_tokens=500
            )
            # Add assistant response to chat history
            assistant_response = response.choices[0].message.content
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
