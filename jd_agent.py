#!/usr/bin/env python3
"""
Job Application Email Agent using CrewAI
This agent helps write personalized job application emails using local Ollama models.
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

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

class EmailTemplateManager(BaseTool):
    """Tool for managing and customizing email templates"""
    
    name: str = "Email Template Manager"
    description: str = "Manages email templates and customizes them based on job requirements"
    
    def _run(self, template_type: str, customization_data: Dict[str, Any]) -> str:
        """Return customized email template"""
        base_templates = {
            "software_engineer": """
Dear {hiring_manager},

I am writing to express my strong interest in the {role_title} position at {company}. With my background in {key_skills} and experience in {relevant_experience}, I believe I would be an excellent fit for your team.

{company_specific_paragraph}

{experience_highlight_paragraph}

I am particularly excited about {company}'s work in {industry_focus} and would welcome the opportunity to contribute to your innovative projects.

Thank you for considering my application. I look forward to discussing how I can add value to your team.

Best regards,
{your_name}
            """,
            "data_scientist": """
Dear {hiring_manager},

I am excited to apply for the {role_title} position at {company}. My expertise in {key_skills} and passion for {industry_focus} align perfectly with your team's mission.

{company_specific_paragraph}

{experience_highlight_paragraph}

I am particularly drawn to {company}'s innovative approach to {industry_focus} and believe my analytical skills would be valuable to your data-driven initiatives.

Thank you for your time and consideration. I look forward to discussing this opportunity further.

Best regards,
{your_name}
            """
        }
        
        template = base_templates.get(template_type, base_templates["software_engineer"])
        return template.format(**customization_data)

def create_agents():
    """Create the CrewAI agents for the job application email system"""
    
    # Job Research Agent
    researcher = Agent(
        role='Job Research Specialist',
        goal='Analyze job descriptions and research companies to understand requirements and culture',
        backstory="""You are an expert at analyzing job descriptions and researching companies. 
        You can quickly identify key requirements, company culture, and industry trends.""",
        verbose=True,
        allow_delegation=False,
        tools=[JobDescriptionAnalyzer()]
    )
    
    # Email Writer Agent
    writer = Agent(
        role='Professional Email Writer',
        goal='Write compelling, personalized job application emails based on research',
        backstory="""You are a professional email writer with expertise in job applications. 
        You know how to craft emails that stand out and show genuine interest in the company.""",
        verbose=True,
        allow_delegation=False,
        tools=[EmailTemplateManager()]
    )
    
    # Email Reviewer Agent
    reviewer = Agent(
        role='Email Quality Reviewer',
        goal='Review and improve email drafts to ensure they are professional and compelling',
        backstory="""You are an expert at reviewing professional communications. 
        You can identify areas for improvement and suggest enhancements to make emails more effective.""",
        verbose=True,
        allow_delegation=False
    )
    
    return researcher, writer, reviewer

def create_tasks(researcher, writer, reviewer):
    """Create the tasks for the agents to execute"""
    
    # Task 1: Research the job and company
    research_task = Task(
        description="""Analyze the provided job description and research the company. 
        Extract key requirements, understand the company culture, and identify industry trends.
        Focus on what makes this role and company unique.""",
        agent=researcher,
        expected_output="""A comprehensive analysis including:
        - Role requirements and responsibilities
        - Company culture and values
        - Industry context and trends
        - Key selling points for the candidate"""
    )
    
    # Task 2: Write the initial email
    writing_task = Task(
        description="""Based on the research, write a personalized job application email. 
        The email should be professional, show genuine interest, and highlight relevant experience.
        Use appropriate email templates and customize them based on the research findings.""",
        agent=writer,
        context=[research_task],
        expected_output="""A complete, personalized job application email that includes:
        - Professional greeting and introduction
        - Clear expression of interest
        - Relevant experience highlights
        - Company-specific details
        - Professional closing"""
    )
    
    # Task 3: Review and improve the email
    review_task = Task(
        description="""Review the drafted email for quality, professionalism, and effectiveness.
        Suggest improvements to make it more compelling and professional.
        Ensure proper grammar, tone, and structure.""",
        agent=reviewer,
        context=[writing_task],
        expected_output="""An improved version of the email with:
        - Grammar and spelling corrections
        - Enhanced clarity and flow
        - Professional tone improvements
        - Specific suggestions for enhancement"""
    )
    
    return research_task, writing_task, review_task

def main():
    """Main function to orchestrate the CrewAI workflow"""
    
    print("🚀 Starting Job Application Email Agent...")
    
    # Create agents
    researcher, writer, reviewer = create_agents()
    
    # Create tasks
    research_task, writing_task, review_task = create_tasks(researcher, writer, reviewer)
    
    # Create the crew
    crew = Crew(
        agents=[researcher, writer, reviewer],
        tasks=[research_task, writing_task, review_task],
        process=Process.sequential,
        verbose=True
    )
    
    # For now, use hardcoded job description
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
    
    print(f"📋 Analyzing job description: {job_description[:100]}...")
    
    # Execute the crew
    try:
        result = crew.kickoff()
        print("\n✅ Email generation completed!")
        print("\n📧 Final Email:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        print("Please check your Ollama setup and try again.")

if __name__ == "__main__":
    main()
