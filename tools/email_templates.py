"""
Email Template Manager Tool
This tool manages email templates and customizes them based on job requirements.
"""

from crewai.tools import BaseTool
from typing import Dict, Any, List
import re

class EmailTemplateManager(BaseTool):
    """Tool for managing and customizing email templates"""
    
    name: str = "Email Template Manager"
    description: str = "Manages email templates and customizes them based on job requirements"
    
    def _run(self, template_type: str, customization_data: Dict[str, Any]) -> str:
        """
        Return customized email template based on template type and customization data
        
        Args:
            template_type (str): Type of email template to use
            customization_data (Dict[str, Any]): Data to customize the template with
            
        Returns:
            str: Customized email template
        """
        try:
            # Get the base template
            base_template = self._get_base_template(template_type)
            
            # Customize the template
            customized_email = self._customize_template(base_template, customization_data)
            
            return customized_email
            
        except Exception as e:
            print(f"Error managing email template: {e}")
            # Return a basic template as fallback
            return self._get_fallback_template(customization_data)
    
    def _get_base_template(self, template_type: str) -> str:
        """Get the base template for the specified type"""
        templates = {
            "software_engineer": self._get_software_engineer_template(),
            "data_scientist": self._get_data_scientist_template(),
            "product_manager": self._get_product_manager_template(),
            "designer": self._get_designer_template(),
            "marketing": self._get_marketing_template(),
            "sales": self._get_sales_template(),
            "general": self._get_general_template()
        }
        
        return templates.get(template_type, templates["general"])
    
    def _get_software_engineer_template(self) -> str:
        """Software engineer specific template"""
        return """
Dear {hiring_manager},

I am writing to express my strong interest in the {role_title} position at {company}. With my background in {key_skills} and experience in {relevant_experience}, I believe I would be an excellent fit for your team.

{company_specific_paragraph}

{experience_highlight_paragraph}

I am particularly excited about {company}'s work in {industry_focus} and would welcome the opportunity to contribute to your innovative projects. The {company_culture} you offer aligns perfectly with my professional goals and working style.

{technical_highlight_paragraph}

Thank you for considering my application. I look forward to discussing how I can add value to your team and contribute to {company}'s continued success.

Best regards,
{your_name}

{contact_info}
        """
    
    def _get_data_scientist_template(self) -> str:
        """Data scientist specific template"""
        return """
Dear {hiring_manager},

I am excited to apply for the {role_title} position at {company}. My expertise in {key_skills} and passion for {industry_focus} align perfectly with your team's mission.

{company_specific_paragraph}

{experience_highlight_paragraph}

I am particularly drawn to {company}'s innovative approach to {industry_focus} and believe my analytical skills would be valuable to your data-driven initiatives. The {company_culture} you foster is exactly the environment where I thrive.

{data_science_highlight_paragraph}

Thank you for your time and consideration. I look forward to discussing this opportunity further and learning more about how I can contribute to {company}'s data strategy.

Best regards,
{your_name}

{contact_info}
        """
    
    def _get_product_manager_template(self) -> str:
        """Product manager specific template"""
        return """
Dear {hiring_manager},

I am writing to express my interest in the {role_title} position at {company}. My experience in {key_skills} and passion for {industry_focus} make me an ideal candidate for this role.

{company_specific_paragraph}

{experience_highlight_paragraph}

I am particularly excited about {company}'s mission in {industry_focus} and believe my product strategy skills would be valuable to your team. The {company_culture} you offer is exactly what I'm looking for in my next role.

{product_management_highlight_paragraph}

Thank you for considering my application. I look forward to discussing how I can help {company} deliver exceptional products and experiences.

Best regards,
{your_name}

{contact_info}
        """
    
    def _get_designer_template(self) -> str:
        """Designer specific template"""
        return """
Dear {hiring_manager},

I am thrilled to apply for the {role_title} position at {company}. My creative background in {key_skills} and passion for {industry_focus} make me an ideal fit for your design team.

{company_specific_paragraph}

{experience_highlight_paragraph}

I am particularly drawn to {company}'s innovative work in {industry_focus} and believe my design thinking would enhance your user experience. The {company_culture} you foster is exactly where I want to grow as a designer.

{design_highlight_paragraph}

Thank you for considering my application. I look forward to discussing how I can contribute to {company}'s design excellence.

Best regards,
{your_name}

{contact_info}
        """
    
    def _get_marketing_template(self) -> str:
        """Marketing specific template"""
        return """
Dear {hiring_manager},

I am writing to express my interest in the {role_title} position at {company}. My expertise in {key_skills} and passion for {industry_focus} align perfectly with your marketing goals.

{company_specific_paragraph}

{experience_highlight_paragraph}

I am particularly excited about {company}'s innovative approach to {industry_focus} and believe my marketing skills would drive growth for your team. The {company_culture} you offer is exactly what I'm seeking.

{marketing_highlight_paragraph}

Thank you for considering my application. I look forward to discussing how I can help {company} achieve its marketing objectives.

Best regards,
{your_name}

{contact_info}
        """
    
    def _get_sales_template(self) -> str:
        """Sales specific template"""
        return """
Dear {hiring_manager},

I am excited to apply for the {role_title} position at {company}. My proven track record in {key_skills} and passion for {industry_focus} make me an ideal candidate for your sales team.

{company_specific_paragraph}

{experience_highlight_paragraph}

I am particularly drawn to {company}'s innovative solutions in {industry_focus} and believe my sales expertise would drive revenue growth. The {company_culture} you offer is exactly where I want to excel.

{sales_highlight_paragraph}

Thank you for considering my application. I look forward to discussing how I can contribute to {company}'s sales success.

Best regards,
{your_name}

{contact_info}
        """
    
    def _get_general_template(self) -> str:
        """General template for any role"""
        return """
Dear {hiring_manager},

I am writing to express my interest in the {role_title} position at {company}. With my background in {key_skills} and experience in {relevant_experience}, I believe I would be an excellent fit for your team.

{company_specific_paragraph}

{experience_highlight_paragraph}

I am particularly excited about {company}'s work in {industry_focus} and would welcome the opportunity to contribute to your organization's success. The {company_culture} you offer aligns perfectly with my professional goals.

{general_highlight_paragraph}

Thank you for considering my application. I look forward to discussing how I can add value to your team.

Best regards,
{your_name}

{contact_info}
        """
    
    def _customize_template(self, template: str, data: Dict[str, Any]) -> str:
        """Customize the template with the provided data"""
        try:
            # Ensure all required fields have values
            default_values = {
                "hiring_manager": "Hiring Manager",
                "role_title": "Software Engineer",
                "company": "TechCorp Inc.",
                "key_skills": "software development and problem-solving",
                "relevant_experience": "building scalable applications",
                "company_specific_paragraph": self._generate_company_paragraph(data),
                "experience_highlight_paragraph": self._generate_experience_paragraph(data),
                "industry_focus": data.get("industry", "technology"),
                "company_culture": data.get("company_culture", "innovative and collaborative"),
                "technical_highlight_paragraph": self._generate_technical_paragraph(data),
                "data_science_highlight_paragraph": self._generate_data_science_paragraph(data),
                "product_management_highlight_paragraph": self._generate_product_management_paragraph(data),
                "design_highlight_paragraph": self._generate_design_paragraph(data),
                "marketing_highlight_paragraph": self._generate_marketing_paragraph(data),
                "sales_highlight_paragraph": self._generate_sales_paragraph(data),
                "general_highlight_paragraph": self._generate_general_highlight_paragraph(data),
                "your_name": data.get("your_name", "Your Name"),
                "contact_info": self._generate_contact_info(data)
            }
            
            # Update with provided data
            default_values.update(data)
            
            # Fill the template
            customized = template
            for key, value in default_values.items():
                placeholder = "{" + key + "}"
                customized = customized.replace(placeholder, str(value))
            
            return customized
            
        except Exception as e:
            print(f"Error customizing template: {e}")
            return template
    
    def _generate_company_paragraph(self, data: Dict[str, Any]) -> str:
        """Generate company-specific paragraph"""
        company = data.get("company", "TechCorp Inc.")
        industry = data.get("industry", "technology")
        
        return f"I have been following {company}'s impressive growth in the {industry} sector and am particularly impressed by your innovative approach to solving complex challenges."
    
    def _generate_experience_paragraph(self, data: Dict[str, Any]) -> str:
        """Generate experience highlight paragraph"""
        key_skills = data.get("key_requirements", ["Python", "Problem-solving"])
        skills_text = ", ".join(key_skills[:3])  # Use top 3 skills
        
        return f"In my previous roles, I have successfully utilized {skills_text} to deliver high-quality solutions that drive business value. I am confident that my technical expertise and problem-solving abilities would be valuable to your team."
    
    def _generate_technical_paragraph(self, data: Dict[str, Any]) -> str:
        """Generate technical highlight paragraph"""
        key_skills = data.get("key_requirements", ["Python", "Problem-solving"])
        skills_text = ", ".join(key_skills[:3])
        
        return f"My technical background includes deep expertise in {skills_text}, and I am always eager to learn new technologies and methodologies. I believe in writing clean, maintainable code and collaborating effectively with cross-functional teams."
    
    def _generate_data_science_paragraph(self, data: Dict[str, Any]) -> str:
        """Generate data science highlight paragraph"""
        return "I have a proven track record of turning complex data into actionable insights and building machine learning models that drive business decisions. I am passionate about using data to solve real-world problems."
    
    def _generate_product_management_paragraph(self, data: Dict[str, Any]) -> str:
        """Generate product management highlight paragraph"""
        return "I have successfully led product development from ideation to launch, working closely with engineering, design, and business teams to deliver products that users love and that drive business growth."
    
    def _generate_design_paragraph(self, data: Dict[str, Any]) -> str:
        """Generate design highlight paragraph"""
        return "I have a strong foundation in user-centered design principles and have created intuitive, beautiful interfaces that enhance user experience and drive engagement. I believe in the power of design to solve complex problems."
    
    def _generate_marketing_paragraph(self, data: Dict[str, Any]) -> str:
        """Generate marketing highlight paragraph"""
        return "I have successfully developed and executed marketing strategies that drive brand awareness, lead generation, and revenue growth. I am data-driven and always optimize campaigns based on performance metrics."
    
    def _generate_sales_paragraph(self, data: Dict[str, Any]) -> str:
        """Generate sales highlight paragraph"""
        return "I have consistently exceeded sales targets and built strong relationships with clients. I am skilled at understanding customer needs and positioning solutions that provide real value."
    
    def _generate_general_highlight_paragraph(self, data: Dict[str, Any]) -> str:
        """Generate general highlight paragraph"""
        return "I am a results-oriented professional who thrives in dynamic environments. I am passionate about continuous learning and always strive to deliver exceptional results."
    
    def _generate_contact_info(self, data: Dict[str, Any]) -> str:
        """Generate contact information"""
        return """
Phone: {phone}
Email: {email}
LinkedIn: {linkedin}
        """.format(
            phone=data.get("phone", "Your Phone"),
            email=data.get("email", "your.email@example.com"),
            linkedin=data.get("linkedin", "linkedin.com/in/yourprofile")
        )
    
    def _get_fallback_template(self, data: Dict[str, Any]) -> str:
        """Get a fallback template if customization fails"""
        return f"""
Dear Hiring Manager,

I am writing to express my interest in the position at {data.get('company', 'your company')}.

I believe my skills and experience would be valuable to your team.

Thank you for considering my application.

Best regards,
{data.get('your_name', 'Your Name')}
        """
