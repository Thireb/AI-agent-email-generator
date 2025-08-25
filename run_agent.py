#!/usr/bin/env python3
"""
Simple Runner Script for Job Application Email Agent
This script provides an easy way to start the agent system.
"""

import sys
import os

def main():
    """Main runner function"""
    print("🤖 Job Application Email Agent")
    print("=" * 40)
    
    # Check if we should run tests first
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("🧪 Running tests first...")
        try:
            import test_ollama_connection
            test_ollama_connection.main()
            print("\n" + "=" * 40)
        except Exception as e:
            print(f"❌ Tests failed: {e}")
            print("Continuing anyway...\n")
    
    # Check if Ollama is running
    print("🔍 Checking Ollama connection...")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running")
        else:
            print("⚠️  Ollama responded but with unexpected status")
    except Exception as e:
        print("❌ Cannot connect to Ollama")
        print("Please make sure Ollama is running: ollama serve")
        print("Then try again.")
        return
    
    # Check if the required model is available
    print("🔍 Checking model availability...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = response.json().get("models", [])
        model_names = [model["name"] for model in models]
        
        if "deepseek-r1:1.5b" in model_names:
            print("✅ deepseek-r1:1.5b model is available")
        else:
            print("⚠️  deepseek-r1:1.5b model not found")
            print("Available models:", ", ".join(model_names))
            print("You can pull it with: ollama pull deepseek-r1:1.5b")
            print("Or modify config/ollama_config.py to use a different model")
    except Exception as e:
        print(f"⚠️  Could not check model availability: {e}")
    
    print("\n🚀 Starting the agent system...")
    print("=" * 40)
    
    try:
        # Import and run the main agent
        from jd_agent import main as run_agent
        run_agent()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error running agent: {e}")
        print("Check the error message above and try running the test script:")
        print("python test_ollama_connection.py")

if __name__ == "__main__":
    main()
