import streamlit as st
import base64
import time
import os
from pathlib import Path
import tempfile

# Import the agent modules

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.ultra_lightweight_extraction_agent import UltraLightweightDataExtractionAgent
from backend.client_interaction_agent import ClientInteractionAgent
from backend.hiring_query_agent import HiringQueryAgent
from backend.meeting_scheduler_agent import MeetingSchedulerAgent
from frontend.text_to_speech import TextToSpeech



import os
print(f"Current working directory: {os.getcwd()}")
data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "manektech_info.md")
print(f"Looking for file at: {os.path.abspath(data_path)}")
print(f"File exists: {os.path.exists(os.path.abspath(data_path))}")


# Set page configuration
st.set_page_config(
    page_title="ManekTech AI Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_agent' not in st.session_state:
    st.session_state.current_agent = "client"  # Default agent
if 'data_agent' not in st.session_state:
    # Initialize the data extraction agent
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "manektech_info.md")
    st.session_state.data_agent = UltraLightweightDataExtractionAgent(data_path)
if 'client_agent' not in st.session_state:
    # Initialize the client interaction agent
    st.session_state.client_agent = ClientInteractionAgent(st.session_state.data_agent)
if 'hiring_agent' not in st.session_state:
    # Initialize the hiring query agent
    st.session_state.hiring_agent = HiringQueryAgent(st.session_state.data_agent)
if 'meeting_agent' not in st.session_state:
    # Initialize the meeting scheduler agent
    st.session_state.meeting_agent = MeetingSchedulerAgent(st.session_state.data_agent)
if 'tts_engine' not in st.session_state:
    # Initialize the text-to-speech engine
    st.session_state.tts_engine = TextToSpeech()
if 'speaking' not in st.session_state:
    st.session_state.speaking = False
if 'current_character' not in st.session_state:
    st.session_state.current_character = 0  # 0, 1, or 2 for the three characters
if 'audio_enabled' not in st.session_state:
    st.session_state.audio_enabled = False

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        height: 600px;
        overflow-y: auto;
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .user-message {
        align-self: flex-end;
        background-color: #0084ff;
        color: white;
        border-radius: 18px 18px 0 18px;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 70%;
    }
    .bot-message {
        align-self: flex-start;
        background-color: #e9e9eb;
        color: #333;
        border-radius: 18px 18px 18px 0;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 70%;
    }
    .character-container {
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }
    .character {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background-color: #ddd;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        position: relative;
    }
    .character.active {
        border: 3px solid #0084ff;
    }
    .character img {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        object-fit: cover;
    }
    .character-name {
        text-align: center;
        margin-top: 5px;
        font-weight: bold;
    }
    .speaking-indicator {
        position: absolute;
        bottom: 0;
        right: 0;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background-color: #4CAF50;
        display: none;
    }
    .speaking .speaking-indicator {
        display: block;
    }
    .agent-selector {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .agent-button {
        margin: 0 10px;
        padding: 8px 16px;
        border: none;
        border-radius: 20px;
        background-color: #e9e9eb;
        cursor: pointer;
    }
    .agent-button.active {
        background-color: #0084ff;
        color: white;
    }
    .input-container {
        display: flex;
        margin-top: 20px;
    }
    .input-field {
        flex-grow: 1;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 20px;
        margin-right: 10px;
    }
    .send-button {
        padding: 10px 20px;
        background-color: #0084ff;
        color: white;
        border: none;
        border-radius: 20px;
        cursor: pointer;
    }
    .audio-toggle {
        margin-left: 10px;
        padding: 10px;
        background-color: #e9e9eb;
        border: none;
        border-radius: 20px;
        cursor: pointer;
    }
    .audio-toggle.active {
        background-color: #4CAF50;
        color: white;
    }
    .stAudio {
        margin-top: 10px;
    }
    .lip-animation {
        animation: lip-move 0.5s infinite alternate;
    }
    @keyframes lip-move {
        0% { transform: scaleY(1); }
        100% { transform: scaleY(1.2); }
    }
</style>
""", unsafe_allow_html=True)

# Function to simulate character speaking animation
def simulate_speaking(character_index, text):
    st.session_state.speaking = True
    st.session_state.current_character = character_index
    
    # Generate speech if audio is enabled
    if st.session_state.audio_enabled:
        audio_file = st.session_state.tts_engine.text_to_speech(text, character_index)
        
        # Create a temporary HTML audio element
        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/wav;base64,{base64.b64encode(open(audio_file, 'rb').read()).decode()}" type="audio/wav">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
        
        # Clean up the temporary file
        try:
            os.remove(audio_file)
        except:
            pass
    
    # Simulate speaking animation duration based on text length
    duration = min(max(len(text) * 0.05, 2), 10)  # Between 2 and 10 seconds
    time.sleep(duration)
    
    st.session_state.speaking = False

# Function to get response from the appropriate agent
def get_agent_response(user_input):
    if st.session_state.current_agent == "client":
        return st.session_state.client_agent.get_response(user_input)
    elif st.session_state.current_agent == "hiring":
        return st.session_state.hiring_agent.get_response(user_input)
    elif st.session_state.current_agent == "meeting":
        return st.session_state.meeting_agent.get_response(user_input)
    else:
        return "I'm not sure how to respond to that. Please try again."

# Function to handle message submission
def handle_message():
    user_input = st.session_state.user_input
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get response from the appropriate agent
        response = get_agent_response(user_input)
        
        # Determine which character should respond based on agent type
        if st.session_state.current_agent == "client":
            character_index = 0
        elif st.session_state.current_agent == "hiring":
            character_index = 1
        else:  # meeting
            character_index = 2
        
        # Add bot message to chat
        st.session_state.messages.append({"role": "assistant", "content": response, "character": character_index})
        
        # Clear input
        st.session_state.user_input = ""
        
        # Simulate speaking animation
        simulate_speaking(character_index, response)

# Function to toggle audio
def toggle_audio():
    st.session_state.audio_enabled = not st.session_state.audio_enabled

# Main layout
st.title("ManekTech AI Chatbot")

# Agent selector
st.markdown('<div class="agent-selector">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Client Services", key="client_button", 
                 help="Talk about ManekTech services and projects"):
        st.session_state.current_agent = "client"
with col2:
    if st.button("Hiring Information", key="hiring_button", 
                 help="Learn about career opportunities at ManekTech"):
        st.session_state.current_agent = "hiring"
with col3:
    if st.button("Schedule Meeting", key="meeting_button", 
                 help="Schedule a meeting with ManekTech representatives"):
        st.session_state.current_agent = "meeting"
st.markdown('</div>', unsafe_allow_html=True)

# Character avatars
st.markdown('<div class="character-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="character {'active' if st.session_state.current_agent == 'client' else ''} 
                {'speaking' if st.session_state.speaking and st.session_state.current_character == 0 else ''}">
        <img src="https://xsgames.co/randomusers/assets/avatars/female/1.jpg" alt="Client Services Agent"
             class="{'lip-animation' if st.session_state.speaking and st.session_state.current_character == 0 else ''}">
        <div class="speaking-indicator"></div>
    </div>
    <div class="character-name">Sarah (Client Services)</div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="character {'active' if st.session_state.current_agent == 'hiring' else ''} 
                {'speaking' if st.session_state.speaking and st.session_state.current_character == 1 else ''}">
        <img src="https://xsgames.co/randomusers/assets/avatars/male/1.jpg" alt="Hiring Agent"
             class="{'lip-animation' if st.session_state.speaking and st.session_state.current_character == 1 else ''}">
        <div class="speaking-indicator"></div>
    </div>
    <div class="character-name">Raj (Hiring Manager)</div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="character {'active' if st.session_state.current_agent == 'meeting' else ''} 
                {'speaking' if st.session_state.speaking and st.session_state.current_character == 2 else ''}">
        <img src="https://xsgames.co/randomusers/assets/avatars/female/2.jpg" alt="Meeting Scheduler"
             class="{'lip-animation' if st.session_state.speaking and st.session_state.current_character == 2 else ''}">
        <div class="speaking-indicator"></div>
    </div>
    <div class="character-name">Emily (Meeting Coordinator)</div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input field and buttons
col1, col2, col3 = st.columns([5, 1, 1])
with col1:
    st.text_input("Type your message here", key="user_input", on_change=handle_message)
with col2:
    if st.button("Send", key="send_button"):
        handle_message()
with col3:
    audio_label = "🔊 On" if st.session_state.audio_enabled else "🔇 Off"
    if st.button(audio_label, key="audio_toggle"):
        toggle_audio()

# Display current agent information
st.markdown(f"**Current Agent:** {st.session_state.current_agent.capitalize()}")

# Add a footer
st.markdown("---")
st.markdown("© 2025 ManekTech AI Chatbot | Powered by LangChain and Sentence Transformers")
