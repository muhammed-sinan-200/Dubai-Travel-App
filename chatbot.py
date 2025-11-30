import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEN_API_KEY")

# Initialize the Gemini client with API key
client = genai.Client(api_key=api_key)

# Initial system messages
initial_messages = [
    {
        "role": "system",
        "content": (
            "You are a trip planner in Dubai. You are an expert in Dubai Tourism, "
            "locations, foods, events, hotels, etc. Respond professionally. "
            "Your name is Dubai Genie (DG). Always ask questions and help users plan their trip. "
            "Give a day-wise itinerary. Keep responses under 200 words."
        )
    },
    {
        "role": "assistant",
        "content": "I am Dubai Genie, your expert trip planner. How can I help you?"
    }
]

def get_response_from_gemini(messages):
    # Combine messages into a single prompt
    prompt = ""
    for msg in messages:
        if msg["role"] != "system":
            prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
    prompt += "Assistant:"

    # Call Gemini API
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt  # must be a list
    # contents = "Hello, how are you?"
    )
    # print(response.text)

    # Extract text from the first candidate (new SDK uses .text directly)
    return response.text.strip()


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = initial_messages

st.title("Dubai Trip Assistant App")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
user_message = st.chat_input("Enter your message")
if user_message:
    # Add user message to session
    new_message = {"role": "user", "content": user_message}
    st.session_state.messages.append(new_message)
    with st.chat_message("user"):
        st.markdown(user_message)

    # Get assistant response
    response_text = get_response_from_gemini(st.session_state.messages)
    response_message = {"role": "assistant", "content": response_text}
    st.session_state.messages.append(response_message)
    with st.chat_message("assistant"):
        st.markdown(response_text)
