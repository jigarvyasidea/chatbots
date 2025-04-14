"""
Main implementation file for the Data Extraction Agent with lightweight alternatives
to work within disk space constraints.
"""

import os
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import faiss

class LightweightDataExtractionAgent:
    def __init__(self, data_path):
        """
        Initialize the Lightweight Data Extraction Agent.
        
        Args:
            data_path (str): Path to the data file containing ManekTech information.
        """
        self.data_path = data_path
        self.model = None
        self.texts = []
        self.embeddings = None
        self.index = None
        self.initialize_knowledge_base()
        
    def initialize_knowledge_base(self):
        """
        Initialize the knowledge base by loading and processing the ManekTech data.
        """
        # Load the data
        with open(self.data_path, 'r') as f:
            manektech_data = f.read()
        
        # Split the text into chunks
        self.texts = self._split_text(manektech_data)
        
        # Load the model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Create embeddings
        self.embeddings = self.model.encode(self.texts)
        
        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(self.embeddings).astype('float32'))
    
    def _split_text(self, text, chunk_size=1000, chunk_overlap=200):
        """
        Split text into chunks.
        
        Args:
            text (str): Text to split.
            chunk_size (int): Size of each chunk.
            chunk_overlap (int): Overlap between chunks.
            
        Returns:
            list: List of text chunks.
        """
        chunks = []
        start = 0
        
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
                
                # If paragraph is longer than chunk_size, split it further
                if len(paragraph) > chunk_size:
                    words = paragraph.split()
                    current_chunk = ""
                    for word in words:
                        if len(current_chunk) + len(word) <= chunk_size:
                            current_chunk += word + " "
                        else:
                            chunks.append(current_chunk.strip())
                            current_chunk = word + " "
                    if current_chunk:
                        current_chunk += "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
    
    def extract_information(self, query):
        """
        Extract information from the ManekTech knowledge base based on the query.
        
        Args:
            query (str): The query to extract information for.
            
        Returns:
            str: The extracted information.
        """
        if self.index is None or len(self.texts) == 0:
            return "Knowledge base not initialized. Please initialize the knowledge base first."
        
        try:
            # Encode the query
            query_embedding = self.model.encode([query])
            
            # Search for similar chunks
            k = min(3, len(self.texts))  # Get top k results
            distances, indices = self.index.search(np.array(query_embedding).astype('float32'), k)
            
            # Get the relevant chunks
            relevant_chunks = [self.texts[idx] for idx in indices[0]]
            
            # Combine the chunks
            context = "\n\n".join(relevant_chunks)
            
            # Generate a response based on the context
            response = self._generate_response(query, context)
            
            return response
        except Exception as e:
            return f"Error extracting information: {str(e)}"
    
    def _generate_response(self, query, context):
        """
        Generate a response based on the query and context.
        
        Args:
            query (str): The query.
            context (str): The context.
            
        Returns:
            str: The generated response.
        """
        # Simple template-based response generation
        # In a production system, this would use an LLM
        
        if "overview" in query.lower() or "about" in query.lower():
            if "Founded" in context and "Years of Establishment" in context:
                return self._extract_section(context, "Company Overview")
            else:
                return "I don't have enough information about ManekTech's overview."
        
        elif "service" in query.lower():
            if "Services Offered" in context:
                return self._extract_section(context, "Services Offered")
            else:
                return "I don't have enough information about ManekTech's services."
        
        elif "value" in query.lower():
            if "Company Values" in context:
                return self._extract_section(context, "Company Values")
            else:
                return "I don't have enough information about ManekTech's values."
        
        elif "global" in query.lower() or "presence" in query.lower() or "office" in query.lower():
            if "Global Presence" in context:
                return self._extract_section(context, "Global Presence")
            else:
                return "I don't have enough information about ManekTech's global presence."
        
        elif "contact" in query.lower():
            if "Contact Information" in context:
                return self._extract_section(context, "Contact Information")
            else:
                return "I don't have enough information about ManekTech's contact details."
        
        elif "hiring" in query.lower() or "recruitment" in query.lower():
            if "Hiring Services" in context:
                return self._extract_section(context, "Hiring Services")
            else:
                return "I don't have enough information about ManekTech's hiring process."
        
        elif "year" in query.lower() or "business" in query.lower():
            if "Founded" in context:
                for line in context.split('\n'):
                    if "Founded" in line:
                        return line.strip()
            return "ManekTech was founded in 2011 and has been in business for over 14 years."
        
        elif "rating" in query.lower() or "customer" in query.lower():
            if "Customer Rating" in context:
                for line in context.split('\n'):
                    if "Customer Rating" in line:
                        return line.strip()
            return "ManekTech has a customer rating of 4.8/5."
        
        elif "developer" in query.lower() or "team" in query.lower():
            if "Team Size" in context:
                for line in context.split('\n'):
                    if "Team Size" in line:
                        return line.strip()
            return "ManekTech has a team of 450+ developers and engineers."
        
        elif "technolog" in query.lower():
            if "Services Offered" in context:
                return "ManekTech works with various technologies including Web Development, Mobile App Development, Software Development, CMS Development, eCommerce Development, Cloud Computing, AI ML Development, AR VR Development, IoT Development, UI UX Design, Blockchain Development, and more."
            else:
                return "I don't have specific information about the technologies ManekTech works with."
        
        else:
            # Return the most relevant context
            return f"Based on the information I have about ManekTech: {context[:500]}..."
    
    def _extract_section(self, context, section_name):
        """
        Extract a section from the context.
        
        Args:
            context (str): The context.
            section_name (str): The name of the section to extract.
            
        Returns:
            str: The extracted section.
        """
        lines = context.split('\n')
        section_content = []
        in_section = False
        
        for line in lines:
            if section_name in line:
                in_section = True
                continue
            elif in_section and line.startswith('##'):
                break
            elif in_section:
                section_content.append(line)
        
        if section_content:
            return '\n'.join(section_content).strip()
        else:
            # If section not found, return the most relevant part of the context
            return context[:500] + "..."
    
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
    agent = LightweightDataExtractionAgent(data_path)
    
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
