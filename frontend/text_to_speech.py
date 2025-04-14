"""
Text-to-Speech module for ManekTech AI Chatbot

This module provides text-to-speech functionality for the chatbot responses.
"""

import os
import tempfile
import pyttsx3
from pathlib import Path

class TextToSpeech:
    def __init__(self):
        """Initialize the Text-to-Speech engine."""
        self.engine = pyttsx3.init()
        self.setup_voices()
        
    def setup_voices(self):
        """Set up different voices for different characters."""
        self.voices = self.engine.getProperty('voices')
        self.character_voices = {
            0: 0,  # Default female voice for Client Services (Sarah)
            1: 1,  # Male voice for Hiring Manager (Raj)
            2: 0   # Female voice for Meeting Coordinator (Emily)
        }
        
        # Set default properties
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        
    def get_available_voices(self):
        """Get a list of available voices."""
        return [(i, voice.name) for i, voice in enumerate(self.voices)]
    
    def set_character_voice(self, character_index):
        """Set the voice for a specific character."""
        if character_index in self.character_voices and self.character_voices[character_index] < len(self.voices):
            voice_index = self.character_voices[character_index]
            self.engine.setProperty('voice', self.voices[voice_index].id)
        else:
            # Default to first voice if specified voice is not available
            self.engine.setProperty('voice', self.voices[0].id)
    
    def text_to_speech(self, text, character_index=0):
        """
        Convert text to speech and return the path to the audio file.
        
        Args:
            text (str): The text to convert to speech.
            character_index (int): The index of the character speaking (0, 1, or 2).
            
        Returns:
            str: Path to the generated audio file.
        """
        # Set the appropriate voice for the character
        self.set_character_voice(character_index)
        
        # Create a temporary file for the audio
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.close()
        
        # Save speech to the temporary file
        self.engine.save_to_file(text, temp_file.name)
        self.engine.runAndWait()
        
        return temp_file.name
    
    def speak(self, text, character_index=0):
        """
        Speak the text directly without saving to a file.
        
        Args:
            text (str): The text to speak.
            character_index (int): The index of the character speaking (0, 1, or 2).
        """
        # Set the appropriate voice for the character
        self.set_character_voice(character_index)
        
        # Speak the text
        self.engine.say(text)
        self.engine.runAndWait()


# Example usage
if __name__ == "__main__":
    tts = TextToSpeech()
    
    # Print available voices
    print("Available voices:")
    for i, name in tts.get_available_voices():
        print(f"{i}: {name}")
    
    # Test with different characters
    test_text = "Hello, I'm Sarah from ManekTech client services. How can I help you today?"
    tts.speak(test_text, 0)
    
    test_text = "Hi, I'm Raj from ManekTech hiring team. We're always looking for talented professionals."
    tts.speak(test_text, 1)
    
    test_text = "Hello, I'm Emily, the meeting coordinator at ManekTech. I can help you schedule a meeting."
    tts.speak(test_text, 2)
    
    # Generate an audio file
    audio_path = tts.text_to_speech("Thank you for using ManekTech AI Chatbot!")
    print(f"Audio saved to: {audio_path}")
