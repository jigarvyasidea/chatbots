"""
Main application for ManekTech AI-powered Chatbot

This script integrates all components of the ManekTech AI-powered chatbot
and provides a unified interface for running the application.
"""

import os
import sys
import streamlit as st
import subprocess
import webbrowser
from pathlib import Path

def main():
    """Main function to run the ManekTech AI-powered Chatbot."""
    print("ManekTech AI-powered Chatbot")
    print("============================")
    print("\nThis application integrates multiple AI agents:")
    print("1. Data Extraction Agent - Extracts company details from ManekTech data")
    print("2. Client Interaction Agent - Mimics human responses for client interactions")
    print("3. Hiring Query Agent - Handles hiring queries with positive responses")
    print("4. Meeting Scheduler Agent - Schedules meetings if requested")
    print("\nThe chatbot includes:")
    print("- Three animated characters with lip movement")
    print("- Interactive conversation experience")
    print("- Text-to-speech functionality")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the Streamlit app
    app_path = os.path.join(current_dir, "frontend", "app_with_tts.py")
    
    # Check if the app file exists
    if not os.path.exists(app_path):
        print(f"\nError: Could not find the application file at {app_path}")
        return
    
    print("\nStarting the chatbot application...")
    print("(Press Ctrl+C to stop the application)")
    
    # Run the Streamlit app
    try:
        # Command to run the Streamlit app
        cmd = ["streamlit", "run", app_path, "--server.port=8501"]
        
        # Start the process
        process = subprocess.Popen(cmd)
        
        # Open the browser
        webbrowser.open("http://localhost:8501")
        
        # Wait for the process to complete
        process.wait()
    except KeyboardInterrupt:
        print("\nStopping the chatbot application...")
    except Exception as e:
        print(f"\nError running the application: {e}")
    
    print("\nThank you for using ManekTech AI-powered Chatbot!")

if __name__ == "__main__":
    main()
