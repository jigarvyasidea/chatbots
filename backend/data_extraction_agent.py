"""
Data Extraction Agent for ManekTech Chatbot

This agent is responsible for extracting and providing company information
from the ManekTech data gathered during research.
"""

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFaceHub

class DataExtractionAgent:
    def __init__(self, data_path):
        """
        Initialize the Data Extraction Agent.
        
        Args:
            data_path (str): Path to the data file containing ManekTech information.
        """
        self.data_path = data_path
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None
        self.qa_chain = None
        self.initialize_knowledge_base()
        
    def initialize_knowledge_base(self):
        """
        Initialize the knowledge base by loading and processing the ManekTech data.
        """
        # Load the data
        with open(self.data_path, 'r') as f:
            manektech_data = f.read()
        
        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        texts = text_splitter.split_text(manektech_data)
        
        # Create vector store
        self.vector_store = FAISS.from_texts(texts, self.embeddings)
        
        # Create QA chain
        template = """
        You are a helpful AI assistant that provides accurate information about ManekTech.
        Use only the following context to answer the question. If you don't know the answer, 
        just say you don't know. Don't make up an answer.
        
        Context: {context}
        
        Question: {question}
        
        Answer:
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Use HuggingFaceHub for the LLM
        llm = HuggingFaceHub(
            repo_id="google/flan-t5-base",
            model_kwargs={"temperature": 0.1, "max_length": 512}
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(),
            chain_type_kwargs={"prompt": prompt}
        )
    
    def extract_information(self, query):
        """
        Extract information from the ManekTech knowledge base based on the query.
        
        Args:
            query (str): The query to extract information for.
            
        Returns:
            str: The extracted information.
        """
        if not self.qa_chain:
            return "Knowledge base not initialized. Please initialize the knowledge base first."
        
        try:
            result = self.qa_chain.run(query)
            return result
        except Exception as e:
            return f"Error extracting information: {str(e)}"
    
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
    agent = DataExtractionAgent(data_path)
    
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
