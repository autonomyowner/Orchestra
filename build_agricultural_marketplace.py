#!/usr/bin/env python3
"""
🌾 Agricultural Marketplace Builder
Builds "الغلة" - Algerian Agricultural Marketplace using the Creative Frontend Builder Agent
"""

import asyncio
import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set environment variables
os.environ['OPENAI_API_KEY'] = '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'
os.environ['OPENAI_BASE_URL'] = 'https://openrouter.ai/api/v1'

from main import CreativeFrontendSystem
from rich.console import Console

console = Console()

async def build_agricultural_marketplace():
    """Build the agricultural marketplace using the agent"""
    
    console.print("🌾 [bold green]Launching Creative Frontend Builder Agent[/bold green]")
    console.print("🎯 [cyan]Building الغلة - Algerian Agricultural Marketplace[/cyan]")
    
    # Initialize the creative frontend system
    builder = CreativeFrontendSystem()
    
    # Perfect project specification for agricultural marketplace
    agricultural_project = {
        "name": "الغلة - Al Ghalla",
        "type": "ecommerce",  # E-commerce type for marketplace
        "description": "Modern agricultural marketplace for Algeria featuring farming equipment sales, land rental services, agricultural products trading, and expert consultations. A comprehensive platform connecting farmers, equipment suppliers, landowners, and agricultural experts.",
        "target_audience": "farmers, agricultural businesses, equipment suppliers, landowners, agricultural experts in Algeria",
        "creative_preference": "warm_artistic",  # Perfect for agricultural theme
        "features": [
            "hero_section",           # Stunning hero with farm imagery
            "portfolio_gallery",     # Equipment and products gallery  
            "service_showcase",       # Services like land rental, consultations
            "testimonials",          # Farmer success stories
            "contact_form"           # Expert consultation requests
        ],
        "pages": [
            "Home",                  # Main landing page
            "Marketplace Equipment", # Equipment buying/selling
            "Marketplace Products",  # Agricultural products trading
            "About",                 # About الغلة platform
            "Contact"               # Contact and expert consultation
        ],
        "industry": "agriculture",
        "focus": "frontend_only",
        "quality_level": "enterprise",
        "special_requirements": {
            "language_support": "Arabic and French (Algeria)",
            "color_scheme": "earth tones with green agricultural theme",
            "imagery": "farming, tractors, crops, landscapes",
            "rtl_support": True,  # For Arabic text
            "marketplace_features": [
                "Equipment listings",
                "Product trading",
                "Land rental",
                "Expert consultations",
                "Farmer profiles",
                "Search and filters"
            ]
        }
    }
    
    console.print("\n🚀 [bold magenta]Agent is building your agricultural marketplace...[/bold magenta]")
    
    # Build the project using the agent
    project_path = await builder.build_creative_frontend(agricultural_project)
    
    if project_path:
        # Run QA
        qa_results = await builder.run_creative_qa(project_path)
        
        # Display results
        builder.display_creative_completion_summary(project_path, qa_results)
        
        console.print(f"\n🌾 [bold green]الغلة Agricultural Marketplace Ready![/bold green]")
        console.print(f"📁 [cyan]Location:[/cyan] {project_path}")
        
    else:
        console.print("❌ [red]Build failed. Please check your API setup.[/red]")

if __name__ == "__main__":
    asyncio.run(build_agricultural_marketplace())