import streamlit as st
import os
from dotenv import load_dotenv
from retriever import get_rag_response
from streamlit_chat import message
import time

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Unstress Therapy Chat",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .title-text {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2E4057;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle-text {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
        padding: 10px 20px;
    }
    .stButton > button {
        border-radius: 20px;
        padding: 10px 20px;
        background-color: #2E4057;
        color: white;
    }
    .stButton > button:hover {
        background-color: #1E2F3F;
    }
    </style>
    """, unsafe_allow_html=True)

# Display title with custom styling
st.markdown('<h1 class="title-text">Unstress Therapy Chat</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Your AI-powered mental health companion</p>', unsafe_allow_html=True)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to display chat messages
def display_chat():
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            message(msg["content"], is_user=True, key=f"user_{i}")
        else:
            message(msg["content"], is_user=False, key=f"assistant_{i}")

# Main chat interface
user_input = st.text_input("How are you feeling today?", key="user_input")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    message(user_input, is_user=True)
    
    # Get AI response
    with st.spinner("Thinking..."):
        response = get_rag_response(user_input)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display assistant response
    message(response, is_user=False)
    
    # Clear the input box
    st.session_state.user_input = ""

# Display chat history
display_chat()

# Add footer
st.markdown("""
    <div style='text-align: center; margin-top: 2rem; color: #666;'>
        <p>© 2024 Unstress. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)
