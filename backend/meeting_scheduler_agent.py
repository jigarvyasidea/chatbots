"""
Meeting Scheduler Agent for ManekTech Chatbot

This agent is responsible for handling meeting scheduling requests.
It allows users to schedule meetings with ManekTech representatives.
"""

import re
import random
import datetime

class MeetingSchedulerAgent:
    def __init__(self, data_extraction_agent):
        """
        Initialize the Meeting Scheduler Agent.
        
        Args:
            data_extraction_agent: The data extraction agent to get company information.
        """
        self.data_extraction_agent = data_extraction_agent
        self.conversation_history = []
        self.current_meeting = {}
        self.meeting_state = "initial"  # States: initial, collecting_info, confirming, scheduled
        
        # Available time slots (simplified for demo)
        self.available_slots = {
            "Monday": ["10:00 AM", "2:00 PM", "4:00 PM"],
            "Tuesday": ["9:00 AM", "11:00 AM", "3:00 PM"],
            "Wednesday": ["10:00 AM", "1:00 PM", "4:00 PM"],
            "Thursday": ["9:00 AM", "2:00 PM", "5:00 PM"],
            "Friday": ["11:00 AM", "1:00 PM", "3:00 PM"]
        }
        
        # Meeting types
        self.meeting_types = [
            "General Inquiry",
            "Project Discussion",
            "Service Information",
            "Technical Consultation",
            "Hiring Discussion",
            "Partnership Opportunity"
        ]
        
        # ManekTech representatives (simplified for demo)
        self.representatives = {
            "General Inquiry": ["Sarah Johnson", "Michael Chen"],
            "Project Discussion": ["David Rodriguez", "Emily Wong"],
            "Service Information": ["James Wilson", "Priya Patel"],
            "Technical Consultation": ["Alex Kim", "Sophia Martinez"],
            "Hiring Discussion": ["Raj Sharma", "Lisa Thompson"],
            "Partnership Opportunity": ["Daniel Lee", "Olivia Brown"]
        }
        
    def get_response(self, user_input):
        """
        Process user input and provide appropriate response for meeting scheduling.
        
        Args:
            user_input (str): The user's input message.
            
        Returns:
            str: The agent's response.
        """
        # Add user input to conversation history
        self.conversation_history.append(("user", user_input))
        
        # Process based on current state
        if self.meeting_state == "initial":
            if self._is_scheduling_request(user_input):
                self.meeting_state = "collecting_info"
                response = self._start_scheduling()
            else:
                response = self._handle_general_query(user_input)
        
        elif self.meeting_state == "collecting_info":
            # Update meeting info based on user input
            self._update_meeting_info(user_input)
            
            # Check if we have all required information
            if self._has_all_required_info():
                self.meeting_state = "confirming"
                response = self._get_confirmation_message()
            else:
                # Ask for the next piece of information
                response = self._request_next_info()
        
        elif self.meeting_state == "confirming":
            if self._is_confirmation(user_input):
                self.meeting_state = "scheduled"
                response = self._confirm_meeting()
            elif self._is_rejection(user_input):
                # Reset and start over
                self.current_meeting = {}
                self.meeting_state = "initial"
                response = "I understand you'd like to make changes. Let's start over. Would you like to schedule a meeting with ManekTech?"
            else:
                # Handle modifications to the meeting
                self._handle_meeting_modification(user_input)
                response = self._get_confirmation_message()
        
        elif self.meeting_state == "scheduled":
            if self._is_scheduling_request(user_input):
                # Start a new meeting scheduling process
                self.current_meeting = {}
                self.meeting_state = "collecting_info"
                response = self._start_scheduling()
            else:
                response = "Your meeting has been scheduled. Is there anything else I can help you with?"
                self.meeting_state = "initial"
                self.current_meeting = {}
        
        # Add response to conversation history
        self.conversation_history.append(("agent", response))
        
        return response
    
    def _is_scheduling_request(self, text):
        """Check if the text is a meeting scheduling request."""
        keywords = ["schedule", "meeting", "appointment", "book", "call", "talk", "discuss", "meet"]
        return any(keyword in text.lower() for keyword in keywords)
    
    def _is_confirmation(self, text):
        """Check if the text is a confirmation."""
        confirmations = ["yes", "confirm", "correct", "right", "good", "ok", "okay", "sure", "perfect"]
        return any(confirmation in text.lower() for confirmation in confirmations)
    
    def _is_rejection(self, text):
        """Check if the text is a rejection."""
        rejections = ["no", "wrong", "incorrect", "change", "modify", "different", "not right", "cancel"]
        return any(rejection in text.lower() for rejection in rejections)
    
    def _start_scheduling(self):
        """Start the meeting scheduling process."""
        response = "I'd be happy to help you schedule a meeting with a ManekTech representative. "
        response += "Could you please tell me what type of meeting you're interested in? Here are some options:\n\n"
        
        for i, meeting_type in enumerate(self.meeting_types, 1):
            response += f"{i}. {meeting_type}\n"
        
        response += "\nPlease select a meeting type or describe your needs."
        
        return response
    
    def _update_meeting_info(self, user_input):
        """Update meeting information based on user input."""
        # Check for meeting type
        if "current_meeting" not in self.__dict__:
            self.current_meeting = {}
            
        if "type" not in self.current_meeting:
            for meeting_type in self.meeting_types:
                if meeting_type.lower() in user_input.lower():
                    self.current_meeting["type"] = meeting_type
                    break
            
            # Check for numeric selection
            if "type" not in self.current_meeting:
                for i, meeting_type in enumerate(self.meeting_types, 1):
                    if str(i) in user_input:
                        self.current_meeting["type"] = meeting_type
                        break
        
        # Check for day preference
        if "day" not in self.current_meeting:
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            for day in days:
                if day.lower() in user_input.lower():
                    self.current_meeting["day"] = day
                    break
        
        # Check for time preference
        if "time" not in self.current_meeting and "day" in self.current_meeting:
            for time_slot in self.available_slots[self.current_meeting["day"]]:
                if time_slot.lower() in user_input.lower():
                    self.current_meeting["time"] = time_slot
                    break
                # Check for hour mentions (e.g., "2 pm", "10 am")
                hour_pattern = r'(\d+)(?:\s*)(am|pm)'
                matches = re.findall(hour_pattern, user_input.lower())
                for match in matches:
                    hour, meridiem = match
                    for slot in self.available_slots[self.current_meeting["day"]]:
                        if f"{hour} {meridiem}" in slot.lower():
                            self.current_meeting["time"] = slot
                            break
        
        # Check for name
        if "name" not in self.current_meeting:
            name_pattern = r'(?:my name is|this is|i am|i\'m) ([a-zA-Z\s]+)'
            matches = re.findall(name_pattern, user_input.lower())
            if matches:
                self.current_meeting["name"] = matches[0].strip().title()
        
        # Check for email
        if "email" not in self.current_meeting:
            email_pattern = r'[\w\.-]+@[\w\.-]+'
            matches = re.findall(email_pattern, user_input.lower())
            if matches:
                self.current_meeting["email"] = matches[0]
        
        # Check for phone
        if "phone" not in self.current_meeting:
            phone_pattern = r'(?:\+\d{1,3}[-\.\s]?)?(?:\(?\d{3}\)?[-\.\s]?)?\d{3}[-\.\s]?\d{4}'
            matches = re.findall(phone_pattern, user_input)
            if matches:
                self.current_meeting["phone"] = matches[0]
    
    def _has_all_required_info(self):
        """Check if we have all required information for scheduling."""
        required_fields = ["type", "day", "time", "name", "email"]
        return all(field in self.current_meeting for field in required_fields)
    
    def _request_next_info(self):
        """Request the next piece of information needed."""
        if "type" not in self.current_meeting:
            return "What type of meeting are you interested in? Please select from the options I provided earlier."
        
        if "day" not in self.current_meeting:
            response = "What day would you prefer for the meeting? We have availability on "
            response += ", ".join(list(self.available_slots.keys())[:-1])
            response += f", and {list(self.available_slots.keys())[-1]}."
            return response
        
        if "time" not in self.current_meeting:
            day = self.current_meeting["day"]
            response = f"What time would work best for you on {day}? We have the following slots available: "
            response += ", ".join(self.available_slots[day])
            return response
        
        if "name" not in self.current_meeting:
            return "Could you please provide your name for the meeting?"
        
        if "email" not in self.current_meeting:
            return "What email address should we use to send the meeting confirmation?"
        
        if "phone" not in self.current_meeting:
            return "Could you please provide a phone number where we can reach you if needed? (This is optional)"
        
        return "Is there anything else you'd like to add about the meeting?"
    
    def _get_confirmation_message(self):
        """Generate a confirmation message with the meeting details."""
        meeting_type = self.current_meeting.get("type", "N/A")
        day = self.current_meeting.get("day", "N/A")
        time = self.current_meeting.get("time", "N/A")
        name = self.current_meeting.get("name", "N/A")
        email = self.current_meeting.get("email", "N/A")
        
        # Select a representative based on meeting type
        if meeting_type in self.representatives:
            representative = random.choice(self.representatives[meeting_type])
        else:
            representative = "a ManekTech representative"
        
        self.current_meeting["representative"] = representative
        
        response = "Great! Here's a summary of your meeting request:\n\n"
        response += f"Meeting Type: {meeting_type}\n"
        response += f"Day: {day}\n"
        response += f"Time: {time}\n"
        response += f"Your Name: {name}\n"
        response += f"Your Email: {email}\n"
        
        if "phone" in self.current_meeting:
            response += f"Your Phone: {self.current_meeting['phone']}\n"
        
        response += f"ManekTech Representative: {representative}\n\n"
        
        response += "Is this information correct? Please confirm or let me know if you need to make any changes."
        
        return response
    
    def _confirm_meeting(self):
        """Confirm the meeting and provide next steps."""
        meeting_type = self.current_meeting.get("type", "N/A")
        day = self.current_meeting.get("day", "N/A")
        time = self.current_meeting.get("time", "N/A")
        name = self.current_meeting.get("name", "N/A")
        representative = self.current_meeting.get("representative", "a ManekTech representative")
        
        # Calculate meeting date (simplified for demo)
        today = datetime.datetime.now()
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        today_day = days_of_week[today.weekday()]
        
        days_until_meeting = (days_of_week.index(day) - days_of_week.index(today_day)) % 7
        if days_until_meeting == 0:
            days_until_meeting = 7  # Schedule for next week if same day
        
        meeting_date = today + datetime.timedelta(days=days_until_meeting)
        date_str = meeting_date.strftime("%B %d, %Y")
        
        response = f"Perfect! Your meeting with {representative} has been scheduled for {day}, {date_str} at {time}. "
        response += f"The meeting will be about '{meeting_type}'. "
        
        response += f"You will receive a confirmation email shortly with the meeting details and a calendar invitation. "
        response += f"If you need to reschedule or have any questions, please contact us at info@manektech.com or +91 851 142 8441. "
        
        response += "Is there anything else I can help you with today?"
        
        return response
    
    def _handle_meeting_modification(self, user_input):
        """Handle modifications to the meeting details."""
        # Check for specific modifications
        if "type" in user_input.lower() or "meeting" in user_input.lower():
            self.current_meeting.pop("type", None)
            self._update_meeting_info(user_input)
        
        if "day" in user_input.lower() or "date" in user_input.lower():
            self.current_meeting.pop("day", None)
            self._update_meeting_info(user_input)
        
        if "time" in user_input.lower():
            self.current_meeting.pop("time", None)
            self._update_meeting_info(user_input)
        
        if "name" in user_input.lower():
            self.current_meeting.pop("name", None)
            self._update_meeting_info(user_input)
        
        if "email" in user_input.lower():
            self.current_meeting.pop("email", None)
            self._update_meeting_info(user_input)
        
        if "phone" in user_input.lower():
            self.current_meeting.pop("phone", None)
            self._update_meeting_info(user_input)
    
    def _handle_general_query(self, user_input):
        """Handle general queries about meetings."""
        if "available" in user_input.lower() or "time" in user_input.lower():
            response = "ManekTech representatives are generally available for meetings Monday through Friday, from 9:00 AM to 5:00 PM (IST/GMT+5:30). "
            response += "Would you like to schedule a meeting with one of our representatives?"
            return response
        
        if "how" in user_input.lower() and "schedule" in user_input.lower():
            response = "Scheduling a meeting with ManekTech is easy! I can help you with that right now. "
            response += "Would you like to schedule a meeting with one of our representatives?"
            return response
        
        if "cancel" in user_input.lower() or "reschedule" in user_input.lower():
            response = "If you need to cancel or reschedule a meeting, please contact us at info@manektech.com or +91 851 142 8441. "
            response += "Our team will be happy to assist you with rescheduling."
            return response
        
        # Default response
        response = "I can help you schedule a meeting with a ManekTech representative. "
        response += "Would you like to proceed with scheduling a meeting?"
        return response


# Example usage
if __name__ == "__main__":
    # Mock data extraction agent for testing
    class MockDataExtractionAgent:
        def extract_information(self, query):
            return "This is mock information about ManekTech based on your query."
        
        def get_contact_information(self):
            return "Email: info@manektech.com, Phone: +91 851 142 8441"
    
    # Create meeting scheduler agent
    mock_data_agent = MockDataExtractionAgent()
    agent = MeetingSchedulerAgent(mock_data_agent)
    
    # Test with a conversation flow
    conversation = [
        "I'd like to schedule a meeting",
        "Project Discussion",
        "Wednesday",
        "1:00 PM",
        "My name is John Smith",
        "john.smith@example.com",
        "555-123-4567",
        "Yes, that looks correct"
    ]
    
    for input_text in conversation:
        print(f"\nUser: {input_text}")
        response = agent.get_response(input_text)
        print(f"Agent: {response}")
