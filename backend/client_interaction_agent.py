"""
Client Interaction Agent for ManekTech Chatbot

This agent is responsible for mimicking human responses for client interactions.
It provides natural, conversational responses to client queries.
"""

import re
import random

class ClientInteractionAgent:
    def __init__(self, data_extraction_agent):
        """
        Initialize the Client Interaction Agent.
        
        Args:
            data_extraction_agent: The data extraction agent to get company information.
        """
        self.data_extraction_agent = data_extraction_agent
        self.conversation_history = []
        self.greeting_phrases = [
            "Hi there! How can I help you today?",
            "Hello! Welcome to ManekTech. What can I assist you with?",
            "Good day! I'm here to help with any questions about ManekTech.",
            "Welcome! How may I assist you with ManekTech's services today?"
        ]
        self.thinking_phrases = [
            "Let me think about that...",
            "That's a good question. Let me check...",
            "I'm looking into that for you...",
            "Just a moment while I find that information..."
        ]
        self.positive_phrases = [
            "Absolutely!",
            "Definitely!",
            "Of course!",
            "Certainly!"
        ]
        self.transition_phrases = [
            "By the way,",
            "I should mention that",
            "It's worth noting that",
            "I'd like to add that"
        ]
        self.follow_up_questions = [
            "Is there anything specific about our services you'd like to know?",
            "What kind of project are you looking to develop?",
            "Would you like to know more about our development process?",
            "Are you interested in any particular technology stack?"
        ]
        
    def get_response(self, user_input):
        """
        Get a human-like response to the user input.
        
        Args:
            user_input (str): The user's input message.
            
        Returns:
            str: The agent's response.
        """
        # Add user input to conversation history
        self.conversation_history.append(("user", user_input))
        
        # Check for greetings
        if self._is_greeting(user_input):
            response = self._handle_greeting()
        
        # Check for goodbyes
        elif self._is_goodbye(user_input):
            response = self._handle_goodbye()
        
        # Check for questions about services
        elif self._is_about_services(user_input):
            response = self._handle_services_question(user_input)
        
        # Check for questions about company
        elif self._is_about_company(user_input):
            response = self._handle_company_question(user_input)
        
        # Check for questions about contact
        elif self._is_about_contact(user_input):
            response = self._handle_contact_question(user_input)
        
        # Check for questions about technologies
        elif self._is_about_technologies(user_input):
            response = self._handle_technologies_question(user_input)
        
        # Check for questions about projects or portfolio
        elif self._is_about_projects(user_input):
            response = self._handle_projects_question(user_input)
        
        # Check for questions about pricing
        elif self._is_about_pricing(user_input):
            response = self._handle_pricing_question(user_input)
        
        # Check for questions about timeline
        elif self._is_about_timeline(user_input):
            response = self._handle_timeline_question(user_input)
        
        # Default response for other queries
        else:
            response = self._handle_general_question(user_input)
        
        # Add response to conversation history
        self.conversation_history.append(("agent", response))
        
        return response
    
    def _is_greeting(self, text):
        """Check if the text is a greeting."""
        greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]
        return any(greeting in text.lower() for greeting in greetings)
    
    def _is_goodbye(self, text):
        """Check if the text is a goodbye."""
        goodbyes = ["bye", "goodbye", "see you", "talk to you later", "farewell"]
        return any(goodbye in text.lower() for goodbye in goodbyes)
    
    def _is_about_services(self, text):
        """Check if the text is about services."""
        keywords = ["service", "offer", "provide", "solution", "develop", "build", "create"]
        return any(keyword in text.lower() for keyword in keywords)
    
    def _is_about_company(self, text):
        """Check if the text is about the company."""
        keywords = ["company", "about", "manektech", "business", "organization", "team", "history"]
        return any(keyword in text.lower() for keyword in keywords)
    
    def _is_about_contact(self, text):
        """Check if the text is about contact information."""
        keywords = ["contact", "email", "phone", "reach", "call", "message", "connect"]
        return any(keyword in text.lower() for keyword in keywords)
    
    def _is_about_technologies(self, text):
        """Check if the text is about technologies."""
        keywords = ["technology", "tech", "stack", "framework", "language", "platform", "tool"]
        return any(keyword in text.lower() for keyword in keywords)
    
    def _is_about_projects(self, text):
        """Check if the text is about projects or portfolio."""
        keywords = ["project", "portfolio", "work", "case study", "client", "previous", "example"]
        return any(keyword in text.lower() for keyword in keywords)
    
    def _is_about_pricing(self, text):
        """Check if the text is about pricing."""
        keywords = ["price", "cost", "budget", "expensive", "affordable", "quote", "estimate"]
        return any(keyword in text.lower() for keyword in keywords)
    
    def _is_about_timeline(self, text):
        """Check if the text is about timeline."""
        keywords = ["time", "timeline", "deadline", "duration", "schedule", "when", "long"]
        return any(keyword in text.lower() for keyword in keywords)
    
    def _handle_greeting(self):
        """Handle greeting messages."""
        return random.choice(self.greeting_phrases)
    
    def _handle_goodbye(self):
        """Handle goodbye messages."""
        return "Thank you for chatting with us today! If you have any more questions about ManekTech's services, feel free to reach out. Have a great day!"
    
    def _handle_services_question(self, user_input):
        """Handle questions about services."""
        thinking = random.choice(self.thinking_phrases)
        positive = random.choice(self.positive_phrases)
        
        # Get services information from data extraction agent
        services_info = self.data_extraction_agent.get_services()
        
        # Create a more conversational response
        response = f"{thinking} {positive} ManekTech offers a wide range of services. {services_info}"
        
        # Add a follow-up question
        if random.random() < 0.7:  # 70% chance to add a follow-up
            response += f" {random.choice(self.follow_up_questions)}"
        
        return response
    
    def _handle_company_question(self, user_input):
        """Handle questions about the company."""
        thinking = random.choice(self.thinking_phrases)
        
        # Get company information from data extraction agent
        company_info = self.data_extraction_agent.get_company_overview()
        
        # Create a more conversational response
        response = f"{thinking} ManekTech is a leading software development company. {company_info}"
        
        # Add a transition to values
        if random.random() < 0.5:  # 50% chance to add company values
            values_info = self.data_extraction_agent.get_company_values()
            transition = random.choice(self.transition_phrases)
            response += f" {transition} {values_info}"
        
        return response
    
    def _handle_contact_question(self, user_input):
        """Handle questions about contact information."""
        positive = random.choice(self.positive_phrases)
        
        # Get contact information from data extraction agent
        contact_info = self.data_extraction_agent.get_contact_information()
        
        # Create a more conversational response
        response = f"{positive} You can easily get in touch with ManekTech. {contact_info}"
        
        # Add a suggestion
        response += " Would you like me to schedule a call with our team to discuss your project requirements?"
        
        return response
    
    def _handle_technologies_question(self, user_input):
        """Handle questions about technologies."""
        thinking = random.choice(self.thinking_phrases)
        
        # Create a conversational response about technologies
        response = f"{thinking} ManekTech works with a wide range of cutting-edge technologies. Our team is proficient in Web Development (React, Angular, Vue.js), Mobile App Development (iOS, Android, React Native, Flutter), Backend Development (Node.js, Python, Java, .NET), Database Management (SQL, NoSQL), Cloud Services (AWS, Azure, Google Cloud), and emerging technologies like AI/ML, Blockchain, and IoT."
        
        # Add a question about their project
        response += " What kind of technology stack are you considering for your project?"
        
        return response
    
    def _handle_projects_question(self, user_input):
        """Handle questions about projects or portfolio."""
        positive = random.choice(self.positive_phrases)
        
        # Create a conversational response about projects
        response = f"{positive} ManekTech has successfully delivered over 2000+ projects since 2011. Our portfolio includes work for startups, small-mid sized companies, and Fortune 500+ companies including Nestle and NYSE. We've developed custom software solutions, web applications, mobile apps, and enterprise systems across various industries including finance, healthcare, e-commerce, education, and more."
        
        # Add a suggestion
        response += " I'd be happy to connect you with our team to discuss specific case studies relevant to your industry. Would that be helpful?"
        
        return response
    
    def _handle_pricing_question(self, user_input):
        """Handle questions about pricing."""
        thinking = random.choice(self.thinking_phrases)
        
        # Create a conversational response about pricing
        response = f"{thinking} ManekTech offers flexible pricing models tailored to your project needs. We provide hourly rates, fixed project costs, and dedicated team arrangements. Each project is unique, so the cost depends on factors like project complexity, timeline, features, and the required expertise."
        
        # Add a call to action
        response += " To get an accurate estimate for your specific requirements, I'd recommend scheduling a consultation with our team. Would you like me to arrange that for you?"
        
        return response
    
    def _handle_timeline_question(self, user_input):
        """Handle questions about timeline."""
        thinking = random.choice(self.thinking_phrases)
        
        # Create a conversational response about timeline
        response = f"{thinking} Project timelines at ManekTech vary based on the scope and complexity. A simple website might take 4-6 weeks, while a complex enterprise application could take several months. We pride ourselves on on-time delivery and have a strong track record of meeting deadlines."
        
        # Add a personalized touch
        response += " To provide you with a more accurate timeline for your specific project, our team would need to understand your requirements in detail. Would you like to share more about your project scope?"
        
        return response
    
    def _handle_general_question(self, user_input):
        """Handle general questions by passing to the data extraction agent."""
        thinking = random.choice(self.thinking_phrases)
        
        # Get information from data extraction agent
        info = self.data_extraction_agent.extract_information(user_input)
        
        # Create a conversational response
        response = f"{thinking} {info}"
        
        # Add a follow-up question if the response is short
        if len(response) < 200 and random.random() < 0.7:  # 70% chance to add a follow-up for short responses
            response += f" {random.choice(self.follow_up_questions)}"
        
        return response


# Example usage
if __name__ == "__main__":
    # Mock data extraction agent for testing
    class MockDataExtractionAgent:
        def extract_information(self, query):
            return "This is mock information about ManekTech based on your query."
        
        def get_company_overview(self):
            return "ManekTech is a software development company founded in 2011 with 450+ developers."
        
        def get_services(self):
            return "ManekTech offers web development, mobile app development, and custom software development services."
        
        def get_company_values(self):
            return "ManekTech values integrity, quality, and on-time delivery."
        
        def get_contact_information(self):
            return "You can contact ManekTech at info@manektech.com or +91 851 142 8441."
    
    # Create client interaction agent
    mock_data_agent = MockDataExtractionAgent()
    agent = ClientInteractionAgent(mock_data_agent)
    
    # Test with different inputs
    test_inputs = [
        "Hello there",
        "What services does ManekTech offer?",
        "Tell me about your company",
        "How can I contact you?",
        "What technologies do you work with?",
        "Can you show me some of your projects?",
        "How much do your services cost?",
        "How long does it take to develop an app?",
        "Goodbye"
    ]
    
    for input_text in test_inputs:
        print(f"\nUser: {input_text}")
        response = agent.get_response(input_text)
        print(f"Agent: {response}")
