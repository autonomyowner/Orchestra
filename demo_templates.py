#!/usr/bin/env python3
"""
Template System Demo
Demonstrates the capabilities of the project templates system.
"""

import json
import os
from pathlib import Path

from template_manager import TemplateManager

def demo_template_listing():
    """Demo: List all available templates."""
    print("🎯 DEMO: Template Listing")
    print("=" * 50)
    
    manager = TemplateManager()
    templates = manager.list_templates()
    
    for key, info in templates.items():
        print(f"\n🔹 {info['name']} ({key})")
        print(f"   {info['description']}")
        print(f"   Features: {', '.join(info['features'][:3])}...")
        print(f"   Best for: {info['best_for']}")

def demo_template_info():
    """Demo: Get detailed template information."""
    print("\n\n📊 DEMO: Template Information")
    print("=" * 50)
    
    manager = TemplateManager()
    template = manager.get_template("saas", "Demo SaaS App", "A demonstration SaaS platform")
    
    if template:
        summary = manager.generate_template_summary(template)
        print(f"Template: {summary['template_type'].upper()}")
        print(f"Project: {summary['project_name']}")
        print(f"Complexity: {summary['complexity']}")
        print(f"Development Time: {summary['estimated_development_time']}")
        print(f"Features: {summary['total_features']}")
        print(f"Pages: {summary['total_pages']}")
        print(f"Integrations: {summary['total_integrations']}")
        print(f"Database Tables: {summary['database_tables']}")
        print(f"API Endpoints: {summary['api_endpoints']}")

def demo_template_comparison():
    """Demo: Compare two templates."""
    print("\n\n🔄 DEMO: Template Comparison")
    print("=" * 50)
    
    manager = TemplateManager()
    template1 = manager.get_template("saas", "SaaS App")
    template2 = manager.get_template("blog", "Blog App")
    
    if template1 and template2:
        comparison = manager.compare_templates(template1, template2)
        print(f"Comparing {comparison['template1']} vs {comparison['template2']}")
        
        for category, diff in comparison['differences'].items():
            print(f"\n{category.title()}:")
            print(f"  Only in {comparison['template1']}: {len(diff['only_in_template1'])}")
            print(f"  Only in {comparison['template2']}: {len(diff['only_in_template2'])}")
            print(f"  Common: {len(diff['common'])}")

def demo_template_export():
    """Demo: Export template specifications."""
    print("\n\n📁 DEMO: Template Export")
    print("=" * 50)
    
    manager = TemplateManager()
    
    # Create demo directory
    demo_dir = Path("demo_outputs")
    demo_dir.mkdir(exist_ok=True)
    
    templates_to_export = ["saas", "ecommerce", "blog"]
    
    for template_type in templates_to_export:
        template = manager.get_template(template_type, f"Demo {template_type.title()}")
        if template:
            output_path = demo_dir / f"{template_type}_spec.json"
            if manager.export_template_spec(template, str(output_path)):
                print(f"✅ Exported {template_type} template to {output_path}")
                
                # Show summary
                summary = manager.generate_template_summary(template)
                print(f"   📊 {summary['total_features']} features, {summary['total_pages']} pages")

def demo_template_recommendations():
    """Demo: Get template recommendations."""
    print("\n\n💡 DEMO: Template Recommendations")
    print("=" * 50)
    
    manager = TemplateManager()
    
    # Example requirements
    requirements_examples = [
        {
            "name": "Business SaaS",
            "requirements": {
                "purpose": "business",
                "billing_required": True,
                "user_interactions": False,
                "content_management": False
            }
        },
        {
            "name": "Content Platform",
            "requirements": {
                "purpose": "content",
                "billing_required": False,
                "user_interactions": True,
                "content_management": True
            }
        },
        {
            "name": "E-commerce Store",
            "requirements": {
                "purpose": "sales",
                "billing_required": True,
                "user_interactions": True,
                "content_management": False
            }
        }
    ]
    
    for example in requirements_examples:
        print(f"\n📋 {example['name']}:")
        recommendations = manager.get_recommendations(example['requirements'])
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                info = manager.template_descriptions.get(rec, {})
                print(f"  {i}. {info.get('name', rec)} ({rec})")
        else:
            print("  No specific recommendations found")

def demo_template_customization():
    """Demo: Template customization."""
    print("\n\n🔧 DEMO: Template Customization")
    print("=" * 50)
    
    manager = TemplateManager()
    
    # Create a customized template
    template = manager.create_custom_template(
        template_type="saas",
        project_name="Custom SaaS",
        description="A customized SaaS platform",
        customizations={
            "billing_provider": "paypal",
            "has_team_features": False
        }
    )
    
    if template:
        spec = manager.get_template_spec(template)
        print(f"✅ Created customized {template.template_type} template")
        print(f"Project: {spec['project_name']}")
        print(f"Description: {spec['description']}")
        print(f"Features: {len(spec['features'])}")
        print(f"Pages: {len(spec['pages'])}")

def demo_integration_workflow():
    """Demo: Complete integration workflow."""
    print("\n\n🚀 DEMO: Integration Workflow")
    print("=" * 50)
    
    manager = TemplateManager()
    
    # Simulate the workflow that happens in main.py
    print("1. User selects 'saas' template in wizard")
    
    template = manager.get_template("saas", "My SaaS App", "A modern SaaS platform")
    if template:
        print("2. Template instance created")
        
        # Get template specification
        template_spec = manager.get_template_spec(template)
        print("3. Template specification generated")
        
        # Simulate wizard data
        wizard_data = {
            "project_name": "My SaaS App",
            "description": "A modern SaaS platform",
            "template_type": "saas",
            "custom_color": "purple",
            "additional_features": ["custom_feature_1"]
        }
        
        # Merge template spec with wizard data
        merged_spec = {**template_spec, **wizard_data}
        print("4. Template spec merged with wizard data")
        
        # Show what was enhanced
        summary = manager.generate_template_summary(template)
        print(f"5. Enhanced specification includes:")
        print(f"   • {summary['total_features']} features")
        print(f"   • {summary['total_pages']} pages")
        print(f"   • {summary['total_integrations']} integrations")
        print(f"   • {summary['database_tables']} database tables")
        print(f"   • {summary['api_endpoints']} API endpoints")
        
        print("6. Ready for AI development pipeline!")

def main():
    """Run all demos."""
    print("🎯 AI Development Team Orchestrator - Template System Demo")
    print("=" * 60)
    print("This demo showcases the comprehensive template system capabilities.")
    print()
    
    try:
        demo_template_listing()
        demo_template_info()
        demo_template_comparison()
        demo_template_export()
        demo_template_recommendations()
        demo_template_customization()
        demo_integration_workflow()
        
        print("\n\n🎉 Demo completed successfully!")
        print("\n📁 Check the 'demo_outputs' directory for exported template specifications.")
        print("\n🚀 Ready to use templates in your projects!")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 