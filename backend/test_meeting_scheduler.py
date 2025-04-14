"""
Test script for the Meeting Scheduler Agent
"""

import sys
import os

# Add the parent directory to the path to import the agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.meeting_scheduler_agent import MeetingSchedulerAgent
from backend.ultra_lightweight_extraction_agent import UltraLightweightDataExtractionAgent

def test_meeting_scheduler_agent():
    """Test the Meeting Scheduler Agent functionality"""
    data_path = "./data/manektech_info.md"
    
    print("Initializing Data Extraction Agent...")
    data_agent = UltraLightweightDataExtractionAgent(data_path)
    
    print("Initializing Meeting Scheduler Agent...")
    scheduler_agent = MeetingSchedulerAgent(data_agent)
    
    print("\n===== Testing Meeting Scheduler Agent =====")
    
    # Test with a conversation flow
    conversation = [
        "I'd like to schedule a meeting",
        "Project Discussion",
        "Wednesday",
        "1:00 PM",
        "My name is John Smith",
        "john.smith@example.com",
        "555-123-4567",
        "Yes, that looks correct",
        "Is there anything else I need to prepare for the meeting?"
    ]
    
    for input_text in conversation:
        print(f"\nUser: {input_text}")
        response = scheduler_agent.get_response(input_text)
        print(f"Agent: {response}")
    
    print("\n===== Testing New Meeting Request =====")
    
    # Test starting a new meeting after one is completed
    new_conversation = [
        "I'd like to schedule another meeting",
        "Technical Consultation",
        "Friday",
        "11:00 AM",
        "My name is Jane Doe",
        "jane.doe@example.com",
        "Yes, that's correct"
    ]
    
    for input_text in new_conversation:
        print(f"\nUser: {input_text}")
        response = scheduler_agent.get_response(input_text)
        print(f"Agent: {response}")
    
    print("\n===== Testing General Meeting Queries =====")
    
    general_queries = [
        "What are your available meeting times?",
        "How do I schedule a meeting?",
        "Can I cancel a meeting?",
        "Do you have meetings on weekends?"
    ]
    
    # Reset the agent state
    scheduler_agent.meeting_state = "initial"
    scheduler_agent.current_meeting = {}
    
    for input_text in general_queries:
        print(f"\nUser: {input_text}")
        response = scheduler_agent.get_response(input_text)
        print(f"Agent: {response}")

if __name__ == "__main__":
    test_meeting_scheduler_agent()
