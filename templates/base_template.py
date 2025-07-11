"""
Base Template Class
Foundation for all project templates.
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod

class BaseTemplate(ABC):
    """Base class for all project templates."""
    
    def __init__(self, project_name: str, description: str = ""):
        self.project_name = project_name
        self.description = description
        self.template_type = self.__class__.__name__.replace("ProjectTemplate", "").lower()
    
    @abstractmethod
    def get_project_spec(self) -> Dict[str, Any]:
        """Return the complete project specification."""
        pass
    
    @abstractmethod
    def get_features(self) -> List[str]:
        """Return list of features for this template."""
        pass
    
    @abstractmethod
    def get_pages(self) -> List[str]:
        """Return list of pages for this template."""
        pass
    
    @abstractmethod
    def get_integrations(self) -> List[str]:
        """Return list of third-party integrations."""
        pass
    
    def get_technical_stack(self) -> Dict[str, str]:
        """Return the technical stack for this template."""
        return {
            "frontend": "Next.js 14 with TypeScript",
            "backend": "Next.js API Routes",
            "database": "PostgreSQL with Prisma",
            "authentication": "NextAuth.js",
            "styling": "Tailwind CSS",
            "deployment": "Vercel",
            "testing": "Jest + React Testing Library",
            "linting": "ESLint + Prettier"
        }
    
    def get_database_schema(self) -> List[Dict[str, Any]]:
        """Return database schema for this template."""
        return [
            {
                "name": "User",
                "fields": [
                    {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                    {"name": "email", "type": "string", "required": True, "description": "User email"},
                    {"name": "name", "type": "string", "required": False, "description": "User name"},
                    {"name": "image", "type": "string", "required": False, "description": "Profile image URL"},
                    {"name": "createdAt", "type": "datetime", "required": True, "description": "Account creation date"},
                    {"name": "updatedAt", "type": "datetime", "required": True, "description": "Last update date"}
                ],
                "relationships": []
            }
        ]
    
    def get_api_routes(self) -> List[Dict[str, Any]]:
        """Return API routes for this template."""
        return [
            {
                "method": "GET",
                "path": "/api/auth/session",
                "description": "Get current user session",
                "authentication_required": True
            },
            {
                "method": "POST",
                "path": "/api/auth/signin",
                "description": "User sign in",
                "authentication_required": False
            },
            {
                "method": "POST",
                "path": "/api/auth/signout",
                "description": "User sign out",
                "authentication_required": True
            }
        ]
    
    def get_environment_variables(self) -> List[Dict[str, str]]:
        """Return required environment variables."""
        return [
            {"name": "DATABASE_URL", "description": "PostgreSQL database connection string"},
            {"name": "NEXTAUTH_SECRET", "description": "Secret key for NextAuth.js"},
            {"name": "NEXTAUTH_URL", "description": "Base URL for NextAuth.js"},
            {"name": "NODE_ENV", "description": "Environment (development/production)"}
        ]
    
    def get_dependencies(self) -> Dict[str, List[str]]:
        """Return package dependencies."""
        return {
            "dependencies": [
                "next@14.0.0",
                "react@^18",
                "react-dom@^18",
                "typescript@^5",
                "@types/node@^20",
                "@types/react@^18",
                "@types/react-dom@^18",
                "tailwindcss@^3.3.0",
                "autoprefixer@^10.0.1",
                "postcss@^8",
                "@prisma/client@^5.0.0",
                "next-auth@^4.24.0",
                "bcryptjs@^2.4.3"
            ],
            "devDependencies": [
                "prisma@^5.0.0",
                "eslint@^8",
                "eslint-config-next@14.0.0",
                "@types/bcryptjs@^2.4.6",
                "jest@^29.0.0",
                "@testing-library/react@^13.0.0",
                "@testing-library/jest-dom@^5.16.0"
            ]
        }
    
    def get_scripts(self) -> Dict[str, str]:
        """Return npm scripts."""
        return {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "lint": "next lint",
            "type-check": "tsc --noEmit",
            "test": "jest",
            "test:watch": "jest --watch",
            "db:generate": "prisma generate",
            "db:push": "prisma db push",
            "db:studio": "prisma studio"
        }
    
    def get_file_structure(self) -> Dict[str, Any]:
        """Return the expected file structure."""
        return {
            "app/": {
                "layout.tsx": "Root layout component",
                "page.tsx": "Home page",
                "globals.css": "Global styles",
                "api/": "API routes",
                "auth/": "Authentication pages",
                "dashboard/": "Dashboard pages"
            },
            "components/": {
                "ui/": "Reusable UI components",
                "forms/": "Form components",
                "layout/": "Layout components"
            },
            "lib/": {
                "db.ts": "Database configuration",
                "auth.ts": "Authentication setup",
                "utils.ts": "Utility functions"
            },
            "prisma/": {
                "schema.prisma": "Database schema"
            },
            "docs/": {
                "API.md": "API documentation",
                "DEPLOYMENT.md": "Deployment guide",
                "USER_GUIDE.md": "User guide"
            }
        }
    
    def get_quality_standards(self) -> Dict[str, Any]:
        """Return quality standards for this template."""
        return {
            "typescript": "strict mode enabled",
            "eslint": "Next.js recommended rules",
            "accessibility": "WCAG AA compliance",
            "performance": "Lighthouse score 90+",
            "security": "OWASP compliance",
            "testing": "80%+ code coverage",
            "responsive": "Mobile-first design"
        }
    
    def customize(self, **kwargs) -> 'BaseTemplate':
        """Customize the template with user preferences."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
    
    def validate(self) -> List[str]:
        """Validate the template configuration."""
        errors = []
        
        if not self.project_name:
            errors.append("Project name is required")
        
        if not self.description:
            errors.append("Project description is required")
        
        if not self.get_features():
            errors.append("At least one feature is required")
        
        if not self.get_pages():
            errors.append("At least one page is required")
        
        return errors 