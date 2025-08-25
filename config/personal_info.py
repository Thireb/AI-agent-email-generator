"""
Personal Information Configuration
This file contains personal information that will be used to customize email templates.
"""

# Personal Information - Customize these values
PERSONAL_INFO = {
    "your_name": "Your Name",
    "phone": "+1 (555) 123-4567",
    "email": "your.email@example.com",
    "linkedin": "linkedin.com/in/yourprofile",
    "github": "github.com/yourusername",
    "portfolio": "yourportfolio.com",
    
    # Professional Summary
    "professional_summary": "Experienced software engineer with a passion for building scalable solutions",
    
    # Key Skills (top 5-7 skills)
    "key_skills": [
        "Python",
        "JavaScript/React",
        "AWS/Cloud Computing",
        "Database Design",
        "API Development",
        "Agile Methodologies",
        "Problem Solving"
    ],
    
    # Relevant Experience
    "relevant_experience": "building scalable web applications and cloud-based solutions",
    
    # Years of Experience
    "years_experience": "5+ years",
    
    # Current Role
    "current_role": "Senior Software Engineer",
    
    # Education
    "education": "Bachelor's in Computer Science",
    
    # Certifications
    "certifications": [
        "AWS Certified Developer",
        "Google Cloud Professional Developer"
    ],
    
    # Notable Projects
    "notable_projects": [
        "Led development of microservices architecture serving 100K+ users",
        "Implemented CI/CD pipeline reducing deployment time by 60%",
        "Designed and built RESTful APIs for mobile applications"
    ],
    
    # Industry Focus
    "industry_focus": "technology and software development",
    
    # Career Goals
    "career_goals": "Continue growing as a technical leader while contributing to innovative projects"
}

# Email Preferences
EMAIL_PREFERENCES = {
    "tone": "professional yet enthusiastic",
    "length": "concise but comprehensive",
    "highlight_achievements": True,
    "show_company_research": True,
    "include_specific_examples": True
}

# Template Preferences
TEMPLATE_PREFERENCES = {
    "default_template": "software_engineer",  # software_engineer, data_scientist, general, etc.
    "include_contact_info": True,
    "include_portfolio_link": True,
    "customize_for_company": True
}

def get_personal_info():
    """Get the personal information dictionary"""
    return PERSONAL_INFO.copy()

def get_email_preferences():
    """Get the email preferences dictionary"""
    return EMAIL_PREFERENCES.copy()

def get_template_preferences():
    """Get the template preferences dictionary"""
    return TEMPLATE_PREFERENCES.copy()

def update_personal_info(key, value):
    """Update a specific personal information field"""
    if key in PERSONAL_INFO:
        PERSONAL_INFO[key] = value
        return True
    return False

def get_customization_data(job_analysis):
    """Get customization data combining personal info and job analysis"""
    personal = get_personal_info()
    
    # Merge personal info with job analysis
    customization_data = {
        **personal,
        **job_analysis,
        "key_skills": ", ".join(personal["key_skills"][:3]),  # Top 3 skills as string
        "relevant_experience": personal["relevant_experience"],
        "industry_focus": job_analysis.get("industry", personal["industry_focus"])
    }
    
    return customization_data

if __name__ == "__main__":
    # Test the configuration
    print("Personal Information:")
    print(f"Name: {PERSONAL_INFO['your_name']}")
    print(f"Skills: {', '.join(PERSONAL_INFO['key_skills'][:3])}")
    print(f"Experience: {PERSONAL_INFO['years_experience']}")
    
    print("\nEmail Preferences:")
    print(f"Tone: {EMAIL_PREFERENCES['tone']}")
    print(f"Length: {EMAIL_PREFERENCES['length']}")
    
    print("\nTemplate Preferences:")
    print(f"Default Template: {TEMPLATE_PREFERENCES['default_template']}")
    print(f"Customize for Company: {TEMPLATE_PREFERENCES['customize_for_company']}")
