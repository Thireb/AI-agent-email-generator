#!/usr/bin/env python3
"""
CV Parser Tool for Job Application Email Agent
Extracts structured information from CV/Resume files to personalize job applications.
"""

import os
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
import PyPDF2
from datetime import datetime

class CVParser:
    """Parse CV/Resume files and extract structured information"""
    
    def __init__(self, cv_folder: str = "CV"):
        self.cv_folder = Path(cv_folder)
        self.cv_file = None
        self.cv_text = ""
        self.parsed_data = {}
    
    def find_cv_file(self) -> Optional[str]:
        """Find the first CV file in the CV folder"""
        if not self.cv_folder.exists():
            print(f"❌ CV folder '{self.cv_folder}' not found")
            return None
        
        # Look for common CV file extensions
        cv_extensions = ['.pdf', '.docx', '.doc', '.txt']
        
        for file_path in self.cv_folder.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in cv_extensions:
                print(f"✅ Found CV file: {file_path.name}")
                return str(file_path)
        
        print(f"❌ No CV files found in '{self.cv_folder}' folder")
        return None
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
            return ""
    
    def extract_personal_info(self) -> Dict[str, str]:
        """Extract personal information from CV text"""
        personal_info = {
            'name': '',
            'email': '',
            'phone': '',
            'location': '',
            'linkedin': ''
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, self.cv_text)
        if emails:
            personal_info['email'] = emails[0]
        
        # Extract phone number
        phone_pattern = r'(\+?[\d\s\-\(\)]{10,})'
        phones = re.findall(phone_pattern, self.cv_text)
        if phones:
            personal_info['phone'] = phones[0].strip()
        
        # Extract LinkedIn (common patterns)
        linkedin_pattern = r'(?:linkedin\.com/in/|LinkedIn:?\s*)([A-Za-z0-9\-_]+)'
        linkedin_matches = re.findall(linkedin_pattern, self.cv_text, re.IGNORECASE)
        if linkedin_matches:
            personal_info['linkedin'] = f"linkedin.com/in/{linkedin_matches[0]}"
        
        # Try to extract name from first few lines
        lines = self.cv_text.split('\n')[:10]
        for line in lines:
            line = line.strip()
            if line and len(line.split()) <= 4 and not any(char in line for char in '@()'):
                if not personal_info['name'] and line:
                    personal_info['name'] = line
                    break
        
        return personal_info
    
    def extract_experience(self) -> List[Dict[str, Any]]:
        """Extract work experience from CV text"""
        experience = []
        
        # Common experience section headers
        experience_headers = [
            r'EXPERIENCE', r'WORK EXPERIENCE', r'EMPLOYMENT HISTORY',
            r'PROFESSIONAL EXPERIENCE', r'CAREER HISTORY'
        ]
        
        # Look for experience section
        experience_text = ""
        for header in experience_headers:
            pattern = rf'{header}[:\s]*\n(.*?)(?=\n[A-Z\s]+\n|$)'
            match = re.search(pattern, self.cv_text, re.IGNORECASE | re.DOTALL)
            if match:
                experience_text = match.group(1)
                break
        
        if not experience_text:
            # Fallback: look for common job patterns
            experience_text = self.cv_text
        
        # Extract job entries (look for date patterns and company names)
        job_pattern = r'(\d{4}[-\s]*(?:present|now|current)?)[\s\-]*([^•\n]+?)(?:[\s\-]*([^•\n]+?))?(?=\d{4}|$)'
        jobs = re.findall(job_pattern, experience_text, re.IGNORECASE)
        
        for job in jobs:
            if len(job) >= 2:
                experience.append({
                    'period': job[0].strip(),
                    'title': job[1].strip() if len(job) > 1 else '',
                    'company': job[2].strip() if len(job) > 2 else '',
                    'description': ''
                })
        
        return experience
    
    def extract_skills(self) -> List[str]:
        """Extract skills from CV text"""
        skills = []
        
        # Common skills section headers
        skills_headers = [
            r'SKILLS', r'TECHNICAL SKILLS', r'COMPETENCIES',
            r'PROFICIENCIES', r'EXPERTISE'
        ]
        
        # Look for skills section
        skills_text = ""
        for header in skills_headers:
            pattern = rf'{header}[:\s]*\n(.*?)(?=\n[A-Z\s]+\n|$)'
            match = re.search(pattern, self.cv_text, re.IGNORECASE | re.DOTALL)
            if match:
                skills_text = match.group(1)
                break
        
        if skills_text:
            # Extract skills (look for comma-separated or bullet-pointed lists)
            skill_items = re.split(r'[,•\n]+', skills_text)
            for skill in skill_items:
                skill = skill.strip()
                if skill and len(skill) > 2 and len(skill) < 50:
                    skills.append(skill)
        
        # Fallback: look for common technical skills throughout the text
        if not skills:
            common_skills = [
                'Python', 'JavaScript', 'Java', 'C++', 'React', 'Angular', 'Vue',
                'Node.js', 'Django', 'Flask', 'AWS', 'Docker', 'Kubernetes',
                'SQL', 'MongoDB', 'Git', 'Linux', 'Agile', 'Scrum'
            ]
            
            for skill in common_skills:
                if re.search(rf'\b{skill}\b', self.cv_text, re.IGNORECASE):
                    skills.append(skill)
        
        return list(set(skills))  # Remove duplicates
    
    def extract_education(self) -> List[Dict[str, str]]:
        """Extract education information from CV text"""
        education = []
        
        # Common education section headers
        education_headers = [
            r'EDUCATION', r'ACADEMIC BACKGROUND', r'QUALIFICATIONS'
        ]
        
        # Look for education section
        education_text = ""
        for header in education_headers:
            pattern = rf'{header}[:\s]*\n(.*?)(?=\n[A-Z\s]+\n|$)'
            match = re.search(pattern, self.cv_text, re.IGNORECASE | re.DOTALL)
            if match:
                education_text = match.group(1)
                break
        
        if education_text:
            # Extract degree and institution
            lines = education_text.split('\n')
            for line in lines:
                line = line.strip()
                if line and len(line) > 10:
                    # Look for degree patterns
                    degree_pattern = r'(Bachelor|Master|PhD|BSc|MSc|MBA|Associate|Diploma)'
                    degree_match = re.search(degree_pattern, line, re.IGNORECASE)
                    
                    if degree_match:
                        education.append({
                            'degree': degree_match.group(1),
                            'institution': line.replace(degree_match.group(1), '').strip(' ,.-'),
                            'year': ''
                        })
        
        return education
    
    def parse_cv(self) -> Dict[str, Any]:
        """Main method to parse CV and extract all information"""
        # Find CV file
        cv_path = self.find_cv_file()
        if not cv_path:
            return {}
        
        self.cv_file = cv_path
        
        # Extract text
        if cv_path.lower().endswith('.pdf'):
            self.cv_text = self.extract_text_from_pdf(cv_path)
        else:
            # For other formats, we'll implement later
            print(f"⚠️  File format {Path(cv_path).suffix} not yet supported")
            return {}
        
        if not self.cv_text:
            print("❌ No text could be extracted from CV")
            return {}
        
        # Parse all sections
        self.parsed_data = {
            'personal_info': self.extract_personal_info(),
            'experience': self.extract_experience(),
            'skills': self.extract_skills(),
            'education': self.extract_education(),
            'raw_text': self.cv_text[:1000]  # First 1000 chars for debugging
        }
        
        print(f"✅ CV parsed successfully:")
        print(f"   - Personal Info: {len(self.parsed_data['personal_info'])} fields")
        print(f"   - Experience: {len(self.parsed_data['experience'])} entries")
        print(f"   - Skills: {len(self.parsed_data['skills'])} skills")
        print(f"   - Education: {len(self.parsed_data['education'])} entries")
        
        return self.parsed_data
    
    def get_summary(self) -> str:
        """Get a human-readable summary of the CV"""
        if not self.parsed_data:
            return "No CV data available"
        
        summary = []
        
        # Personal info
        if self.parsed_data.get('personal_info', {}).get('name'):
            summary.append(f"Name: {self.parsed_data['personal_info']['name']}")
        
        # Experience summary
        exp_count = len(self.parsed_data.get('experience', []))
        if exp_count > 0:
            summary.append(f"Experience: {exp_count} positions")
        
        # Skills summary
        skills_count = len(self.parsed_data.get('skills', []))
        if skills_count > 0:
            top_skills = self.parsed_data['skills'][:5]
            summary.append(f"Skills: {', '.join(top_skills)}")
        
        # Education summary
        edu_count = len(self.parsed_data.get('education', []))
        if edu_count > 0:
            summary.append(f"Education: {edu_count} degrees")
        
        return " | ".join(summary)

def main():
    """Test the CV parser"""
    parser = CVParser()
    data = parser.parse_cv()
    
    if data:
        print("\n📋 CV Summary:")
        print(parser.get_summary())
        
        print("\n🔍 Detailed Information:")
        for key, value in data.items():
            if key != 'raw_text':
                print(f"\n{key.upper()}:")
                print(value)

if __name__ == "__main__":
    main()
