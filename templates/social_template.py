"""
Social Media Project Template
Social platform with user profiles, posts, and interactions.
"""

from typing import Dict, Any, List
from .base_template import BaseTemplate

class SocialProjectTemplate(BaseTemplate):
    """Social media application template."""
    
    def __init__(self, project_name: str, description: str = ""):
        super().__init__(project_name, description or f"A social platform for {project_name}")
    
    def get_features(self) -> List[str]:
        return [
            "user_profiles",
            "posts_sharing",
            "comments_likes",
            "follow_system",
            "real_time_notifications",
            "direct_messaging",
            "search_discovery",
            "content_moderation",
            "media_upload",
            "trending_topics"
        ]
    
    def get_pages(self) -> List[str]:
        return [
            "Home Feed",
            "Profile",
            "Post Details",
            "Explore",
            "Notifications",
            "Messages",
            "Settings",
            "Search Results"
        ]
    
    def get_integrations(self) -> List[str]:
        return [
            "cloudinary",
            "sendgrid",
            "google_analytics",
            "social_login",
            "push_notifications"
        ]
    
    def get_project_spec(self) -> Dict[str, Any]:
        return {
            "project_name": self.project_name,
            "description": self.description,
            "purpose": "social",
            "target_audience": "social_users",
            "design_style": "modern",
            "color_scheme": "purple",
            "mobile_first": True,
            "pages": self.get_pages(),
            "auth_required": True,
            "features": self.get_features(),
            "database_type": "postgresql",
            "deployment_preference": "vercel",
            "third_party_integrations": self.get_integrations(),
            "expected_users": "1000-100000",
            "performance_priority": "engagement",
            "seo_important": True,
            "analytics_required": True,
            "cms_needed": False,
            "multi_language": False,
            "custom_requirements": "Social platform with user profiles, posts, and interactions",
            "budget_tier": "medium",
            "technical_stack": self.get_technical_stack(),
            "database_schema": self.get_database_schema(),
            "api_routes": self.get_api_routes(),
            "environment_variables": self.get_environment_variables(),
            "dependencies": self.get_dependencies(),
            "scripts": self.get_scripts(),
            "file_structure": self.get_file_structure(),
            "quality_standards": self.get_quality_standards()
        } 