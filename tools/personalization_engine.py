#!/usr/bin/env python3
"""
Personalization Engine for Job Application Email Agent
Uses CV information to personalize job applications based on job requirements.
"""

from typing import Dict, List, Any, Tuple
import re

class PersonalizationEngine:
    """Engine for personalizing job applications based on CV and job requirements"""
    
    def __init__(self, cv_data: Dict[str, Any]):
        self.cv_data = cv_data
        self.personal_info = cv_data.get('personal_info', {})
        self.experience = cv_data.get('experience', [])
        self.skills = cv_data.get('skills', [])
        self.education = cv_data.get('education', [])
    
    def analyze_skills_match(self, job_requirements: List[str]) -> Dict[str, Any]:
        """Analyze how well CV skills match job requirements"""
        if not job_requirements or not self.skills:
            return {'match_score': 0, 'matched_skills': [], 'missing_skills': []}
        
        # Normalize skills for comparison
        normalized_job_skills = [skill.lower().strip() for skill in job_requirements]
        normalized_cv_skills = [skill.lower().strip() for skill in self.skills]
        
        matched_skills = []
        missing_skills = []
        
        for job_skill in normalized_job_skills:
            # Check for exact matches and partial matches
            matched = False
            for cv_skill in normalized_cv_skills:
                if (job_skill in cv_skill or cv_skill in job_skill or 
                    self._calculate_similarity(job_skill, cv_skill) > 0.7):
                    matched_skills.append(job_skill)
                    matched = True
                    break
            
            if not matched:
                missing_skills.append(job_skill)
        
        # Calculate match score
        match_score = len(matched_skills) / len(normalized_job_skills) if normalized_job_skills else 0
        
        return {
            'match_score': match_score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'total_required': len(normalized_job_skills),
            'total_matched': len(matched_skills)
        }
    
    def _calculate_similarity(self, skill1: str, skill2: str) -> float:
        """Calculate similarity between two skills"""
        # Simple similarity calculation
        if skill1 == skill2:
            return 1.0
        
        # Check if one is contained in the other
        if skill1 in skill2 or skill2 in skill1:
            return 0.8
        
        # Check for common abbreviations
        if self._are_abbreviations(skill1, skill2):
            return 0.9
        
        return 0.0
    
    def _are_abbreviations(self, skill1: str, skill2: str) -> bool:
        """Check if skills are abbreviations of each other"""
        # Common abbreviation mappings
        abbreviations = {
            'javascript': ['js'],
            'python': ['py'],
            'react': ['reactjs'],
            'node.js': ['nodejs', 'node'],
            'aws': ['amazon web services'],
            'sql': ['mysql', 'postgresql', 'sqlite'],
            'git': ['github', 'gitlab']
        }
        
        skill1_lower = skill1.lower()
        skill2_lower = skill2.lower()
        
        for full, abbrevs in abbreviations.items():
            if skill1_lower == full and skill2_lower in abbrevs:
                return True
            if skill2_lower == full and skill1_lower in abbrevs:
                return True
        
        return False
    
    def find_relevant_experience(self, job_title: str, required_skills: List[str]) -> List[Dict[str, Any]]:
        """Find experience entries most relevant to the job"""
        if not self.experience:
            return []
        
        relevant_experience = []
        
        for exp in self.experience:
            relevance_score = 0
            
            # Check title relevance
            if job_title and exp.get('title'):
                title_similarity = self._calculate_title_similarity(job_title, exp['title'])
                relevance_score += title_similarity * 0.4
            
            # Check skills relevance
            if required_skills and exp.get('description'):
                skills_in_description = self._count_skills_in_text(required_skills, exp['description'])
                relevance_score += (skills_in_description / len(required_skills)) * 0.6
            
            if relevance_score > 0.1:  # Only include if somewhat relevant
                exp_copy = exp.copy()
                exp_copy['relevance_score'] = relevance_score
                relevant_experience.append(exp_copy)
        
        # Sort by relevance score
        relevant_experience.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        return relevant_experience[:3]  # Return top 3 most relevant
    
    def _calculate_title_similarity(self, job_title: str, exp_title: str) -> float:
        """Calculate similarity between job title and experience title"""
        job_words = set(job_title.lower().split())
        exp_words = set(exp_title.lower().split())
        
        if not job_words or not exp_words:
            return 0.0
        
        intersection = job_words.intersection(exp_words)
        union = job_words.union(exp_words)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _count_skills_in_text(self, skills: List[str], text: str) -> int:
        """Count how many skills appear in the given text"""
        if not text:
            return 0
        
        text_lower = text.lower()
        count = 0
        
        for skill in skills:
            if skill.lower() in text_lower:
                count += 1
        
        return count
    
    def generate_personalized_content(self, job_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized content for job application"""
        job_title = job_analysis.get('role_title', '')
        company_name = job_analysis.get('company', '')
        required_skills = job_analysis.get('key_requirements', [])
        
        # Analyze skills match
        skills_analysis = self.analyze_skills_match(required_skills)
        
        # Find relevant experience
        relevant_experience = self.find_relevant_experience(job_title, required_skills)
        
        # Generate personalized talking points
        talking_points = self._generate_talking_points(
            skills_analysis, relevant_experience, job_analysis
        )
        
        return {
            'skills_match': skills_analysis,
            'relevant_experience': relevant_experience,
            'talking_points': talking_points,
            'personal_info': self.personal_info,
            'strengths_to_highlight': self._identify_strengths(skills_analysis),
            'areas_to_emphasize': self._identify_emphasis_areas(job_analysis)
        }
    
    def _generate_talking_points(self, skills_analysis: Dict, 
                                relevant_experience: List[Dict], 
                                job_analysis: Dict) -> List[str]:
        """Generate personalized talking points for the application"""
        talking_points = []
        
        # Skills match talking points
        if skills_analysis['match_score'] > 0.5:
            matched_skills = skills_analysis['matched_skills']
            talking_points.append(
                f"I have strong experience in {', '.join(matched_skills[:3])} which directly align with your requirements."
            )
        
        # Experience talking points
        if relevant_experience:
            top_exp = relevant_experience[0]
            talking_points.append(
                f"In my role as {top_exp.get('title', 'Software Engineer')}, I gained valuable experience that would benefit your team."
            )
        
        # Company-specific talking points
        company_name = job_analysis.get('company', '')
        if company_name:
            talking_points.append(
                f"I'm excited about the opportunity to contribute to {company_name}'s innovative projects and growth."
            )
        
        # Industry enthusiasm
        industry = job_analysis.get('industry', 'technology')
        talking_points.append(
            f"I'm passionate about {industry} and always eager to learn new technologies and approaches."
        )
        
        return talking_points
    
    def _identify_strengths(self, skills_analysis: Dict) -> List[str]:
        """Identify key strengths to highlight"""
        strengths = []
        
        if skills_analysis['match_score'] > 0.7:
            strengths.append("Strong technical skills alignment")
        
        if skills_analysis['total_matched'] > 5:
            strengths.append("Extensive relevant experience")
        
        if len(self.experience) > 2:
            strengths.append("Proven track record")
        
        if self.education:
            strengths.append("Strong educational background")
        
        return strengths
    
    def _identify_emphasis_areas(self, job_analysis: Dict) -> List[str]:
        """Identify areas to emphasize based on job requirements"""
        emphasis_areas = []
        
        required_skills = job_analysis.get('key_requirements', [])
        if 'communication' in ' '.join(required_skills).lower():
            emphasis_areas.append("Communication and collaboration skills")
        
        if any(skill in ' '.join(required_skills).lower() for skill in ['leadership', 'management']):
            emphasis_areas.append("Leadership and project management experience")
        
        if any(skill in ' '.join(required_skills).lower() for skill in ['agile', 'scrum']):
            emphasis_areas.append("Agile methodology experience")
        
        return emphasis_areas
    
    def get_candidate_summary(self) -> str:
        """Get a summary of the candidate for the application"""
        summary_parts = []
        
        # Name and current role
        if self.personal_info.get('name'):
            summary_parts.append(f"I am {self.personal_info['name']}")
        
        # Experience summary
        if self.experience:
            exp_count = len(self.experience)
            summary_parts.append(f"a software engineer with {exp_count} years of experience")
        
        # Key skills
        if self.skills:
            top_skills = self.skills[:5]
            summary_parts.append(f"specializing in {', '.join(top_skills)}")
        
        # Education
        if self.education:
            degree = self.education[0].get('degree', 'degree')
            summary_parts.append(f"with a {degree}")
        
        return " ".join(summary_parts) + "."

def main():
    """Test the personalization engine"""
    # Sample CV data for testing
    sample_cv_data = {
        'personal_info': {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+1234567890'
        },
        'experience': [
            {
                'title': 'Software Engineer',
                'company': 'TechCorp',
                'period': '2020-2023',
                'description': 'Developed web applications using Python, React, and AWS'
            }
        ],
        'skills': ['Python', 'React', 'JavaScript', 'AWS', 'Docker'],
        'education': [
            {
                'degree': 'Bachelor of Science',
                'institution': 'University of Technology',
                'year': '2020'
            }
        ]
    }
    
    # Sample job analysis
    sample_job = {
        'role_title': 'Software Engineer',
        'company': 'Innovation Inc',
        'key_requirements': ['Python', 'React', 'AWS', 'communication skills'],
        'industry': 'technology'
    }
    
    engine = PersonalizationEngine(sample_cv_data)
    personalized_content = engine.generate_personalized_content(sample_job)
    
    print("🧪 Testing Personalization Engine")
    print("=" * 50)
    print(f"Skills Match Score: {personalized_content['skills_match']['match_score']:.2f}")
    print(f"Relevant Experience: {len(personalized_content['relevant_experience'])} entries")
    print(f"Talking Points: {len(personalized_content['talking_points'])} generated")
    print(f"Strengths: {', '.join(personalized_content['strengths_to_highlight'])}")
    
    print("\n📝 Sample Talking Points:")
    for i, point in enumerate(personalized_content['talking_points'], 1):
        print(f"{i}. {point}")

if __name__ == "__main__":
    main()
