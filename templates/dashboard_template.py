"""
Dashboard Project Template
Data dashboard with analytics and visualization.
"""

from typing import Dict, Any, List
from .base_template import BaseTemplate

class DashboardProjectTemplate(BaseTemplate):
    """Dashboard application template."""
    
    def __init__(self, project_name: str, description: str = ""):
        super().__init__(project_name, description or f"A data dashboard for {project_name}")
    
    def get_features(self) -> List[str]:
        return [
            "data_visualization",
            "real_time_analytics",
            "user_management",
            "role_based_access",
            "export_functionality",
            "custom_reports",
            "alerts_notifications",
            "data_import",
            "api_integration",
            "mobile_responsive"
        ]
    
    def get_pages(self) -> List[str]:
        return [
            "Dashboard",
            "Analytics",
            "Reports",
            "Users",
            "Settings",
            "Profile",
            "Admin"
        ]
    
    def get_integrations(self) -> List[str]:
        return [
            "google_analytics",
            "mixpanel",
            "amplitude",
            "segment",
            "slack",
            "email_services"
        ]
    
    def get_project_spec(self) -> Dict[str, Any]:
        return {
            "project_name": self.project_name,
            "description": self.description,
            "purpose": "dashboard",
            "target_audience": "business_users",
            "design_style": "professional",
            "color_scheme": "blue",
            "mobile_first": True,
            "pages": self.get_pages(),
            "auth_required": True,
            "features": self.get_features(),
            "database_type": "postgresql",
            "deployment_preference": "vercel",
            "third_party_integrations": self.get_integrations(),
            "expected_users": "100-5000",
            "performance_priority": "data",
            "seo_important": False,
            "analytics_required": True,
            "cms_needed": False,
            "multi_language": False,
            "custom_requirements": "Data dashboard with analytics and visualization",
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