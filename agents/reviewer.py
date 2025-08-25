"""
Email Reviewer Agent
This agent specializes in reviewing and improving job application emails.
"""

from crewai import Agent
from config.ollama_config import create_agent_with_ollama

def create_reviewer_agent():
    """Create the email quality reviewer agent"""
    
    role = "Email Quality Reviewer"
    goal = "Review and improve email drafts to ensure they are professional and compelling"
    backstory = """You are an expert at reviewing professional communications. 
    You can identify areas for improvement and suggest enhancements to make emails more effective. 
    You have a keen eye for grammar, tone, and structure. You know how to make emails 
    more compelling while maintaining professionalism. You've helped countless professionals 
    improve their communication skills and increase their success rates."""
    
    try:
        agent = create_agent_with_ollama(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=[],
            verbose=True
        )
        return agent
    except Exception as e:
        print(f"Error creating reviewer agent: {e}")
        # Fallback to basic agent without Ollama
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=[],
            verbose=True,
            allow_delegation=False
        )

if __name__ == "__main__":
    # Test the agent creation
    agent = create_reviewer_agent()
    print(f"✅ Reviewer agent created: {agent.role}")
