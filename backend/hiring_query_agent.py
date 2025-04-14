"""
Hiring Query Agent for ManekTech Chatbot

This agent is responsible for handling hiring-related queries and providing
positive responses about the company.
"""

import re
import random

class HiringQueryAgent:
    def __init__(self, data_extraction_agent):
        """
        Initialize the Hiring Query Agent.
        
        Args:
            data_extraction_agent: The data extraction agent to get company information.
        """
        self.data_extraction_agent = data_extraction_agent
        self.conversation_history = []
        self.positive_phrases = [
            "I'm excited to share that",
            "I'm happy to tell you that",
            "You'll be pleased to know that",
            "It's worth highlighting that"
        ]
        self.enthusiasm_phrases = [
            "ManekTech is an amazing place to work!",
            "Working at ManekTech is truly rewarding!",
            "ManekTech offers an exceptional work environment!",
            "ManekTech is known for its fantastic work culture!"
        ]
        self.culture_highlights = [
            "We embrace a wide range of philosophies, cultures, and individuals with great respect.",
            "Our team is like a close-knit family that believes in working together.",
            "We foster a culture of innovation, learning, and growth.",
            "We provide a platform for our team to demonstrate their distinct abilities."
        ]
        self.benefits_highlights = [
            "ManekTech offers competitive compensation packages and excellent growth opportunities.",
            "We provide continuous learning opportunities, flexible work arrangements, and a collaborative environment.",
            "Our benefits include health insurance, professional development programs, and team-building activities.",
            "We celebrate achievements and recognize outstanding contributions from our team members."
        ]
        
    def get_response(self, user_input):
        """
        Get a positive response to hiring-related queries.
        
        Args:
            user_input (str): The user's input message.
            
        Returns:
            str: The agent's response.
        """
        # Add user input to conversation history
        self.conversation_history.append(("user", user_input))
        
        # Check for different types of hiring queries
        if self._is_about_job_openings(user_input):
            response = self._handle_job_openings_query()
        elif self._is_about_work_culture(user_input):
            response = self._handle_work_culture_query()
        elif self._is_about_hiring_process(user_input):
            response = self._handle_hiring_process_query()
        elif self._is_about_skills_required(user_input):
            response = self._handle_skills_required_query(user_input)
        elif self._is_about_benefits(user_input):
            response = self._handle_benefits_query()
        elif self._is_about_career_growth(user_input):
            response = self._handle_career_growth_query()
        elif self._is_about_remote_work(user_input):
            response = self._handle_remote_work_query()
        elif self._is_about_interview_process(user_input):
            response = self._handle_interview_process_query()
        else:
            # Default to general hiring information
            response = self._handle_general_hiring_query()
        
        # Add response to conversation history
        self.conversation_history.append(("agent", response))
        
        return response
    
    def _is_about_job_openings(self, text):
        """Check if the text is about job openings."""
        keywords = ["job", "opening", "vacancy", "position", "opportunity", "hiring", "career"]
        return any(keyword in text.lower() for keyword in keywords)
    
    def _is_about_work_culture(self, text):
        """Check if the text is about work culture."""
        keywords = ["culture", "environment", "atmosphere", "workplace", "team", "values"]
        return any(keyword in text.lower() for keyword in keywords)
    
    def _is_about_hiring_process(self, text):
        """Check if the text is about the hiring process."""
        keywords = ["process", "hire", "recruitment", "application", "apply", "join"]
        return any(keyword in text.lower() for keyword in keywords)
    
    def _is_about_skills_required(self, text):
        """Check if the text is about skills required."""
        keywords = ["skill", "requirement", "qualification", "experience", "expertise", "knowledge"]
        return any(keyword in text.lower() for keyword in keywords)
    
    def _is_about_benefits(self, text):
        """Check if the text is about benefits."""
        keywords = ["benefit", "perk", "salary", "compensation", "package", "offer"]
        return any(keyword in text.lower() for keyword in keywords)
    
    def _is_about_career_growth(self, text):
        """Check if the text is about career growth."""
        keywords = ["growth", "advancement", "promotion", "development", "progress", "learn"]
        return any(keyword in text.lower() for keyword in keywords)
    
    def _is_about_remote_work(self, text):
        """Check if the text is about remote work."""
        keywords = ["remote", "work from home", "wfh", "telecommute", "virtual", "offshore"]
        return any(keyword in text.lower() for keyword in keywords)
    
    def _is_about_interview_process(self, text):
        """Check if the text is about the interview process."""
        keywords = ["interview", "assessment", "test", "evaluation", "round", "selection"]
        return any(keyword in text.lower() for keyword in keywords)
    
    def _handle_job_openings_query(self):
        """Handle queries about job openings."""
        positive = random.choice(self.positive_phrases)
        enthusiasm = random.choice(self.enthusiasm_phrases)
        
        response = f"{enthusiasm} {positive} ManekTech is always looking for talented professionals to join our team of 450+ developers and engineers. We have openings across various roles including Web Developers, Mobile App Developers, UI/UX Designers, QA Engineers, Project Managers, and more."
        
        response += " Our team members have the opportunity to work on exciting projects for clients ranging from startups to Fortune 500 companies like Nestle and NYSE."
        
        response += " Would you like to know more about specific roles or our hiring process?"
        
        return response
    
    def _handle_work_culture_query(self):
        """Handle queries about work culture."""
        positive = random.choice(self.positive_phrases)
        culture = random.choice(self.culture_highlights)
        
        response = f"{positive} ManekTech has fostered an exceptional work culture since its founding in 2011. {culture} We believe in maintaining a healthy work-life balance and creating an environment where innovation thrives."
        
        response += " Our leadership team is approachable and supportive, always encouraging new ideas and perspectives. We celebrate diversity and inclusion, with team members from various backgrounds and cultures."
        
        response += " Would you like to know more about what makes ManekTech a great place to work?"
        
        return response
    
    def _handle_hiring_process_query(self):
        """Handle queries about the hiring process."""
        positive = random.choice(self.positive_phrases)
        
        response = f"{positive} ManekTech has a streamlined and efficient hiring process designed to identify the best talent. Our typical process includes:"
        
        response += "\n\n1. Application review: We carefully evaluate your resume and portfolio."
        response += "\n2. Technical assessment: A brief test to evaluate your technical skills relevant to the position."
        response += "\n3. First interview: A discussion about your experience and how you approach problems."
        response += "\n4. Technical interview: A deeper dive into your technical expertise."
        response += "\n5. Final interview: Meeting with the team leads or management to ensure a good cultural fit."
        
        response += "\n\nThe entire process typically takes 1-2 weeks, and we pride ourselves on providing timely feedback to all candidates. Would you like to know more about any specific stage of our hiring process?"
        
        return response
    
    def _handle_skills_required_query(self, user_input):
        """Handle queries about skills required."""
        positive = random.choice(self.positive_phrases)
        
        # Check for specific technology mentions
        technologies = {
            "web": "For web development roles, we value expertise in React, Angular, Vue.js, Node.js, and modern JavaScript frameworks. Experience with responsive design and performance optimization is a plus.",
            "mobile": "For mobile development positions, we look for skills in native iOS (Swift) and Android (Kotlin/Java) development, as well as cross-platform frameworks like React Native and Flutter.",
            "ui": "For UI/UX design roles, proficiency in tools like Figma, Adobe XD, and Sketch is important, along with a strong portfolio demonstrating user-centered design principles.",
            "backend": "For backend development, we value experience with Node.js, Python, Java, .NET, and database technologies including SQL and NoSQL solutions.",
            "devops": "For DevOps positions, expertise in CI/CD pipelines, containerization (Docker, Kubernetes), and cloud platforms (AWS, Azure, GCP) is highly valued.",
            "ai": "For AI/ML roles, we look for experience with Python, TensorFlow, PyTorch, and a strong foundation in mathematics and statistics.",
            "blockchain": "For blockchain development, knowledge of smart contracts, Solidity, and experience with platforms like Ethereum or Hyperledger is important."
        }
        
        # Default response if no specific technology is mentioned
        tech_response = "At ManekTech, we value both technical expertise and soft skills. Technical requirements vary by position, but we generally look for proficiency in relevant programming languages and frameworks, problem-solving abilities, and a passion for learning new technologies."
        
        # Check if any technology is mentioned in the query
        for tech, description in technologies.items():
            if tech in user_input.lower():
                tech_response = description
                break
        
        response = f"{positive} {tech_response}"
        
        response += " Beyond technical skills, we highly value soft skills such as effective communication, teamwork, adaptability, and a growth mindset. We believe that the right attitude and willingness to learn are just as important as technical expertise."
        
        response += " Would you like to know more about specific roles or technologies we work with?"
        
        return response
    
    def _handle_benefits_query(self):
        """Handle queries about benefits."""
        positive = random.choice(self.positive_phrases)
        benefits = random.choice(self.benefits_highlights)
        
        response = f"{positive} ManekTech offers an excellent benefits package to our team members. {benefits}"
        
        response += " Our comprehensive benefits are designed to support both professional growth and personal well-being. We believe in recognizing and rewarding the contributions of our team members."
        
        response += " Some specific benefits include competitive salaries, health insurance, paid time off, flexible work arrangements, professional development opportunities, and regular team-building activities."
        
        response += " Would you like to know more about our compensation packages or other aspects of working at ManekTech?"
        
        return response
    
    def _handle_career_growth_query(self):
        """Handle queries about career growth."""
        positive = random.choice(self.positive_phrases)
        
        response = f"{positive} ManekTech is committed to the professional growth and development of our team members. We provide clear career paths and advancement opportunities based on performance and skills development."
        
        response += " Our team members have access to continuous learning resources, including workshops, online courses, certifications, and mentorship programs. We encourage everyone to expand their skills and explore new technologies."
        
        response += " Many of our team leads and managers have grown within the company, starting in developer roles and advancing as they demonstrated their capabilities. We believe in promoting from within whenever possible."
        
        response += " Would you like to hear about specific success stories or career paths at ManekTech?"
        
        return response
    
    def _handle_remote_work_query(self):
        """Handle queries about remote work."""
        positive = random.choice(self.positive_phrases)
        
        response = f"{positive} ManekTech embraces flexible work arrangements, including remote work options. We have successfully implemented a hybrid work model that combines the benefits of in-office collaboration with the flexibility of remote work."
        
        response += " Our global team spans multiple countries, with offices in the USA, UK, India, Germany, and South Africa. We have robust systems and processes in place to ensure seamless collaboration across different locations and time zones."
        
        response += " We provide our remote team members with the necessary tools and support to be productive and connected. Regular virtual team meetings, collaborative platforms, and occasional in-person gatherings help maintain our strong team culture."
        
        response += " Would you like to know more about our remote work policies or global presence?"
        
        return response
    
    def _handle_interview_process_query(self):
        """Handle queries about the interview process."""
        positive = random.choice(self.positive_phrases)
        
        response = f"{positive} ManekTech's interview process is designed to be thorough yet efficient. We aim to create a positive experience that allows candidates to showcase their skills and learn about our company."
        
        response += " Our interviews typically include technical assessments relevant to the role, problem-solving scenarios, and discussions about past projects and experiences. We're interested in understanding not just what you've done, but how you approach challenges."
        
        response += " We provide clear information about each stage of the process and strive to give timely feedback. Our interviewers are experienced professionals who create a comfortable environment for open discussion."
        
        response += " Do you have specific questions about preparing for an interview with ManekTech?"
        
        return response
    
    def _handle_general_hiring_query(self):
        """Handle general hiring queries."""
        enthusiasm = random.choice(self.enthusiasm_phrases)
        culture = random.choice(self.culture_highlights)
        benefits = random.choice(self.benefits_highlights)
        
        response = f"{enthusiasm} {culture} {benefits}"
        
        response += " Since our founding in 2011, we've grown to a team of 450+ talented developers and engineers serving clients worldwide. Our team members enjoy working on diverse projects across various industries, using cutting-edge technologies."
        
        response += " If you're passionate about technology and looking for a dynamic, supportive environment where you can grow professionally, ManekTech could be the perfect fit for you."
        
        response += " Would you like to know more about specific job openings, our hiring process, or what it's like to work at ManekTech?"
        
        return response


# Example usage
if __name__ == "__main__":
    # Mock data extraction agent for testing
    class MockDataExtractionAgent:
        def extract_information(self, query):
            return "This is mock information about ManekTech based on your query."
        
        def get_company_overview(self):
            return "ManekTech is a software development company founded in 2011 with 450+ developers."
        
        def get_hiring_information(self):
            return "ManekTech offers dedicated remote developers from India on Hourly, Full-Time, and Part-Time basis."
    
    # Create hiring query agent
    mock_data_agent = MockDataExtractionAgent()
    agent = HiringQueryAgent(mock_data_agent)
    
    # Test with different inputs
    test_inputs = [
        "Are you hiring?",
        "What's the work culture like?",
        "How does your hiring process work?",
        "What skills do you look for in web developers?",
        "What benefits do you offer?",
        "Are there opportunities for career growth?",
        "Do you allow remote work?",
        "What is your interview process like?"
    ]
    
    for input_text in test_inputs:
        print(f"\nUser: {input_text}")
        response = agent.get_response(input_text)
        print(f"Agent: {response}")
