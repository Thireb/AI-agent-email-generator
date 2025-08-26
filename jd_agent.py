#!/usr/bin/env python3
"""
Job Application Email Agent using CrewAI
This agent helps write personalized job application emails using local Ollama models and CV data.
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from typing import List, Dict, Any
from langchain_ollama import OllamaLLM
from tools.llm_cv_parser import LLMCVParser
from tools.personalization_engine import PersonalizationEngine

# Load environment variables
load_dotenv()

# Configure Ollama LLM
ollama_llm = OllamaLLM(
    model="ollama/gemma3:1b",
    base_url="http://localhost:11434"
)

# Initialize LLM-based CV parser and personalization engine
cv_parser = LLMCVParser()
cv_data = cv_parser.parse_cv()

if cv_data:
    personalization_engine = PersonalizationEngine(cv_data)
    print(f"✅ CV loaded: {cv_parser.get_summary()}")
else:
    personalization_engine = None
    print("⚠️  No CV data available - will use generic templates")

class JobDescriptionAnalyzer(BaseTool):
    """Tool for analyzing job descriptions and extracting key information"""
    
    name: str = "Job Description Analyzer"
    description: str = "Analyzes job descriptions to extract key requirements, company info, and role details"
    
    def _run(self, job_description: str) -> Dict[str, Any]:
        """Analyze the job description and return structured information"""
        # For now, return hardcoded analysis
        # In future, this could use more sophisticated NLP
        return {
            "role_title": "Software Engineer",
            "company": "TechCorp Inc.",
            "key_requirements": ["Python", "React", "AWS", "3+ years experience"],
            "company_culture": "Fast-paced startup environment",
            "industry": "Technology",
            "seniority_level": "Mid-level"
        }

def create_agents():
    """Create the CrewAI agents for the job application email system"""
    
    # Job Research Agent
    researcher = Agent(
        role='Job Research Specialist',
        goal='Analyze job descriptions and extract specific information to help a job candidate write a compelling application',
        backstory="""You are an expert at analyzing job descriptions and helping job candidates understand what companies are looking for. 
        You work for job seekers, not companies. Your job is to extract real, specific information from job postings 
        so candidates can write personalized application emails. You never use placeholder text - you extract actual information.
        You also have access to the candidate's CV data to help match their background with job requirements.""",
        verbose=True,
        allow_delegation=False,
        tools=[JobDescriptionAnalyzer()],
        llm=ollama_llm
    )
    
    # Email Writer Agent
    writer = Agent(
        role='Professional Email Writer for Job Seekers',
        goal='Write compelling job application emails from the candidate\'s perspective, using CV data for personalization',
        backstory="""You are a professional email writer who specializes in helping job candidates write application emails. 
        You ALWAYS write from the candidate's perspective - someone applying FOR a job, not someone offering a job. 
        You use real company names, real job titles, and real requirements from the research. 
        You never use placeholder text like [Company Name] or [Job Title].
        You write complete, professional emails with proper structure and compelling content.
        You have access to the candidate's CV data and use it to personalize the email with their actual experience, skills, and background.""",
        verbose=True,
        allow_delegation=False,
        tools=[],  # No tools needed - generate email content directly
        llm=ollama_llm
    )
    
    # Email Reviewer Agent
    reviewer = Agent(
        role='Email Quality Reviewer for Job Applications',
        goal='Ensure job application emails are written correctly from the candidate\'s perspective and contain no placeholder text',
        backstory="""You are an expert at reviewing job application emails. Your most important job is to ensure the email 
        is written from the CANDIDATE's perspective applying for a job, NOT from the company's perspective hiring someone. 
        You check that all placeholder text has been replaced with real information. If an email is fundamentally wrong, 
        you rewrite it completely. You ensure the tone is appropriate for someone applying for a position.
        You also verify that the email effectively uses the candidate's CV information for personalization.""",
        verbose=True,
        allow_delegation=False,
        llm=ollama_llm
    )
    
    return researcher, writer, reviewer

def create_tasks(researcher, writer, reviewer):
    """Create the tasks for the agents to execute"""
    
    # Task 1: Research the job and company
    research_task = Task(
        description="""You are a job research specialist. Analyze the provided job description and extract key information.
        
        Job Description: {job_description}
        
        CANDIDATE CV INFORMATION:
        {cv_summary}
        
        Your task is to:
        1. Extract the job title, company name, and key requirements
        2. Identify the company culture and industry
        3. Determine what skills and experience are most important
        4. Find key selling points that would make a candidate attractive
        5. Analyze how well the candidate's CV matches the job requirements
        6. Identify specific talking points based on the candidate's background
        
        Be specific and extract actual information from the job description, not placeholder text.
        Use the CV information to provide personalized insights.""",
        agent=researcher,
        expected_output="""A detailed analysis with specific information:
        - Job Title: [actual job title from description]
        - Company Name: [actual company name from description]
        - Key Requirements: [list of actual requirements]
        - Company Culture: [what you can infer about the company]
        - Industry: [what industry this company operates in]
        - Key Skills Needed: [most important technical and soft skills]
        - CV Match Analysis: [how well candidate's background fits]
        - Personalized Talking Points: [specific points based on candidate's CV]"""
    )
    
    # Task 2: Write the initial email
    writing_task = Task(
        description="""You are a professional email writer creating a job application email. 
        
        IMPORTANT: You are writing as a JOB CANDIDATE applying for a position, NOT as a company hiring someone.
        
        Use the research from the previous task to write a personalized job application email.
        
        CANDIDATE INFORMATION TO USE:
        {candidate_info}
        
        The email must:
        1. Be written from the perspective of someone applying for the job
        2. Include the actual company name and job title from the research
        3. Express genuine interest in the specific role and company
        4. Highlight relevant skills and experience from the candidate's CV
        5. Use the candidate's actual name, background, and achievements
        6. Be professional and compelling
        7. NOT contain placeholder text like [Company Name] or [Job Title]
        8. Include specific examples from the candidate's experience that match the job requirements
        
        Write a complete email with proper greeting, body, and closing. Use the actual information from the research task and the candidate's CV."""
        agent=writer,
        context=[research_task],
        expected_output="""A complete job application email that:
        - Has a clear subject line
        - Is written from the candidate's perspective
        - Uses actual company and job information
        - Shows genuine interest and enthusiasm
        - Highlights relevant skills and experience from the candidate's CV
        - Has a professional tone and structure
        - Contains NO placeholder text
        - Is personalized with the candidate's actual background"""
    )
    
    # Task 3: Review and improve the email
    review_task = Task(
        description="""You are an email quality reviewer. Review the drafted job application email.
        
        CRITICAL CHECK: Ensure this email is written from the CANDIDATE's perspective applying for a job, NOT from the company's perspective.
        
        CANDIDATE INFORMATION FOR VERIFICATION:
        {candidate_info}
        
        Your task is to:
        1. Verify the email is written as a job application (not a job posting)
        2. Check that all placeholder text has been replaced with actual information
        3. Ensure the tone is appropriate for a job application
        4. Verify that the email uses the candidate's actual CV information effectively
        5. Improve grammar, clarity, and professionalism
        6. Make sure the email makes sense and flows well
        7. Ensure personalization is effective and relevant
        
        If the email is fundamentally wrong (wrong perspective, major issues), rewrite it completely.
        If it's mostly correct, make improvements and corrections.
        Make sure the personalization from the CV data is natural and compelling."""
        agent=reviewer,
        context=[writing_task],
        expected_output="""A final, polished job application email that:
        - Is written from the candidate's perspective
        - Contains no placeholder text
        - Is professional and compelling
        - Has proper grammar and structure
        - Makes sense as a job application email
        - Effectively uses the candidate's CV information for personalization
        - Is tailored to the specific job and company"""
    )
    
    return research_task, writing_task, review_task

def main():
    """Main function to orchestrate the CrewAI workflow"""
    
    print("🚀 Starting Job Application Email Agent...")
    
    # Validate Ollama configuration
    if ollama_llm is None:
        print("❌ Failed to initialize Ollama LLM")
        print("Please check:")
        print("1. Ollama is running: ollama serve")
        print("2. Model is available: ollama list")
        print("3. Run: python check_env.py to check environment variables")
        return
    
    print("✅ Ollama LLM configured successfully")
    
    # Define the job description
    job_description = """
    Software Engineer - Full Stack
    TechCorp Inc.
    
    We are looking for a talented Full Stack Software Engineer to join our growing team.
    Requirements:
    - 3+ years of experience in software development
    - Proficiency in Python, JavaScript, and React
    - Experience with cloud platforms (AWS preferred)
    - Strong problem-solving skills
    - Team player with excellent communication skills
    
    We offer a fast-paced startup environment with opportunities for growth and learning.
    """
    
    print(f"📋 Job Description: {job_description[:100]}...")
    
    # Create agents
    try:
        researcher, writer, reviewer = create_agents()
        print("✅ Agents created successfully")
    except Exception as e:
        print(f"❌ Failed to create agents: {e}")
        print("This might be a CrewAI configuration issue")
        return
    
    # Create tasks with job description context
    try:
        research_task, writing_task, review_task = create_tasks(researcher, writer, reviewer)
        
        # Prepare CV information for tasks
        cv_summary = cv_parser.get_summary() if cv_data else "No CV data available"
        
        # Prepare candidate information for personalization
        if personalization_engine:
            candidate_info = personalization_engine.get_candidate_summary()
        else:
            candidate_info = "Generic candidate information"
        
        # Update the research task description with the actual job description and CV data
        research_task.description = research_task.description.format(
            job_description=job_description,
            cv_summary=cv_summary
        )
        
        # Update the writing task description with candidate information
        writing_task.description = writing_task.description.format(
            candidate_info=candidate_info
        )
        
        # Update the review task description with candidate information
        review_task.description = review_task.description.format(
            candidate_info=candidate_info
        )
        
        print("✅ Tasks created successfully")
        print(f"📋 CV Summary: {cv_summary}")
        print(f"👤 Candidate Info: {candidate_info}")
    except Exception as e:
        print(f"❌ Failed to create tasks: {e}")
        return
    
    # Create the crew
    try:
        crew = Crew(
            agents=[researcher, writer, reviewer],
            tasks=[research_task, writing_task, review_task],
            process=Process.sequential,
            verbose=True,
            llm=ollama_llm
        )
        print("✅ Crew created successfully")
    except Exception as e:
        print(f"❌ Failed to create crew: {e}")
        return
    
    # Execute the crew
    try:
        print("🔄 Starting CrewAI workflow...")
        print("\n📋 Step 1: Researching job description...")
        result = crew.kickoff()
        print("\n✅ Email generation completed!")
        print("\n📧 Final Email:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Check if Ollama is running: ollama serve")
        print("2. Verify model availability: ollama list")
        print("3. Check environment variables: python check_env.py")
        print("4. Test Ollama connection: python test_ollama_connection.py")
        print("\nIf the issue persists, the error details above should help identify the problem.")

if __name__ == "__main__":
    main()
