#!/usr/bin/env python3
"""
Check for conflicting environment variables that might cause OpenAI API key errors
"""

import os

def check_environment():
    """Check for potentially conflicting environment variables"""
    print("🔍 Checking environment variables...")
    print("=" * 50)
    
    # Check for OpenAI-related environment variables
    openai_vars = [
        "OPENAI_API_KEY",
        "OPENAI_API_BASE",
        "OPENAI_ORGANIZATION",
        "LITELLM_API_KEY",
        "LITELLM_MODEL",
        "LITELLM_BASE_URL"
    ]
    
    found_openai_vars = []
    for var in openai_vars:
        value = os.getenv(var)
        if value:
            found_openai_vars.append((var, value))
    
    if found_openai_vars:
        print("⚠️  Found OpenAI-related environment variables:")
        for var, value in found_openai_vars:
            # Mask the API key for security
            if "API_KEY" in var:
                masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
                print(f"   {var}: {masked_value}")
            else:
                print(f"   {var}: {value}")
        print("\n💡 These might be causing conflicts with Ollama.")
        print("   Consider unsetting them: unset OPENAI_API_KEY")
    else:
        print("✅ No OpenAI-related environment variables found")
    
    # Check for CrewAI-specific environment variables
    crewai_vars = [
        "CREWAI_LLM",
        "CREWAI_MODEL",
        "CREWAI_BASE_URL"
    ]
    
    found_crewai_vars = []
    for var in crewai_vars:
        value = os.getenv(var)
        if value:
            found_crewai_vars.append((var, value))
    
    if found_crewai_vars:
        print("\n⚠️  Found CrewAI-related environment variables:")
        for var, value in found_crewai_vars:
            print(f"   {var}: {value}")
    else:
        print("\n✅ No CrewAI-specific environment variables found")
    
    # Check for Ollama environment variables
    ollama_vars = [
        "OLLAMA_HOST",
        "OLLAMA_ORIGINS"
    ]
    
    found_ollama_vars = []
    for var in ollama_vars:
        value = os.getenv(var)
        if value:
            found_ollama_vars.append((var, value))
    
    if found_ollama_vars:
        print("\n✅ Found Ollama environment variables:")
        for var, value in found_ollama_vars:
            print(f"   {var}: {value}")
    else:
        print("\n✅ No Ollama environment variables found (using defaults)")
    
    print("\n" + "=" * 50)
    
    if found_openai_vars:
        print("🔧 RECOMMENDATIONS:")
        print("1. Unset OpenAI API key: unset OPENAI_API_KEY")
        print("2. Unset other OpenAI vars if not needed: unset OPENAI_API_BASE")
        print("3. Restart your terminal session")
        print("4. Try running the agent again")
        return False
    else:
        print("✅ Environment looks clean for Ollama usage")
        return True

if __name__ == "__main__":
    check_environment()
