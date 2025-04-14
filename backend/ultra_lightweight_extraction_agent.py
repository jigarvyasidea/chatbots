"""
Ultra-lightweight Data Extraction Agent for ManekTech Chatbot

This agent is responsible for extracting and providing company information
from the ManekTech data gathered during research, using a simple keyword-based approach
that doesn't rely on external ML libraries to work within disk space constraints.
"""

import os
import re

class UltraLightweightDataExtractionAgent:
    def __init__(self, data_path):
        """
        Initialize the Ultra-Lightweight Data Extraction Agent.
        
        Args:
            data_path (str): Path to the data file containing ManekTech information.
        """
        self.data_path = data_path
        self.data = ""
        self.sections = {}
        self.load_data()
        
    def load_data(self):
        """
        Load and process the ManekTech data.
        """
        try:
            with open(self.data_path, 'r') as f:
                self.data = f.read()
            
            # Extract sections from the markdown file
            section_pattern = r'## ([^\n]+)\n(.*?)(?=\n## |$)'
            matches = re.findall(section_pattern, self.data, re.DOTALL)
            
            for section_title, section_content in matches:
                self.sections[section_title.strip()] = section_content.strip()
                
            # Also add the entire document as a section for fallback
            self.sections["Full Document"] = self.data
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
    
    def extract_information(self, query):
        """
        Extract information from the ManekTech knowledge base based on the query.
        
        Args:
            query (str): The query to extract information for.
            
        Returns:
            str: The extracted information.
        """
        if not self.data:
            return "Knowledge base not initialized. Please initialize the knowledge base first."
        
        try:
            # Convert query to lowercase for case-insensitive matching
            query_lower = query.lower()
            
            # Check for specific query types
            if any(keyword in query_lower for keyword in ["overview", "about", "company"]):
                if "Company Overview" in self.sections:
                    return self._format_response("Company Overview", self.sections["Company Overview"])
                
            elif any(keyword in query_lower for keyword in ["service", "offer"]):
                if "Services Offered" in self.sections:
                    return self._format_response("Services Offered", self.sections["Services Offered"])
                
            elif any(keyword in query_lower for keyword in ["value", "culture"]):
                if "Company Values" in self.sections:
                    return self._format_response("Company Values", self.sections["Company Values"])
                
            elif any(keyword in query_lower for keyword in ["global", "presence", "office", "location"]):
                if "Global Presence" in self.sections:
                    return self._format_response("Global Presence", self.sections["Global Presence"])
                
            elif any(keyword in query_lower for keyword in ["contact", "email", "phone"]):
                if "Contact Information" in self.sections:
                    return self._format_response("Contact Information", self.sections["Contact Information"])
                
            elif any(keyword in query_lower for keyword in ["hire", "hiring", "recruitment", "job"]):
                if "Hiring Services" in self.sections:
                    return self._format_response("Hiring Services", self.sections["Hiring Services"])
                
            # Check for specific fact queries
            elif any(keyword in query_lower for keyword in ["year", "founded", "established"]):
                pattern = r"Founded[:\s]*(.*?)(?:\n|$)"
                match = re.search(pattern, self.data)
                if match:
                    return f"ManekTech was founded in {match.group(1).strip()}."
                return "ManekTech was founded in 2011 and has been in business for over 14 years."
                
            elif any(keyword in query_lower for keyword in ["rating", "customer", "satisfaction"]):
                pattern = r"Customer Rating[:\s]*(.*?)(?:\n|$)"
                match = re.search(pattern, self.data)
                if match:
                    return f"ManekTech has a customer rating of {match.group(1).strip()}."
                return "ManekTech has a customer rating of 4.8/5."
                
            elif any(keyword in query_lower for keyword in ["developer", "team", "employee"]):
                pattern = r"Team Size[:\s]*(.*?)(?:\n|$)"
                match = re.search(pattern, self.data)
                if match:
                    return f"ManekTech has a team of {match.group(1).strip()}."
                return "ManekTech has a team of 450+ developers and engineers."
                
            elif any(keyword in query_lower for keyword in ["technolog", "tech stack", "framework"]):
                if "Services Offered" in self.sections:
                    return "ManekTech works with various technologies including Web Development, Mobile App Development, Software Development, CMS Development, eCommerce Development, Cloud Computing, AI ML Development, AR VR Development, IoT Development, UI UX Design, Blockchain Development, and more."
            
            # Fallback: Search for keywords in the entire document
            relevant_paragraphs = []
            query_keywords = [word.lower() for word in query.split() if len(word) > 3]
            
            paragraphs = self.data.split('\n\n')
            for paragraph in paragraphs:
                paragraph_lower = paragraph.lower()
                if any(keyword in paragraph_lower for keyword in query_keywords):
                    relevant_paragraphs.append(paragraph)
            
            if relevant_paragraphs:
                return "\n\n".join(relevant_paragraphs[:3])  # Return top 3 relevant paragraphs
            
            # Final fallback
            return "I don't have specific information about that. ManekTech is a custom software, web, and mobile app development company founded in 2011 with 450+ developers and engineers, serving startups, small-mid sized companies, and Fortune 500+ companies worldwide."
            
        except Exception as e:
            return f"Error extracting information: {str(e)}"
    
    def _format_response(self, section_title, section_content):
        """
        Format a response based on a section.
        
        Args:
            section_title (str): The title of the section.
            section_content (str): The content of the section.
            
        Returns:
            str: The formatted response.
        """
        # Clean up the content (remove markdown formatting, etc.)
        content = section_content.replace('- ', '').replace('*', '')
        
        # Limit the length of the response
        if len(content) > 1000:
            content = content[:997] + "..."
            
        return content
    
    def get_company_overview(self):
        """Get an overview of ManekTech company."""
        return self.extract_information("Give me an overview of ManekTech company.")
    
    def get_services(self):
        """Get information about ManekTech services."""
        return self.extract_information("What services does ManekTech offer?")
    
    def get_company_values(self):
        """Get information about ManekTech company values."""
        return self.extract_information("What are ManekTech's company values?")
    
    def get_global_presence(self):
        """Get information about ManekTech's global presence."""
        return self.extract_information("What is ManekTech's global presence?")
    
    def get_contact_information(self):
        """Get ManekTech's contact information."""
        return self.extract_information("What is ManekTech's contact information?")
    
    def get_hiring_information(self):
        """Get information about ManekTech's hiring process."""
        return self.extract_information("What is ManekTech's hiring process?")


# Example usage
if __name__ == "__main__":
    data_path = "../data/manektech_info.md"
    agent = UltraLightweightDataExtractionAgent(data_path)
    
    print("Company Overview:")
    print(agent.get_company_overview())
    
    print("\nServices:")
    print(agent.get_services())
    
    print("\nCompany Values:")
    print(agent.get_company_values())
    
    print("\nCustom Query:")
    query = "How many years has ManekTech been in business?"
    print(f"Query: {query}")
    print(agent.extract_information(query))
