#!/usr/bin/env python3
"""
Test Script for Ollama Connection
This script tests the basic Ollama connection and CrewAI setup.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ollama_connection():
    """Test the Ollama connection"""
    print("🧪 Testing Ollama Connection...")
    
    try:
        from config.ollama_config import test_ollama_connection
        success = test_ollama_connection()
        return success
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install the required packages: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error testing Ollama connection: {e}")
        return False

def test_tools():
    """Test the custom tools"""
    print("\n🧪 Testing Custom Tools...")
    
    try:
        from tools.job_analyzer import JobDescriptionAnalyzer
        from tools.email_templates import EmailTemplateManager
        
        # Test job analyzer
        analyzer = JobDescriptionAnalyzer()
        sample_jd = "Software Engineer position at TechCorp Inc. Requirements: Python, React, 3+ years experience."
        result = analyzer._run(sample_jd)
        print(f"✅ Job Analyzer: {result['role_title']} at {result['company']}")
        
        # Test email template manager
        template_manager = EmailTemplateManager()
        template = template_manager._run("software_engineer", {"company": "TestCorp"})
        print(f"✅ Email Template Manager: Template generated ({len(template)} characters)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing tools: {e}")
        return False

def test_agents():
    """Test agent creation"""
    print("\n🧪 Testing Agent Creation...")
    
    try:
        from agents.researcher import create_researcher_agent
        from agents.writer import create_writer_agent
        from agents.reviewer import create_reviewer_agent
        
        # Test creating agents
        researcher = create_researcher_agent()
        print(f"✅ Researcher Agent: {researcher.role}")
        
        writer = create_writer_agent()
        print(f"✅ Writer Agent: {writer.role}")
        
        reviewer = create_reviewer_agent()
        print(f"✅ Reviewer Agent: {reviewer.role}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing agents: {e}")
        return False

def test_personal_config():
    """Test personal configuration"""
    print("\n🧪 Testing Personal Configuration...")
    
    try:
        from config.personal_info import get_personal_info, get_customization_data
        
        personal_info = get_personal_info()
        print(f"✅ Personal Info: {personal_info['your_name']} - {personal_info['current_role']}")
        
        # Test customization data
        job_analysis = {
            "role_title": "Software Engineer",
            "company": "TestCorp",
            "industry": "Technology"
        }
        customization_data = get_customization_data(job_analysis)
        print(f"✅ Customization Data: Company={customization_data['company']}, Skills={customization_data['key_skills']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing personal config: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Ollama Connection and CrewAI Tests...\n")
    
    tests = [
        ("Ollama Connection", test_ollama_connection),
        ("Custom Tools", test_tools),
        ("Agent Creation", test_agents),
        ("Personal Configuration", test_personal_config)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Customize your personal information in config/personal_info.py")
        print("2. Run the main script: python jd_agent.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon issues:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Check that the deepseek-r1 model is available: ollama list")

if __name__ == "__main__":
    main()
