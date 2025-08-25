"""
Job Research Agent
This agent specializes in analyzing job descriptions and researching companies.
"""

from crewai import Agent
from config.ollama_config import create_agent_with_ollama
from tools.job_analyzer import JobDescriptionAnalyzer

def create_researcher_agent():
    """Create the job research specialist agent"""
    
    role = "Job Research Specialist"
    goal = "Analyze job descriptions and research companies to understand requirements and culture"
    backstory = """You are an expert at analyzing job descriptions and researching companies. 
    You can quickly identify key requirements, company culture, and industry trends. 
    You have years of experience in HR and recruitment, and you know what makes a job posting 
    attractive to candidates and what companies are looking for in their ideal hires."""
    
    tools = [JobDescriptionAnalyzer()]
    
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
        print(f"Error creating researcher agent: {e}")
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
    agent = create_researcher_agent()
    print(f"✅ Researcher agent created: {agent.role}")
