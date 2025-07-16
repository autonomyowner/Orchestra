"""
Portfolio Project Template
Professional portfolio for showcasing work and projects.
"""

from typing import Dict, Any, List
from .base_template import BaseTemplate

class PortfolioProjectTemplate(BaseTemplate):
    """Portfolio application template."""
    
    def __init__(self, project_name: str, description: str = ""):
        super().__init__(project_name, description or f"A professional portfolio for {project_name}")
    
    def get_features(self) -> List[str]:
        return [
            "project_showcase",
            "about_section",
            "contact_form",
            "resume_download",
            "blog_section",
            "testimonials",
            "skills_display",
            "social_links",
            "seo_optimization",
            "analytics_tracking"
        ]
    
    def get_pages(self) -> List[str]:
        return [
            "Home",
            "About",
            "Projects",
            "Project Details",
            "Blog",
            "Contact",
            "Resume"
        ]
    
    def get_integrations(self) -> List[str]:
        return [
            "sendgrid",
            "cloudinary",
            "google_analytics",
            "social_media_apis"
        ]
    
    def get_project_spec(self) -> Dict[str, Any]:
        return {
            "project_name": self.project_name,
            "description": self.description,
            "purpose": "portfolio",
            "target_audience": "potential_clients",
            "design_style": "minimal",
            "color_scheme": "neutral",
            "mobile_first": True,
            "pages": self.get_pages(),
            "auth_required": False,
            "features": self.get_features(),
            "database_type": "postgresql",
            "deployment_preference": "vercel",
            "third_party_integrations": self.get_integrations(),
            "expected_users": "100-1000",
            "performance_priority": "presentation",
            "seo_important": True,
            "analytics_required": True,
            "cms_needed": False,
            "multi_language": False,
            "custom_requirements": "Professional portfolio showcasing work and projects",
            "budget_tier": "low",
            "technical_stack": self.get_technical_stack(),
            "database_schema": self.get_database_schema(),
            "api_routes": self.get_api_routes(),
            "environment_variables": self.get_environment_variables(),
            "dependencies": self.get_dependencies(),
            "scripts": self.get_scripts(),
            "file_structure": self.get_file_structure(),
            "quality_standards": self.get_quality_standards()
        } 