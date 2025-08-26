#!/usr/bin/env python3
"""
LLM-Based CV Parser for Job Application Email Agent
Uses Ollama LLM to intelligently extract structured information from CV/Resume files.
"""

import os
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
import PyPDF2
from langchain_ollama import OllamaLLM

class LLMCVParser:
    """Parse CV/Resume files using LLM for intelligent information extraction"""
    
    def __init__(self, cv_folder: str = "CV"):
        self.cv_folder = Path(cv_folder)
        self.cv_file = None
        self.cv_text = ""
        self.parsed_data = {}
        
        # Initialize Ollama LLM for parsing
        self.llm = OllamaLLM(
            model="gemma3:1b",  # Remove ollama/ prefix
            base_url="http://localhost:11434"
        )
    
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
    
    def clean_cv_text(self, text: str) -> str:
        """Clean and format the extracted CV text"""
        # Remove excessive whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n', text)
        
        # Clean up common PDF extraction artifacts
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Fix concatenated words
        text = re.sub(r'([0-9])([A-Za-z])', r'\1 \2', text)  # Fix concatenated numbers and letters
        
        return text.strip()
    
    def extract_personal_info_with_llm(self, cv_text: str) -> Dict[str, str]:
        """Use LLM to extract personal information"""
        prompt = f"""
        Extract personal information from this CV text. Return ONLY a JSON object with these fields:
        - name: Full name of the person
        - email: Email address
        - phone: Phone number
        - location: City/Country if mentioned
        - linkedin: LinkedIn profile URL if mentioned
        - age: Age if mentioned
        
        CV Text:
        {cv_text[:2000]}
        
        Return only the JSON object, no other text:
        """
        
        try:
            response = self.llm.invoke(prompt)
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                import json
                return json.loads(json_match.group())
            else:
                return self._fallback_personal_info_extraction(cv_text)
        except Exception as e:
            print(f"⚠️  LLM extraction failed: {e}")
            return self._fallback_personal_info_extraction(cv_text)
    
    def _fallback_personal_info_extraction(self, cv_text: str) -> Dict[str, str]:
        """Fallback to regex-based extraction if LLM fails"""
        personal_info = {
            'name': '',
            'email': '',
            'phone': '',
            'location': '',
            'linkedin': '',
            'age': ''
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, cv_text)
        if emails:
            personal_info['email'] = emails[0]
        
        # Extract phone number
        phone_pattern = r'(\+?[\d\s\-\(\)]{10,})'
        phones = re.findall(phone_pattern, cv_text)
        if phones:
            personal_info['phone'] = phones[0].strip()
        
        # Extract LinkedIn
        linkedin_pattern = r'(?:linkedin\.com/in/|LinkedIn:?\s*)([A-Za-z0-9\-_]+)'
        linkedin_matches = re.findall(linkedin_pattern, cv_text, re.IGNORECASE)
        if linkedin_matches:
            personal_info['linkedin'] = f"linkedin.com/in/{linkedin_matches[0]}"
        
        return personal_info
    
    def extract_experience_with_llm(self, cv_text: str) -> List[Dict[str, Any]]:
        """Use LLM to extract work experience"""
        prompt = f"""
        Extract work experience from this CV text. Return ONLY a JSON array of experience objects.
        Each object should have:
        - title: Job title/role
        - company: Company name
        - period: Employment period (start - end dates)
        - description: Brief description of responsibilities and achievements
        
        CV Text:
        {cv_text[:3000]}
        
        Return only the JSON array, no other text:
        """
        
        try:
            response = self.llm.invoke(prompt)
            # Try to extract JSON array from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                import json
                return json.loads(json_match.group())
            else:
                return self._fallback_experience_extraction(cv_text)
        except Exception as e:
            print(f"⚠️  LLM extraction failed: {e}")
            return self._fallback_experience_extraction(cv_text)
    
    def _fallback_experience_extraction(self, cv_text: str) -> List[Dict[str, Any]]:
        """Fallback to regex-based extraction if LLM fails"""
        # This would be the old regex-based logic
        return []
    
    def extract_skills_with_llm(self, cv_text: str) -> List[str]:
        """Use LLM to extract skills"""
        prompt = f"""
        Extract technical skills and competencies from this CV text. 
        Return ONLY a JSON array of skill strings.
        
        Look for:
        - Programming languages
        - Frameworks and libraries
        - Tools and technologies
        - Soft skills and methodologies
        
        CV Text:
        {cv_text[:2000]}
        
        Return only the JSON array, no other text:
        """
        
        try:
            response = self.llm.invoke(prompt)
            # Try to extract JSON array from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                import json
                return json.loads(json_match.group())
            else:
                return self._fallback_skills_extraction(cv_text)
        except Exception as e:
            print(f"⚠️  LLM extraction failed: {e}")
            return self._fallback_skills_extraction(cv_text)
    
    def _fallback_skills_extraction(self, cv_text: str) -> List[str]:
        """Fallback to regex-based extraction if LLM fails"""
        # Common technical skills to look for
        common_skills = [
            'Python', 'JavaScript', 'Java', 'C++', 'React', 'Angular', 'Vue',
            'Node.js', 'Django', 'Flask', 'AWS', 'Docker', 'Kubernetes',
            'SQL', 'MongoDB', 'Git', 'Linux', 'Agile', 'Scrum', 'Machine Learning',
            'NLP', 'Web Scraping', 'Flutter', 'Redis', 'MySQL', 'Celery'
        ]
        
        found_skills = []
        for skill in common_skills:
            if re.search(rf'\b{skill}\b', cv_text, re.IGNORECASE):
                found_skills.append(skill)
        
        return found_skills
    
    def extract_education_with_llm(self, cv_text: str) -> List[Dict[str, str]]:
        """Use LLM to extract education information"""
        prompt = f"""
        Extract education information from this CV text. Return ONLY a JSON array of education objects.
        Each object should have:
        - degree: Degree type (Bachelor, Master, PhD, etc.)
        - institution: University/College name
        - period: Study period (start - end years)
        - gpa: GPA if mentioned
        
        CV Text:
        {cv_text[:2000]}
        
        Return only the JSON array, no other text:
        """
        
        try:
            response = self.llm.invoke(prompt)
            # Try to extract JSON array from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                import json
                return json.loads(json_match.group())
            else:
                return self._fallback_education_extraction(cv_text)
        except Exception as e:
            print(f"⚠️  LLM extraction failed: {e}")
            return self._fallback_education_extraction(cv_text)
    
    def _fallback_education_extraction(self, cv_text: str) -> List[Dict[str, str]]:
        """Fallback to regex-based extraction if LLM fails"""
        # This would be the old regex-based logic
        return []
    
    def extract_projects_with_llm(self, cv_text: str) -> List[Dict[str, Any]]:
        """Use LLM to extract project information"""
        prompt = f"""
        Extract project information from this CV text. Return ONLY a JSON array of project objects.
        Each object should have:
        - name: Project name
        - description: Brief description
        - period: Project period if mentioned
        - role: Role in the project
        - technologies: Technologies used
        
        CV Text:
        {cv_text[:3000]}
        
        Return only the JSON array, no other text:
        """
        
        try:
            response = self.llm.invoke(prompt)
            # Try to extract JSON array from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                import json
                return json.loads(json_match.group())
            else:
                return []
        except Exception as e:
            print(f"⚠️  LLM extraction failed: {e}")
            return []
    
    def parse_cv(self) -> Dict[str, Any]:
        """Main method to parse CV using LLM"""
        # Find CV file
        cv_path = self.find_cv_file()
        if not cv_path:
            return {}
        
        self.cv_file = cv_path
        
        # Extract text
        if cv_path.lower().endswith('.pdf'):
            self.cv_text = self.extract_text_from_pdf(cv_path)
        else:
            print(f"⚠️  File format {Path(cv_path).suffix} not yet supported")
            return {}
        
        if not self.cv_text:
            print("❌ No text could be extracted from CV")
            return {}
        
        # Clean the text
        self.cv_text = self.clean_cv_text(self.cv_text)
        
        print("🧠 Using LLM for intelligent CV parsing...")
        
        # Parse all sections using LLM
        self.parsed_data = {
            'personal_info': self.extract_personal_info_with_llm(self.cv_text),
            'experience': self.extract_experience_with_llm(self.cv_text),
            'skills': self.extract_skills_with_llm(self.cv_text),
            'education': self.extract_education_with_llm(self.cv_text),
            'projects': self.extract_projects_with_llm(self.cv_text),
            'raw_text': self.cv_text[:1000]  # First 1000 chars for debugging
        }
        
        print(f"✅ LLM CV parsing completed:")
        print(f"   - Personal Info: {len(self.parsed_data['personal_info'])} fields")
        print(f"   - Experience: {len(self.parsed_data['experience'])} entries")
        print(f"   - Skills: {len(self.parsed_data['skills'])} skills")
        print(f"   - Education: {len(self.parsed_data['education'])} entries")
        print(f"   - Projects: {len(self.parsed_data['projects'])} projects")
        
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
    """Test the LLM-based CV parser"""
    parser = LLMCVParser()
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
