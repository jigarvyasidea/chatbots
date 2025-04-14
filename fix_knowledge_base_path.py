"""
Path Fix for ManekTech AI Chatbot Knowledge Base

This script provides a fix for the knowledge base initialization issue by updating the file paths.
"""

import os
import sys

def fix_knowledge_base_path():
    """
    Fix the knowledge base path in the frontend application files.
    """
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the frontend files
    app_path = os.path.join(current_dir, "frontend", "app.py")
    app_tts_path = os.path.join(current_dir, "frontend", "app_with_tts.py")
    
    # Fix the path in app.py
    if os.path.exists(app_path):
        with open(app_path, 'r') as file:
            content = file.read()
        
        # Replace the relative path with an absolute path
        content = content.replace(
            "data_path = \"../data/manektech_info.md\"",
            "data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), \"data\", \"manektech_info.md\")"
        )
        
        with open(app_path, 'w') as file:
            file.write(content)
        
        print(f"Updated path in {app_path}")
    
    # Fix the path in app_with_tts.py
    if os.path.exists(app_tts_path):
        with open(app_tts_path, 'r') as file:
            content = file.read()
        
        # Replace the relative path with an absolute path
        content = content.replace(
            "data_path = \"../data/manektech_info.md\"",
            "data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), \"data\", \"manektech_info.md\")"
        )
        
        with open(app_tts_path, 'w') as file:
            file.write(content)
        
        print(f"Updated path in {app_tts_path}")
    
    # Verify the data file exists
    data_path = os.path.join(current_dir, "data", "manektech_info.md")
    if os.path.exists(data_path):
        print(f"Data file exists at: {data_path}")
    else:
        print(f"WARNING: Data file not found at: {data_path}")
        print("Please ensure the data/manektech_info.md file exists in your project directory.")

if __name__ == "__main__":
    print("ManekTech AI Chatbot - Knowledge Base Path Fix")
    print("=============================================")
    fix_knowledge_base_path()
    print("\nPath fix completed. Please try running the application again with:")
    print("python main.py")
