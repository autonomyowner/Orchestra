"""
Template Manager
Handles project template selection, customization, and integration.
"""

import json
import os
from typing import Dict, Any, List, Optional, Type
from pathlib import Path

from templates import (
    BaseTemplate,
    SAASProjectTemplate,
    EcommerceProjectTemplate,
    BlogProjectTemplate,
    PortfolioProjectTemplate,
    DashboardProjectTemplate,
    SocialProjectTemplate
)

class TemplateManager:
    """Manages project templates and their customization."""
    
    def __init__(self):
        self.templates: Dict[str, Type[BaseTemplate]] = {
            "saas": SAASProjectTemplate,
            "ecommerce": EcommerceProjectTemplate,
            "blog": BlogProjectTemplate,
            "portfolio": PortfolioProjectTemplate,
            "dashboard": DashboardProjectTemplate,
            "social": SocialProjectTemplate
        }
        
        self.template_descriptions = {
            "saas": {
                "name": "SaaS Platform",
                "description": "Complete SaaS application with billing, user management, and analytics",
                "features": ["Billing & Subscriptions", "Team Management", "Analytics Dashboard", "User Authentication"],
                "best_for": "Business applications, subscription services, team collaboration tools"
            },
            "ecommerce": {
                "name": "E-commerce Store",
                "description": "Full-featured online store with product management and payment processing",
                "features": ["Product Catalog", "Shopping Cart", "Payment Processing", "Order Management"],
                "best_for": "Online stores, marketplaces, product sales platforms"
            },
            "blog": {
                "name": "Blog Platform",
                "description": "Content management system with SEO optimization and social features",
                "features": ["Content Management", "SEO Optimization", "Comments System", "Newsletter"],
                "best_for": "Blogs, content websites, news sites, personal websites"
            },
            "portfolio": {
                "name": "Portfolio Website",
                "description": "Professional portfolio for showcasing work and projects",
                "features": ["Project Showcase", "About Section", "Contact Form", "Resume Download"],
                "best_for": "Freelancers, designers, developers, creative professionals"
            },
            "dashboard": {
                "name": "Data Dashboard",
                "description": "Analytics dashboard with data visualization and reporting",
                "features": ["Data Visualization", "Real-time Analytics", "Custom Reports", "User Management"],
                "best_for": "Business intelligence, analytics platforms, monitoring tools"
            },
            "social": {
                "name": "Social Platform",
                "description": "Social media platform with user profiles and interactions",
                "features": ["User Profiles", "Posts & Sharing", "Comments & Likes", "Real-time Notifications"],
                "best_for": "Social networks, community platforms, content sharing sites"
            }
        }
    
    def list_templates(self) -> Dict[str, Dict[str, Any]]:
        """List all available templates with descriptions."""
        return self.template_descriptions
    
    def get_template(self, template_type: str, project_name: str, description: str = "") -> Optional[BaseTemplate]:
        """Get a template instance by type."""
        if template_type not in self.templates:
            return None
        
        template_class = self.templates[template_type]
        return template_class(project_name, description)
    
    def create_custom_template(self, 
                             template_type: str,
                             project_name: str,
                             description: str = "",
                             customizations: Dict[str, Any] = None) -> Optional[BaseTemplate]:
        """Create a customized template instance."""
        template = self.get_template(template_type, project_name, description)
        if not template:
            return None
        
        if customizations:
            template = template.customize(**customizations)
        
        return template
    
    def get_template_spec(self, template: BaseTemplate) -> Dict[str, Any]:
        """Get the complete project specification from a template."""
        return template.get_project_spec()
    
    def validate_template(self, template: BaseTemplate) -> List[str]:
        """Validate a template configuration."""
        return template.validate()
    
    def export_template_spec(self, template: BaseTemplate, output_path: str) -> bool:
        """Export template specification to JSON file."""
        try:
            spec = self.get_template_spec(template)
            with open(output_path, 'w') as f:
                json.dump(spec, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error exporting template spec: {e}")
            return False
    
    def import_template_spec(self, spec_path: str) -> Optional[Dict[str, Any]]:
        """Import template specification from JSON file."""
        try:
            with open(spec_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error importing template spec: {e}")
            return None
    
    def compare_templates(self, template1: BaseTemplate, template2: BaseTemplate) -> Dict[str, Any]:
        """Compare two templates and show differences."""
        spec1 = self.get_template_spec(template1)
        spec2 = self.get_template_spec(template2)
        
        comparison = {
            "template1": template1.template_type,
            "template2": template2.template_type,
            "differences": {}
        }
        
        # Compare features
        features1 = set(template1.get_features())
        features2 = set(template2.get_features())
        comparison["differences"]["features"] = {
            "only_in_template1": list(features1 - features2),
            "only_in_template2": list(features2 - features1),
            "common": list(features1 & features2)
        }
        
        # Compare pages
        pages1 = set(template1.get_pages())
        pages2 = set(template2.get_pages())
        comparison["differences"]["pages"] = {
            "only_in_template1": list(pages1 - pages2),
            "only_in_template2": list(pages2 - pages1),
            "common": list(pages1 & pages2)
        }
        
        # Compare integrations
        integrations1 = set(template1.get_integrations())
        integrations2 = set(template2.get_integrations())
        comparison["differences"]["integrations"] = {
            "only_in_template1": list(integrations1 - integrations2),
            "only_in_template2": list(integrations2 - integrations1),
            "common": list(integrations1 & integrations2)
        }
        
        return comparison
    
    def generate_template_summary(self, template: BaseTemplate) -> Dict[str, Any]:
        """Generate a summary of template features and requirements."""
        spec = self.get_template_spec(template)
        
        return {
            "template_type": template.template_type,
            "project_name": template.project_name,
            "description": template.description,
            "purpose": spec.get("purpose", "unknown"),
            "target_audience": spec.get("target_audience", "general"),
            "complexity": self._assess_complexity(template),
            "estimated_development_time": self._estimate_development_time(template),
            "key_features": template.get_features()[:5],  # Top 5 features
            "total_features": len(template.get_features()),
            "total_pages": len(template.get_pages()),
            "total_integrations": len(template.get_integrations()),
            "database_tables": len(template.get_database_schema()),
            "api_endpoints": len(template.get_api_routes()),
            "environment_variables": len(template.get_environment_variables()),
            "dependencies": {
                "production": len(template.get_dependencies().get("dependencies", [])),
                "development": len(template.get_dependencies().get("devDependencies", []))
            }
        }
    
    def _assess_complexity(self, template: BaseTemplate) -> str:
        """Assess the complexity of a template."""
        feature_count = len(template.get_features())
        page_count = len(template.get_pages())
        integration_count = len(template.get_integrations())
        
        total_complexity = feature_count + page_count + integration_count
        
        if total_complexity < 20:
            return "Simple"
        elif total_complexity < 40:
            return "Medium"
        elif total_complexity < 60:
            return "Complex"
        else:
            return "Very Complex"
    
    def _estimate_development_time(self, template: BaseTemplate) -> str:
        """Estimate development time based on template complexity."""
        complexity = self._assess_complexity(template)
        
        estimates = {
            "Simple": "1-2 weeks",
            "Medium": "2-4 weeks", 
            "Complex": "4-8 weeks",
            "Very Complex": "8-12 weeks"
        }
        
        return estimates.get(complexity, "Unknown")
    
    def get_recommendations(self, requirements: Dict[str, Any]) -> List[str]:
        """Get template recommendations based on requirements."""
        recommendations = []
        
        # Analyze requirements and suggest templates
        if requirements.get("purpose") == "business" and requirements.get("billing_required"):
            recommendations.append("saas")
        
        if requirements.get("purpose") == "sales" or requirements.get("products_required"):
            recommendations.append("ecommerce")
        
        if requirements.get("purpose") == "content" or requirements.get("blog_required"):
            recommendations.append("blog")
        
        if requirements.get("purpose") == "showcase" or requirements.get("portfolio_required"):
            recommendations.append("portfolio")
        
        if requirements.get("purpose") == "analytics" or requirements.get("dashboard_required"):
            recommendations.append("dashboard")
        
        if requirements.get("purpose") == "social" or requirements.get("user_interactions"):
            recommendations.append("social")
        
        # Remove duplicates and return
        return list(set(recommendations))
    
    def create_template_from_requirements(self, requirements: Dict[str, Any]) -> Optional[BaseTemplate]:
        """Create a template based on user requirements."""
        recommendations = self.get_recommendations(requirements)
        
        if not recommendations:
            return None
        
        # Use the first recommendation
        template_type = recommendations[0]
        project_name = requirements.get("project_name", "My Project")
        description = requirements.get("description", "")
        
        template = self.get_template(template_type, project_name, description)
        
        # Apply customizations based on requirements
        customizations = {}
        
        if requirements.get("custom_features"):
            # Note: This would require more sophisticated template modification
            pass
        
        if requirements.get("custom_integrations"):
            # Note: This would require more sophisticated template modification
            pass
        
        return template.customize(**customizations) if customizations else template


def main():
    """CLI interface for template management."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Template Manager CLI")
    parser.add_argument("command", choices=["list", "info", "create", "export", "compare", "recommend"])
    parser.add_argument("--template", "-t", help="Template type")
    parser.add_argument("--name", "-n", help="Project name")
    parser.add_argument("--description", "-d", help="Project description")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--requirements", "-r", help="Requirements JSON file")
    
    args = parser.parse_args()
    
    manager = TemplateManager()
    
    if args.command == "list":
        templates = manager.list_templates()
        print("\n📋 Available Templates:")
        print("=" * 50)
        for key, info in templates.items():
            print(f"\n🔹 {info['name']} ({key})")
            print(f"   {info['description']}")
            print(f"   Features: {', '.join(info['features'][:3])}...")
            print(f"   Best for: {info['best_for']}")
    
    elif args.command == "info":
        if not args.template:
            print("❌ Template type required for info command")
            return
        
        template = manager.get_template(args.template, args.name or "Test Project")
        if template:
            summary = manager.generate_template_summary(template)
            print(f"\n📊 Template Summary: {summary['template_type'].upper()}")
            print("=" * 50)
            print(f"Project: {summary['project_name']}")
            print(f"Description: {summary['description']}")
            print(f"Complexity: {summary['complexity']}")
            print(f"Development Time: {summary['estimated_development_time']}")
            print(f"Features: {summary['total_features']}")
            print(f"Pages: {summary['total_pages']}")
            print(f"Integrations: {summary['total_integrations']}")
            print(f"Database Tables: {summary['database_tables']}")
            print(f"API Endpoints: {summary['api_endpoints']}")
        else:
            print(f"❌ Template '{args.template}' not found")
    
    elif args.command == "create":
        if not args.template or not args.name:
            print("❌ Template type and project name required for create command")
            return
        
        template = manager.get_template(args.template, args.name, args.description or "")
        if template:
            spec = manager.get_template_spec(template)
            print(f"\n✅ Created template: {template.template_type}")
            print(f"Project: {spec['project_name']}")
            print(f"Features: {len(spec['features'])}")
            print(f"Pages: {len(spec['pages'])}")
            
            if args.output:
                if manager.export_template_spec(template, args.output):
                    print(f"📁 Exported to: {args.output}")
                else:
                    print("❌ Failed to export template")
        else:
            print(f"❌ Template '{args.template}' not found")
    
    elif args.command == "export":
        if not args.template or not args.name or not args.output:
            print("❌ Template type, project name, and output path required for export command")
            return
        
        template = manager.get_template(args.template, args.name, args.description or "")
        if template:
            if manager.export_template_spec(template, args.output):
                print(f"✅ Exported template to: {args.output}")
            else:
                print("❌ Failed to export template")
        else:
            print(f"❌ Template '{args.template}' not found")
    
    elif args.command == "compare":
        if not args.template or not args.name:
            print("❌ Template type and project name required for compare command")
            return
        
        # Compare with a default template
        template1 = manager.get_template(args.template, args.name, args.description or "")
        template2 = manager.get_template("blog", "Comparison Project")
        
        if template1 and template2:
            comparison = manager.compare_templates(template1, template2)
            print(f"\n🔄 Template Comparison")
            print("=" * 50)
            print(f"Template 1: {comparison['template1']}")
            print(f"Template 2: {comparison['template2']}")
            
            for category, diff in comparison['differences'].items():
                print(f"\n{category.title()}:")
                print(f"  Only in {comparison['template1']}: {len(diff['only_in_template1'])}")
                print(f"  Only in {comparison['template2']}: {len(diff['only_in_template2'])}")
                print(f"  Common: {len(diff['common'])}")
        else:
            print("❌ Failed to create templates for comparison")
    
    elif args.command == "recommend":
        if not args.requirements:
            print("❌ Requirements file required for recommend command")
            return
        
        try:
            with open(args.requirements, 'r') as f:
                requirements = json.load(f)
            
            recommendations = manager.get_recommendations(requirements)
            print(f"\n💡 Template Recommendations:")
            print("=" * 50)
            
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    info = manager.template_descriptions.get(rec, {})
                    print(f"{i}. {info.get('name', rec)} ({rec})")
                    print(f"   {info.get('description', 'No description')}")
            else:
                print("No specific recommendations found. Consider using a custom template.")
        except Exception as e:
            print(f"❌ Error reading requirements file: {e}")


if __name__ == "__main__":
    main() 