"""
Test script for the Hiring Query Agent
"""

import sys
import os

# Add the parent directory to the path to import the agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.hiring_query_agent import HiringQueryAgent
from backend.ultra_lightweight_extraction_agent import UltraLightweightDataExtractionAgent

def test_hiring_query_agent():
    """Test the Hiring Query Agent functionality"""
    data_path = "./data/manektech_info.md"
    
    print("Initializing Data Extraction Agent...")
    data_agent = UltraLightweightDataExtractionAgent(data_path)
    
    print("Initializing Hiring Query Agent...")
    hiring_agent = HiringQueryAgent(data_agent)
    
    print("\n===== Testing Hiring Query Agent =====")
    
    test_inputs = [
        "Are you hiring?",
        "What's the work culture like at ManekTech?",
        "How does your hiring process work?",
        "What skills do you look for in web developers?",
        "What skills do you look for in mobile developers?",
        "What benefits do you offer to employees?",
        "Are there opportunities for career growth?",
        "Do you allow remote work?",
        "What is your interview process like?",
        "Tell me about working at ManekTech"
    ]
    
    for input_text in test_inputs:
        print(f"\nUser: {input_text}")
        response = hiring_agent.get_response(input_text)
        print(f"Agent: {response}")

if __name__ == "__main__":
    test_hiring_query_agent()
