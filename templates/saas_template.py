"""
SaaS Project Template
Complete SaaS application with billing, user management, and dashboard.
"""

from typing import Dict, Any, List
from .base_template import BaseTemplate

class SAASProjectTemplate(BaseTemplate):
    """SaaS application template with comprehensive features."""
    
    def __init__(self, project_name: str, description: str = ""):
        super().__init__(project_name, description or f"A modern SaaS platform for {project_name}")
        self.billing_provider = "stripe"
        self.has_team_features = True
        self.has_analytics = True
    
    def get_features(self) -> List[str]:
        """Return SaaS-specific features."""
        return [
            "user_management",
            "authentication",
            "billing_subscription",
            "team_management", 
            "dashboard_analytics",
            "api_integration",
            "admin_panel",
            "notifications",
            "file_upload",
            "search_functionality",
            "user_onboarding",
            "usage_tracking"
        ]
    
    def get_pages(self) -> List[str]:
        """Return SaaS-specific pages."""
        return [
            "Landing/Home",
            "Pricing",
            "Features",
            "About",
            "Contact",
            "Dashboard",
            "Profile",
            "Settings",
            "Billing",
            "Team",
            "Analytics",
            "Admin",
            "Onboarding",
            "Help/Support"
        ]
    
    def get_integrations(self) -> List[str]:
        """Return SaaS-specific integrations."""
        return [
            "stripe",
            "sendgrid",
            "google_analytics",
            "cloudinary",
            "auth0",
            "intercom",
            "mixpanel"
        ]
    
    def get_database_schema(self) -> List[Dict[str, Any]]:
        """Return SaaS-specific database schema."""
        base_schema = super().get_database_schema()
        
        saas_schema = [
            {
                "name": "Subscription",
                "fields": [
                    {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                    {"name": "userId", "type": "string", "required": True, "description": "User ID"},
                    {"name": "stripeCustomerId", "type": "string", "required": True, "description": "Stripe customer ID"},
                    {"name": "stripeSubscriptionId", "type": "string", "required": True, "description": "Stripe subscription ID"},
                    {"name": "plan", "type": "string", "required": True, "description": "Subscription plan"},
                    {"name": "status", "type": "string", "required": True, "description": "Subscription status"},
                    {"name": "currentPeriodStart", "type": "datetime", "required": True, "description": "Current period start"},
                    {"name": "currentPeriodEnd", "type": "datetime", "required": True, "description": "Current period end"},
                    {"name": "createdAt", "type": "datetime", "required": True, "description": "Creation date"},
                    {"name": "updatedAt", "type": "datetime", "required": True, "description": "Last update date"}
                ],
                "relationships": [{"type": "oneToOne", "with": "User", "field": "userId"}]
            },
            {
                "name": "Team",
                "fields": [
                    {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                    {"name": "name", "type": "string", "required": True, "description": "Team name"},
                    {"name": "ownerId", "type": "string", "required": True, "description": "Team owner ID"},
                    {"name": "slug", "type": "string", "required": True, "description": "Team slug"},
                    {"name": "createdAt", "type": "datetime", "required": True, "description": "Creation date"},
                    {"name": "updatedAt", "type": "datetime", "required": True, "description": "Last update date"}
                ],
                "relationships": [{"type": "oneToMany", "with": "TeamMember", "field": "teamId"}]
            },
            {
                "name": "TeamMember",
                "fields": [
                    {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                    {"name": "teamId", "type": "string", "required": True, "description": "Team ID"},
                    {"name": "userId", "type": "string", "required": True, "description": "User ID"},
                    {"name": "role", "type": "string", "required": True, "description": "Member role"},
                    {"name": "invitedAt", "type": "datetime", "required": True, "description": "Invitation date"},
                    {"name": "acceptedAt", "type": "datetime", "required": False, "description": "Acceptance date"}
                ],
                "relationships": [
                    {"type": "manyToOne", "with": "Team", "field": "teamId"},
                    {"type": "manyToOne", "with": "User", "field": "userId"}
                ]
            },
            {
                "name": "Usage",
                "fields": [
                    {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                    {"name": "userId", "type": "string", "required": True, "description": "User ID"},
                    {"name": "feature", "type": "string", "required": True, "description": "Feature name"},
                    {"name": "count", "type": "integer", "required": True, "description": "Usage count"},
                    {"name": "date", "type": "date", "required": True, "description": "Usage date"},
                    {"name": "createdAt", "type": "datetime", "required": True, "description": "Creation date"}
                ],
                "relationships": [{"type": "manyToOne", "with": "User", "field": "userId"}]
            }
        ]
        
        return base_schema + saas_schema
    
    def get_api_routes(self) -> List[Dict[str, Any]]:
        """Return SaaS-specific API routes."""
        base_routes = super().get_api_routes()
        
        saas_routes = [
            # Billing routes
            {"method": "POST", "path": "/api/billing/create-checkout", "description": "Create Stripe checkout session", "authentication_required": True},
            {"method": "POST", "path": "/api/billing/create-portal", "description": "Create Stripe customer portal", "authentication_required": True},
            {"method": "GET", "path": "/api/billing/subscription", "description": "Get user subscription", "authentication_required": True},
            {"method": "POST", "path": "/api/billing/webhook", "description": "Stripe webhook handler", "authentication_required": False},
            
            # Team routes
            {"method": "POST", "path": "/api/teams", "description": "Create new team", "authentication_required": True},
            {"method": "GET", "path": "/api/teams", "description": "Get user teams", "authentication_required": True},
            {"method": "GET", "path": "/api/teams/[id]", "description": "Get team details", "authentication_required": True},
            {"method": "PUT", "path": "/api/teams/[id]", "description": "Update team", "authentication_required": True},
            {"method": "DELETE", "path": "/api/teams/[id]", "description": "Delete team", "authentication_required": True},
            {"method": "POST", "path": "/api/teams/[id]/invite", "description": "Invite team member", "authentication_required": True},
            {"method": "POST", "path": "/api/teams/[id]/members/[userId]", "description": "Accept team invitation", "authentication_required": True},
            
            # Usage tracking
            {"method": "POST", "path": "/api/usage/track", "description": "Track feature usage", "authentication_required": True},
            {"method": "GET", "path": "/api/usage/summary", "description": "Get usage summary", "authentication_required": True},
            
            # Analytics
            {"method": "GET", "path": "/api/analytics/dashboard", "description": "Get dashboard analytics", "authentication_required": True},
            {"method": "GET", "path": "/api/analytics/users", "description": "Get user analytics", "authentication_required": True},
            
            # Admin routes
            {"method": "GET", "path": "/api/admin/users", "description": "Get all users (admin)", "authentication_required": True},
            {"method": "GET", "path": "/api/admin/subscriptions", "description": "Get all subscriptions (admin)", "authentication_required": True},
            {"method": "GET", "path": "/api/admin/analytics", "description": "Get admin analytics", "authentication_required": True}
        ]
        
        return base_routes + saas_routes
    
    def get_environment_variables(self) -> List[Dict[str, str]]:
        """Return SaaS-specific environment variables."""
        base_vars = super().get_environment_variables()
        
        saas_vars = [
            {"name": "STRIPE_SECRET_KEY", "description": "Stripe secret key"},
            {"name": "STRIPE_PUBLISHABLE_KEY", "description": "Stripe publishable key"},
            {"name": "STRIPE_WEBHOOK_SECRET", "description": "Stripe webhook secret"},
            {"name": "SENDGRID_API_KEY", "description": "SendGrid API key for emails"},
            {"name": "SENDGRID_FROM_EMAIL", "description": "SendGrid from email address"},
            {"name": "CLOUDINARY_URL", "description": "Cloudinary URL for file uploads"},
            {"name": "GOOGLE_ANALYTICS_ID", "description": "Google Analytics tracking ID"},
            {"name": "INTERCOM_APP_ID", "description": "Intercom app ID for support"},
            {"name": "MIXPANEL_TOKEN", "description": "Mixpanel token for analytics"}
        ]
        
        return base_vars + saas_vars
    
    def get_dependencies(self) -> Dict[str, List[str]]:
        """Return SaaS-specific dependencies."""
        base_deps = super().get_dependencies()
        
        saas_deps = {
            "dependencies": base_deps["dependencies"] + [
                "stripe@^12.0.0",
                "@stripe/stripe-js@^1.54.0",
                "sendgrid@^7.7.0",
                "cloudinary@^1.37.0",
                "mixpanel-browser@^2.45.0",
                "react-hot-toast@^2.4.0",
                "recharts@^2.7.0",
                "date-fns@^2.30.0",
                "zod@^3.22.0",
                "react-hook-form@^7.47.0"
            ],
            "devDependencies": base_deps["devDependencies"] + [
                "@types/stripe@^8.0.417"
            ]
        }
        
        return saas_deps
    
    def get_project_spec(self) -> Dict[str, Any]:
        """Return complete SaaS project specification."""
        return {
            "project_name": self.project_name,
            "description": self.description,
            "purpose": "saas",
            "target_audience": "businesses",
            "design_style": "modern",
            "color_scheme": "blue",
            "mobile_first": True,
            "pages": self.get_pages(),
            "auth_required": True,
            "auth_methods": "email",
            "features": self.get_features(),
            "database_type": "postgresql",
            "deployment_preference": "vercel",
            "third_party_integrations": self.get_integrations(),
            "expected_users": "1000-10000",
            "performance_priority": "user_experience",
            "seo_important": True,
            "analytics_required": True,
            "cms_needed": False,
            "multi_language": False,
            "custom_requirements": "SaaS platform with billing, team management, and analytics",
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