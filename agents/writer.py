"""
Email Writer Agent
This agent specializes in writing compelling, personalized job application emails.
"""

from crewai import Agent
from config.ollama_config import create_agent_with_ollama
from tools.email_templates import EmailTemplateManager

def create_writer_agent():
    """Create the professional email writer agent"""
    
    role = "Professional Email Writer"
    goal = "Write compelling, personalized job application emails based on research"
    backstory = """You are a professional email writer with expertise in job applications. 
    You know how to craft emails that stand out and show genuine interest in the company. 
    You have helped hundreds of candidates land interviews by writing emails that are 
    personal, professional, and compelling. You understand the psychology of what hiring 
    managers want to see and how to make candidates memorable."""
    
    tools = [EmailTemplateManager()]
    
    try:
        agent = create_agent_with_ollama(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools,
            verbose=True
        )
        return agent
    except Exception as e:
        print(f"Error creating writer agent: {e}")
        # Fallback to basic agent without Ollama
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools,
            verbose=True,
            allow_delegation=False
        )

if __name__ == "__main__":
    # Test the agent creation
    agent = create_writer_agent()
    print(f"✅ Writer agent created: {agent.role}")
