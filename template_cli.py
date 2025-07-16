#!/usr/bin/env python3
"""
Template Manager CLI
Command-line interface for managing project templates.
"""

import argparse
import json
import sys
from pathlib import Path

from template_manager import TemplateManager

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Template Manager - Manage and customize project templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python template_cli.py list                    # List all templates
  python template_cli.py info --template saas    # Show template details
  python template_cli.py create --template blog --name my-blog  # Create template
  python template_cli.py export --template ecommerce --name my-store --output spec.json
  python template_cli.py compare --template1 saas --template2 blog
  python template_cli.py recommend --requirements req.json
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all available templates")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show detailed template information")
    info_parser.add_argument("--template", "-t", required=True, help="Template type")
    info_parser.add_argument("--name", "-n", default="Test Project", help="Project name")
    info_parser.add_argument("--description", "-d", default="", help="Project description")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a template instance")
    create_parser.add_argument("--template", "-t", required=True, help="Template type")
    create_parser.add_argument("--name", "-n", required=True, help="Project name")
    create_parser.add_argument("--description", "-d", default="", help="Project description")
    create_parser.add_argument("--output", "-o", help="Output JSON file path")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export template specification")
    export_parser.add_argument("--template", "-t", required=True, help="Template type")
    export_parser.add_argument("--name", "-n", required=True, help="Project name")
    export_parser.add_argument("--description", "-d", default="", help="Project description")
    export_parser.add_argument("--output", "-o", required=True, help="Output file path")
    
    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare two templates")
    compare_parser.add_argument("--template1", "-t1", required=True, help="First template type")
    compare_parser.add_argument("--template2", "-t2", required=True, help="Second template type")
    compare_parser.add_argument("--name1", "-n1", default="Project 1", help="First project name")
    compare_parser.add_argument("--name2", "-n2", default="Project 2", help="Second project name")
    
    # Recommend command
    recommend_parser = subparsers.add_parser("recommend", help="Get template recommendations")
    recommend_parser.add_argument("--requirements", "-r", required=True, help="Requirements JSON file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = TemplateManager()
    
    try:
        if args.command == "list":
            templates = manager.list_templates()
            print("\n📋 Available Templates:")
            print("=" * 60)
            for key, info in templates.items():
                print(f"\n🔹 {info['name']} ({key})")
                print(f"   {info['description']}")
                print(f"   Features: {', '.join(info['features'][:3])}...")
                print(f"   Best for: {info['best_for']}")
        
        elif args.command == "info":
            template = manager.get_template(args.template, args.name, args.description)
            if template:
                summary = manager.generate_template_summary(template)
                print(f"\n📊 Template Information: {summary['template_type'].upper()}")
                print("=" * 60)
                print(f"Project: {summary['project_name']}")
                print(f"Description: {summary['description']}")
                print(f"Purpose: {summary['purpose']}")
                print(f"Target Audience: {summary['target_audience']}")
                print(f"Complexity: {summary['complexity']}")
                print(f"Development Time: {summary['estimated_development_time']}")
                print(f"\n📈 Statistics:")
                print(f"  • Features: {summary['total_features']}")
                print(f"  • Pages: {summary['total_pages']}")
                print(f"  • Integrations: {summary['total_integrations']}")
                print(f"  • Database Tables: {summary['database_tables']}")
                print(f"  • API Endpoints: {summary['api_endpoints']}")
                print(f"  • Environment Variables: {summary['environment_variables']}")
                print(f"  • Dependencies: {summary['dependencies']['production']} prod, {summary['dependencies']['development']} dev")
                
                print(f"\n🎯 Key Features:")
                for feature in summary['key_features']:
                    print(f"  • {feature}")
            else:
                print(f"❌ Template '{args.template}' not found")
                sys.exit(1)
        
        elif args.command == "create":
            template = manager.get_template(args.template, args.name, args.description)
            if template:
                spec = manager.get_template_spec(template)
                print(f"\n✅ Created template: {template.template_type}")
                print(f"Project: {spec['project_name']}")
                print(f"Description: {spec['description']}")
                print(f"Features: {len(spec['features'])}")
                print(f"Pages: {len(spec['pages'])}")
                print(f"Integrations: {len(spec['third_party_integrations'])}")
                
                if args.output:
                    if manager.export_template_spec(template, args.output):
                        print(f"📁 Exported to: {args.output}")
                    else:
                        print("❌ Failed to export template")
                        sys.exit(1)
            else:
                print(f"❌ Template '{args.template}' not found")
                sys.exit(1)
        
        elif args.command == "export":
            template = manager.get_template(args.template, args.name, args.description)
            if template:
                if manager.export_template_spec(template, args.output):
                    print(f"✅ Exported {args.template} template to: {args.output}")
                    
                    # Show summary
                    summary = manager.generate_template_summary(template)
                    print(f"📊 Summary: {summary['total_features']} features, {summary['total_pages']} pages")
                else:
                    print("❌ Failed to export template")
                    sys.exit(1)
            else:
                print(f"❌ Template '{args.template}' not found")
                sys.exit(1)
        
        elif args.command == "compare":
            template1 = manager.get_template(args.template1, args.name1)
            template2 = manager.get_template(args.template2, args.name2)
            
            if template1 and template2:
                comparison = manager.compare_templates(template1, template2)
                print(f"\n🔄 Template Comparison")
                print("=" * 60)
                print(f"Template 1: {comparison['template1']}")
                print(f"Template 2: {comparison['template2']}")
                
                for category, diff in comparison['differences'].items():
                    print(f"\n{category.title()}:")
                    print(f"  Only in {comparison['template1']}: {len(diff['only_in_template1'])}")
                    if diff['only_in_template1']:
                        print(f"    • {', '.join(diff['only_in_template1'][:5])}")
                        if len(diff['only_in_template1']) > 5:
                            print(f"    • ... and {len(diff['only_in_template1']) - 5} more")
                    
                    print(f"  Only in {comparison['template2']}: {len(diff['only_in_template2'])}")
                    if diff['only_in_template2']:
                        print(f"    • {', '.join(diff['only_in_template2'][:5])}")
                        if len(diff['only_in_template2']) > 5:
                            print(f"    • ... and {len(diff['only_in_template2']) - 5} more")
                    
                    print(f"  Common: {len(diff['common'])}")
            else:
                print("❌ Failed to create templates for comparison")
                sys.exit(1)
        
        elif args.command == "recommend":
            try:
                with open(args.requirements, 'r') as f:
                    requirements = json.load(f)
                
                recommendations = manager.get_recommendations(requirements)
                print(f"\n💡 Template Recommendations:")
                print("=" * 60)
                
                if recommendations:
                    for i, rec in enumerate(recommendations, 1):
                        info = manager.template_descriptions.get(rec, {})
                        print(f"{i}. {info.get('name', rec)} ({rec})")
                        print(f"   {info.get('description', 'No description')}")
                        print(f"   Best for: {info.get('best_for', 'General use')}")
                        print()
                else:
                    print("No specific recommendations found. Consider using a custom template.")
                    
                    # Show all templates as alternatives
                    print("\n📋 All Available Templates:")
                    templates = manager.list_templates()
                    for key, info in templates.items():
                        print(f"  • {info['name']} ({key}) - {info['description']}")
            except FileNotFoundError:
                print(f"❌ Requirements file not found: {args.requirements}")
                sys.exit(1)
            except json.JSONDecodeError:
                print(f"❌ Invalid JSON in requirements file: {args.requirements}")
                sys.exit(1)
            except Exception as e:
                print(f"❌ Error reading requirements file: {e}")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled. Goodbye!")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 