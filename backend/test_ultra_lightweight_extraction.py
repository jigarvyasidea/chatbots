"""
Test script for the Ultra-Lightweight Data Extraction Agent
"""

import sys
import os

# Add the parent directory to the path to import the agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.ultra_lightweight_extraction_agent import UltraLightweightDataExtractionAgent

def test_ultra_lightweight_data_extraction_agent():
    """Test the Ultra-Lightweight Data Extraction Agent functionality"""
    data_path = "./data/manektech_info.md"
    
    print("Initializing Ultra-Lightweight Data Extraction Agent...")
    agent = UltraLightweightDataExtractionAgent(data_path)
    
    print("\n===== Testing Company Overview =====")
    print(agent.get_company_overview())
    
    print("\n===== Testing Services Information =====")
    print(agent.get_services())
    
    print("\n===== Testing Company Values =====")
    print(agent.get_company_values())
    
    print("\n===== Testing Global Presence =====")
    print(agent.get_global_presence())
    
    print("\n===== Testing Contact Information =====")
    print(agent.get_contact_information())
    
    print("\n===== Testing Custom Queries =====")
    queries = [
        "How many years has ManekTech been in business?",
        "What is ManekTech's customer rating?",
        "How many developers does ManekTech have?",
        "What technologies does ManekTech work with?",
        "What is ManekTech's hiring process?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        print(agent.extract_information(query))

if __name__ == "__main__":
    test_ultra_lightweight_data_extraction_agent()
