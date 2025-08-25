"""
Job Description Analyzer Tool
This tool analyzes job descriptions and extracts key information for email personalization.
"""

from crewai.tools import BaseTool
from typing import Dict, Any, List
import re

class JobDescriptionAnalyzer(BaseTool):
    """Tool for analyzing job descriptions and extracting key information"""
    
    name: str = "Job Description Analyzer"
    description: str = "Analyzes job descriptions to extract key requirements, company info, and role details"
    
    def _run(self, job_description: str) -> Dict[str, Any]:
        """
        Analyze the job description and return structured information
        
        Args:
            job_description (str): The job description text to analyze
            
        Returns:
            Dict[str, Any]: Structured analysis of the job description
        """
        try:
            # Extract basic information
            analysis = {
                "role_title": self._extract_role_title(job_description),
                "company": self._extract_company(job_description),
                "key_requirements": self._extract_requirements(job_description),
                "company_culture": self._extract_culture_hints(job_description),
                "industry": self._extract_industry(job_description),
                "seniority_level": self._extract_seniority(job_description),
                "location": self._extract_location(job_description),
                "salary_hints": self._extract_salary_hints(job_description),
                "benefits": self._extract_benefits(job_description)
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing job description: {e}")
            # Return default analysis
            return self._get_default_analysis()
    
    def _extract_role_title(self, text: str) -> str:
        """Extract the job title from the description"""
        # Look for common patterns
        patterns = [
            r'(?:Position|Role|Job|We are looking for|Seeking|Hiring)\s*:?\s*([A-Za-z\s&]+(?:Engineer|Developer|Manager|Analyst|Specialist|Coordinator))',
            r'([A-Za-z\s&]+(?:Engineer|Developer|Manager|Analyst|Specialist|Coordinator))\s*position',
            r'([A-Za-z\s&]+(?:Engineer|Developer|Manager|Analyst|Specialist|Coordinator))'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Software Engineer"  # Default
    
    def _extract_company(self, text: str) -> str:
        """Extract company name from the description"""
        # Look for company indicators
        patterns = [
            r'(?:at|with|join)\s+([A-Z][a-zA-Z\s&]+(?:Inc|Corp|LLC|Ltd|Company|Technologies|Solutions))',
            r'([A-Z][a-zA-Z\s&]+(?:Inc|Corp|LLC|Ltd|Company|Technologies|Solutions))',
            r'(?:Company|Organization):\s*([A-Z][a-zA-Z\s&]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "TechCorp Inc."  # Default
    
    def _extract_requirements(self, text: str) -> List[str]:
        """Extract key requirements and skills"""
        requirements = []
        
        # Look for technical skills
        tech_skills = [
            "Python", "JavaScript", "Java", "C++", "C#", "React", "Angular", "Vue",
            "Node.js", "Django", "Flask", "AWS", "Azure", "GCP", "Docker", "Kubernetes",
            "SQL", "MongoDB", "PostgreSQL", "Git", "Linux", "Agile", "Scrum"
        ]
        
        for skill in tech_skills:
            if skill.lower() in text.lower():
                requirements.append(skill)
        
        # Look for experience requirements
        exp_patterns = [
            r'(\d+)\+?\s*years?\s*experience',
            r'experience\s*level:\s*([A-Za-z\s]+)',
            r'(\d+)\+?\s*years?\s*in\s*([A-Za-z\s]+)'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                requirements.append(f"{match.group(1)} years experience")
                break
        
        # Add some default requirements if none found
        if not requirements:
            requirements = ["Python", "Problem-solving", "Communication skills"]
        
        return requirements[:5]  # Limit to top 5
    
    def _extract_culture_hints(self, text: str) -> str:
        """Extract hints about company culture"""
        culture_keywords = {
            "fast-paced": "Fast-paced startup environment",
            "startup": "Fast-paced startup environment",
            "innovative": "Innovative and creative culture",
            "collaborative": "Collaborative team environment",
            "remote": "Remote-first culture",
            "flexible": "Flexible work environment",
            "growth": "Growth-oriented company",
            "learning": "Learning-focused organization"
        }
        
        text_lower = text.lower()
        for keyword, description in culture_keywords.items():
            if keyword in text_lower:
                return description
        
        return "Professional and collaborative environment"  # Default
    
    def _extract_industry(self, text: str) -> str:
        """Extract industry information"""
        industries = {
            "software": "Technology",
            "tech": "Technology",
            "ai": "Artificial Intelligence",
            "machine learning": "Machine Learning",
            "data": "Data Science",
            "finance": "Financial Services",
            "healthcare": "Healthcare",
            "ecommerce": "E-commerce",
            "education": "Education"
        }
        
        text_lower = text.lower()
        for keyword, industry in industries.items():
            if keyword in text_lower:
                return industry
        
        return "Technology"  # Default
    
    def _extract_seniority(self, text: str) -> str:
        """Extract seniority level"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["senior", "lead", "principal", "architect"]):
            return "Senior"
        elif any(word in text_lower for word in ["junior", "entry", "graduate", "intern"]):
            return "Junior"
        elif any(word in text_lower for word in ["mid", "intermediate", "3+", "5+"]):
            return "Mid-level"
        else:
            return "Mid-level"  # Default
    
    def _extract_location(self, text: str) -> str:
        """Extract location information"""
        # Look for location patterns
        patterns = [
            r'(?:in|at|based in)\s+([A-Z][a-zA-Z\s,]+(?:CA|NY|TX|FL|WA|Remote|Hybrid))',
            r'Location:\s*([A-Z][a-zA-Z\s,]+)',
            r'([A-Z][a-zA-Z\s,]+(?:CA|NY|TX|FL|WA|Remote|Hybrid))'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Remote/Hybrid"  # Default
    
    def _extract_salary_hints(self, text: str) -> str:
        """Extract salary information hints"""
        if any(word in text.lower() for word in ["competitive", "market rate", "attractive"]):
            return "Competitive salary"
        elif any(word in text.lower() for word in ["equity", "stock options", "ownership"]):
            return "Equity compensation included"
        else:
            return "Competitive compensation package"
    
    def _extract_benefits(self, text: str) -> List[str]:
        """Extract benefits information"""
        benefits = []
        text_lower = text.lower()
        
        benefit_keywords = {
            "health insurance": "Health insurance",
            "dental": "Dental coverage",
            "vision": "Vision coverage",
            "401k": "401(k) retirement plan",
            "flexible": "Flexible work arrangements",
            "remote": "Remote work options",
            "unlimited pto": "Unlimited PTO",
            "professional development": "Professional development",
            "learning": "Learning opportunities"
        }
        
        for keyword, benefit in benefit_keywords.items():
            if keyword in text_lower:
                benefits.append(benefit)
        
        if not benefits:
            benefits = ["Health insurance", "Professional development"]
        
        return benefits[:3]  # Limit to top 3
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Return default analysis when extraction fails"""
        return {
            "role_title": "Software Engineer",
            "company": "TechCorp Inc.",
            "key_requirements": ["Python", "Problem-solving", "Communication skills"],
            "company_culture": "Professional and collaborative environment",
            "industry": "Technology",
            "seniority_level": "Mid-level",
            "location": "Remote/Hybrid",
            "salary_hints": "Competitive compensation package",
            "benefits": ["Health insurance", "Professional development"]
        }
