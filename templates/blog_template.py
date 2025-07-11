"""
Blog Project Template
Complete blog application with content management and SEO.
"""

from typing import Dict, Any, List
from .base_template import BaseTemplate

class BlogProjectTemplate(BaseTemplate):
    """Blog application template with comprehensive features."""
    
    def __init__(self, project_name: str, description: str = ""):
        super().__init__(project_name, description or f"A modern blog platform for {project_name}")
        self.has_comments = True
        self.has_seo = True
        self.has_newsletter = True
    
    def get_features(self) -> List[str]:
        """Return blog-specific features."""
        return [
            "content_management",
            "blog_posts",
            "categories_tags",
            "comments_system",
            "user_authentication",
            "admin_dashboard",
            "seo_optimization",
            "newsletter_subscription",
            "search_functionality",
            "social_sharing",
            "rss_feeds",
            "analytics_tracking",
            "image_management",
            "draft_preview",
            "related_posts"
        ]
    
    def get_pages(self) -> List[str]:
        """Return blog-specific pages."""
        return [
            "Home",
            "Blog Posts",
            "Post Details",
            "Category",
            "Tag",
            "Author Profile",
            "About",
            "Contact",
            "Search Results",
            "Admin Dashboard",
            "Post Editor",
            "Comments Management",
            "Newsletter",
            "Privacy Policy",
            "Terms of Service"
        ]
    
    def get_integrations(self) -> List[str]:
        """Return blog-specific integrations."""
        return [
            "sendgrid",
            "cloudinary",
            "google_analytics",
            "disqus",
            "mailchimp",
            "social_media_apis"
        ]
    
    def get_database_schema(self) -> List[Dict[str, Any]]:
        """Return blog-specific database schema."""
        base_schema = super().get_database_schema()
        
        blog_schema = [
            {
                "name": "Post",
                "fields": [
                    {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                    {"name": "title", "type": "string", "required": True, "description": "Post title"},
                    {"name": "slug", "type": "string", "required": True, "description": "Post slug"},
                    {"name": "content", "type": "text", "required": True, "description": "Post content"},
                    {"name": "excerpt", "type": "text", "required": False, "description": "Post excerpt"},
                    {"name": "featuredImage", "type": "string", "required": False, "description": "Featured image URL"},
                    {"name": "authorId", "type": "string", "required": True, "description": "Author ID"},
                    {"name": "status", "type": "string", "required": True, "description": "Post status (draft/published)"},
                    {"name": "publishedAt", "type": "datetime", "required": False, "description": "Publication date"},
                    {"name": "metaTitle", "type": "string", "required": False, "description": "SEO meta title"},
                    {"name": "metaDescription", "type": "text", "required": False, "description": "SEO meta description"},
                    {"name": "viewCount", "type": "integer", "required": True, "description": "View count"},
                    {"name": "createdAt", "type": "datetime", "required": True, "description": "Creation date"},
                    {"name": "updatedAt", "type": "datetime", "required": True, "description": "Last update date"}
                ],
                "relationships": [
                    {"type": "manyToOne", "with": "User", "field": "authorId"},
                    {"type": "oneToMany", "with": "Comment", "field": "postId"},
                    {"type": "manyToMany", "with": "Category", "field": "postCategories"},
                    {"type": "manyToMany", "with": "Tag", "field": "postTags"}
                ]
            },
            {
                "name": "Category",
                "fields": [
                    {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                    {"name": "name", "type": "string", "required": True, "description": "Category name"},
                    {"name": "slug", "type": "string", "required": True, "description": "Category slug"},
                    {"name": "description", "type": "text", "required": False, "description": "Category description"},
                    {"name": "createdAt", "type": "datetime", "required": True, "description": "Creation date"},
                    {"name": "updatedAt", "type": "datetime", "required": True, "description": "Last update date"}
                ],
                "relationships": [{"type": "manyToMany", "with": "Post", "field": "categoryPosts"}]
            },
            {
                "name": "Tag",
                "fields": [
                    {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                    {"name": "name", "type": "string", "required": True, "description": "Tag name"},
                    {"name": "slug", "type": "string", "required": True, "description": "Tag slug"},
                    {"name": "createdAt", "type": "datetime", "required": True, "description": "Creation date"},
                    {"name": "updatedAt", "type": "datetime", "required": True, "description": "Last update date"}
                ],
                "relationships": [{"type": "manyToMany", "with": "Post", "field": "tagPosts"}]
            },
            {
                "name": "Comment",
                "fields": [
                    {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                    {"name": "postId", "type": "string", "required": True, "description": "Post ID"},
                    {"name": "authorId", "type": "string", "required": True, "description": "Author ID"},
                    {"name": "content", "type": "text", "required": True, "description": "Comment content"},
                    {"name": "parentId", "type": "string", "required": False, "description": "Parent comment ID"},
                    {"name": "status", "type": "string", "required": True, "description": "Comment status"},
                    {"name": "createdAt", "type": "datetime", "required": True, "description": "Creation date"},
                    {"name": "updatedAt", "type": "datetime", "required": True, "description": "Last update date"}
                ],
                "relationships": [
                    {"type": "manyToOne", "with": "Post", "field": "postId"},
                    {"type": "manyToOne", "with": "User", "field": "authorId"},
                    {"type": "manyToOne", "with": "Comment", "field": "parentId"}
                ]
            },
            {
                "name": "Newsletter",
                "fields": [
                    {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                    {"name": "email", "type": "string", "required": True, "description": "Subscriber email"},
                    {"name": "status", "type": "string", "required": True, "description": "Subscription status"},
                    {"name": "createdAt", "type": "datetime", "required": True, "description": "Subscription date"},
                    {"name": "updatedAt", "type": "datetime", "required": True, "description": "Last update date"}
                ],
                "relationships": []
            }
        ]
        
        return base_schema + blog_schema
    
    def get_api_routes(self) -> List[Dict[str, Any]]:
        """Return blog-specific API routes."""
        base_routes = super().get_api_routes()
        
        blog_routes = [
            # Post routes
            {"method": "GET", "path": "/api/posts", "description": "Get posts with pagination", "authentication_required": False},
            {"method": "GET", "path": "/api/posts/[slug]", "description": "Get post by slug", "authentication_required": False},
            {"method": "POST", "path": "/api/posts", "description": "Create post", "authentication_required": True},
            {"method": "PUT", "path": "/api/posts/[id]", "description": "Update post", "authentication_required": True},
            {"method": "DELETE", "path": "/api/posts/[id]", "description": "Delete post", "authentication_required": True},
            {"method": "POST", "path": "/api/posts/[id]/publish", "description": "Publish post", "authentication_required": True},
            
            # Category routes
            {"method": "GET", "path": "/api/categories", "description": "Get categories", "authentication_required": False},
            {"method": "GET", "path": "/api/categories/[slug]/posts", "description": "Get posts by category", "authentication_required": False},
            {"method": "POST", "path": "/api/categories", "description": "Create category", "authentication_required": True},
            
            # Tag routes
            {"method": "GET", "path": "/api/tags", "description": "Get tags", "authentication_required": False},
            {"method": "GET", "path": "/api/tags/[slug]/posts", "description": "Get posts by tag", "authentication_required": False},
            
            # Comment routes
            {"method": "GET", "path": "/api/posts/[id]/comments", "description": "Get post comments", "authentication_required": False},
            {"method": "POST", "path": "/api/posts/[id]/comments", "description": "Create comment", "authentication_required": True},
            {"method": "PUT", "path": "/api/comments/[id]", "description": "Update comment", "authentication_required": True},
            {"method": "DELETE", "path": "/api/comments/[id]", "description": "Delete comment", "authentication_required": True},
            
            # Newsletter routes
            {"method": "POST", "path": "/api/newsletter/subscribe", "description": "Subscribe to newsletter", "authentication_required": False},
            {"method": "POST", "path": "/api/newsletter/unsubscribe", "description": "Unsubscribe from newsletter", "authentication_required": False},
            
            # Search routes
            {"method": "GET", "path": "/api/search", "description": "Search posts", "authentication_required": False},
            
            # Admin routes
            {"method": "GET", "path": "/api/admin/posts", "description": "Get all posts (admin)", "authentication_required": True},
            {"method": "GET", "path": "/api/admin/comments", "description": "Get all comments (admin)", "authentication_required": True},
            {"method": "GET", "path": "/api/admin/analytics", "description": "Get blog analytics (admin)", "authentication_required": True}
        ]
        
        return base_routes + blog_routes
    
    def get_environment_variables(self) -> List[Dict[str, str]]:
        """Return blog-specific environment variables."""
        base_vars = super().get_environment_variables()
        
        blog_vars = [
            {"name": "SENDGRID_API_KEY", "description": "SendGrid API key for emails"},
            {"name": "SENDGRID_FROM_EMAIL", "description": "SendGrid from email address"},
            {"name": "CLOUDINARY_URL", "description": "Cloudinary URL for images"},
            {"name": "GOOGLE_ANALYTICS_ID", "description": "Google Analytics tracking ID"},
            {"name": "MAILCHIMP_API_KEY", "description": "Mailchimp API key for newsletter"},
            {"name": "MAILCHIMP_LIST_ID", "description": "Mailchimp list ID"},
            {"name": "DISQUS_SHORTNAME", "description": "Disqus shortname for comments"}
        ]
        
        return base_vars + blog_vars
    
    def get_dependencies(self) -> Dict[str, List[str]]:
        """Return blog-specific dependencies."""
        base_deps = super().get_dependencies()
        
        blog_deps = {
            "dependencies": base_deps["dependencies"] + [
                "sendgrid@^7.7.0",
                "cloudinary@^1.37.0",
                "react-markdown@^8.0.7",
                "react-syntax-highlighter@^15.5.0",
                "date-fns@^2.30.0",
                "react-share@^4.4.0",
                "react-hot-toast@^2.4.0",
                "zod@^3.22.0",
                "react-hook-form@^7.47.0"
            ],
            "devDependencies": base_deps["devDependencies"] + [
                "@types/react-syntax-highlighter@^15.5.7"
            ]
        }
        
        return blog_deps
    
    def get_project_spec(self) -> Dict[str, Any]:
        """Return complete blog project specification."""
        return {
            "project_name": self.project_name,
            "description": self.description,
            "purpose": "blog",
            "target_audience": "readers",
            "design_style": "clean",
            "color_scheme": "purple",
            "mobile_first": True,
            "pages": self.get_pages(),
            "auth_required": True,
            "auth_methods": "email",
            "features": self.get_features(),
            "database_type": "postgresql",
            "deployment_preference": "vercel",
            "third_party_integrations": self.get_integrations(),
            "expected_users": "100-10000",
            "performance_priority": "content",
            "seo_important": True,
            "analytics_required": True,
            "cms_needed": False,
            "multi_language": False,
            "custom_requirements": "Blog platform with content management, comments, and SEO optimization",
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