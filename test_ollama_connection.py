#!/usr/bin/env python3
"""
Test script to verify Ollama connection and CrewAI integration
"""

import requests
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ollama_service():
    """Test if Ollama service is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama service is running")
            return True
        else:
            print(f"⚠️  Ollama responded with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        return False

def test_crewai_ollama_integration():
    """Test CrewAI Ollama integration"""
    try:
        from langchain_community.llms import Ollama
        
        print("🔍 Testing CrewAI Ollama integration...")
        llm = Ollama(
            model="ollama/deepseek-r1:1.5b",
            base_url="http://localhost:11434"
        )
        
        print("✅ CrewAI Ollama LLM instance created successfully")
        return True
        
    except Exception as e:
        print(f"❌ CrewAI Ollama integration failed: {e}")
        return False

def test_agent_creation():
    """Test if we can create CrewAI agents with Ollama"""
    try:
        from crewai import Agent
        from langchain_community.llms import Ollama
        
        print("🔍 Testing agent creation with Ollama...")
        
        llm = Ollama(
            model="ollama/deepseek-r1:1.5b",
            base_url="http://localhost:11434"
        )
        
        # Try to create a simple agent
        agent = Agent(
            role="Test Agent",
            goal="Test the Ollama integration",
            backstory="A test agent to verify Ollama works with CrewAI",
            llm=llm,
            verbose=False
        )
        
        print("✅ Agent created successfully with Ollama LLM")
        return True
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Ollama and CrewAI Integration")
    print("=" * 50)
    
    # Test 1: Ollama service
    if not test_ollama_service():
        print("\n❌ Ollama service test failed")
        print("Please ensure Ollama is running: ollama serve")
        return False
    
    # Test 2: CrewAI Ollama integration
    if not test_crewai_ollama_integration():
        print("\n❌ CrewAI Ollama integration test failed")
        return False
    
    # Test 3: Agent creation
    if not test_agent_creation():
        print("\n❌ Agent creation test failed")
        return False
    
    print("\n🎉 All tests passed! Ollama is properly configured with CrewAI.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
