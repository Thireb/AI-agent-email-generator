"""
Ollama Configuration for CrewAI
Configures the local Ollama models for use with the job application email agent.
"""

import os
from crewai import Agent
from langchain_community.llms import Ollama

def get_ollama_llm(model_name: str = "ollama/deepseek-r1:1.5b"):
    """
    Get an Ollama LLM instance for use with CrewAI agents.
    
    Args:
        model_name (str): Name of the Ollama model to use (should include 'ollama/' prefix)
        
    Returns:
        Ollama: Configured LangChain Ollama LLM instance
    """
    try:
        llm = Ollama(
            model=model_name,
            base_url="http://localhost:11434"  # Default Ollama URL
        )
        return llm
    except Exception as e:
        print(f"Error initializing Ollama LLM: {e}")
        print("Please ensure Ollama is running and the model is available")
        return None

def create_agent_with_ollama(role: str, goal: str, backstory: str, tools=None, verbose: bool = True):
    """
    Create a CrewAI agent with Ollama LLM integration.
    
    Args:
        role (str): Agent's role
        goal (str): Agent's goal
        backstory (str): Agent's backstory
        tools: List of tools for the agent
        verbose (bool): Whether to enable verbose output
        
    Returns:
        Agent: Configured CrewAI agent
    """
    llm = get_ollama_llm()
    if llm is None:
        raise RuntimeError("Failed to initialize Ollama LLM")
    
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        tools=tools or [],
        verbose=verbose,
        allow_delegation=False,
        llm=llm
    )

# Available models for reference
AVAILABLE_MODELS = [
    "ollama/deepseek-r1:1.5b",      # 1.5B parameter model - good for basic tasks
    "ollama/all-minilm:latest",     # 45MB model - very fast but limited capability
    "ollama/nomic-embed-text:latest", # 274MB embedding model
    "ollama/mxbai-embed-large:latest" # 669MB embedding model
]

def list_available_models():
    """List all available Ollama models"""
    return AVAILABLE_MODELS

def test_ollama_connection():
    """Test the connection to Ollama"""
    try:
        llm = get_ollama_llm()
        if llm:
            # Simple test query
            response = llm.invoke("Hello, can you respond with 'Ollama is working'?")
            print(f"✅ Ollama connection successful! Response: {response}")
            return True
        else:
            print("❌ Failed to initialize Ollama LLM")
            return False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False
