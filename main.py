import os
import json
import base64

import streamlit as st
from streamlit import caching
from streamlit import components
from streamlit.button import Button
from streamlit.folium import folium_static
from streamlit.libraries import load_state
from streamlit.components import cache
from streamlit.components import img
from streamlit.state import get_state
from streamlit.scribble import Scribble
from streamlit.markdown import markdown

# Import necessary libraries
import groq
from groq import Groq
from streamlit.components.v1 import iframe

# Load streamlit secrets
api_key = st.secrets["API_KEY"]

# Initialize the client
client = Groq(api_key=api_key)

# Available models
available_models = ["llama-3.1-8b-instant", "curie", "davinci"]

# Available themes
available_themes = ["light", "dark"]

# Chat history
chat_history = []

# Initialize cache
loaded_cache = st.cache

# Define the session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = chat_history

# Set up the app layout
st.title("LLAMA 3.1. Chat")

# Create sidebar widgets
with st.sidebar:
    # Add select box for models
    st.session_state.model = st.selectbox(label="Select a model", options=available_models, key="model_selector")

    # Add select box for themes
    st.session_state.theme = st.selectbox(label="Select a theme", options=["light", "dark"], index=1, key="theme_selector")

# Create main app section
st.markdown("## Chat")
with st.expander("Chat History"):
    st.write(st.session_state.chat_history)

# Get the user's message
with st.form(key="chat_form"):
    user_message = st.text_area("Ask LLAMA...", height=100)
    submit_button = st.form_submit_button("Send Message")

if submit_button:
    # Create new message object
    new_message = {"role": "user", "content": user_message}

    # Add message to chat history
    st.session_state.chat_history.append(new_message)

    # Create messages object for API call
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        *st.session_state.chat_history
    ]

    # Create API call object
    api_call = client.chat.completions.create(
        model=st.session_state.model,
        messages=messages
    )

    # Get the API call response
    response = api_call.data

    # Add response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response.choices[0].message.content})

    # Render the chat history
    st.session_state.chat_history