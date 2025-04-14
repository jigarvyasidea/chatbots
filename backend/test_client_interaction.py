"""
Test script for the Client Interaction Agent
"""

import sys
import os

# Add the parent directory to the path to import the agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.client_interaction_agent import ClientInteractionAgent
from backend.ultra_lightweight_extraction_agent import UltraLightweightDataExtractionAgent

def test_client_interaction_agent():
    """Test the Client Interaction Agent functionality"""
    data_path = "./data/manektech_info.md"
    
    print("Initializing Data Extraction Agent...")
    data_agent = UltraLightweightDataExtractionAgent(data_path)
    
    print("Initializing Client Interaction Agent...")
    client_agent = ClientInteractionAgent(data_agent)
    
    print("\n===== Testing Client Interaction Agent =====")
    
    test_inputs = [
        "Hello there",
        "What services does ManekTech offer?",
        "Tell me about your company",
        "How can I contact you?",
        "What technologies do you work with?",
        "Can you show me some of your projects?",
        "How much do your services cost?",
        "How long does it take to develop an app?",
        "Do you have experience with AI development?",
        "What is your hiring process?",
        "Where are your offices located?",
        "Goodbye"
    ]
    
    for input_text in test_inputs:
        print(f"\nUser: {input_text}")
        response = client_agent.get_response(input_text)
        print(f"Agent: {response}")

if __name__ == "__main__":
    test_client_interaction_agent()
