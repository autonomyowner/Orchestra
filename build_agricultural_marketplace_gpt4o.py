#!/usr/bin/env python3
"""
Build "الغلة" Agricultural Marketplace using only GPT-4 Omni via Creative Frontend Builder Agent.
This script patches OpenRouterClient at runtime to force all tasks and fallbacks to GPT-4 Omni.
"""
import asyncio, os, sys
from pathlib import Path
sys.path.append(os.getcwd())

# --- Env vars ---
os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', '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')
os.environ['OPENAI_BASE_URL'] = 'https://openrouter.ai/api/v1'

from core import openrouter_client as orc_module
from rich.console import Console
from main import CreativeFrontendSystem

console = Console()

# --- Force GPT-4 Omni by subclassing ---

class GPT4Client(orc_module.OpenRouterClient):
    """Override model selection to always use GPT-4 Omni."""
    fallback_models = ["openai/gpt-4o"]

    def get_optimal_model(self, task_type: str, complexity: str = "medium") -> str:
        return "openai/gpt-4o"

# Monkey-patch module so any import uses GPT4Client
orc_module.OpenRouterClient = GPT4Client

async def main():
    console.print("[bold green]🚀 Building الغلة agricultural marketplace using GPT-4 Omni only...[/bold green]")
    builder = CreativeFrontendSystem()
    project_spec = {
        "name": "الغلة - Al Ghalla",
        "type": "ecommerce",
        "description": "Modern agricultural marketplace for Algeria featuring farming equipment sales, land rental, agricultural products trading, and expert consultations.",
        "target_audience": "farmers, equipment suppliers, landowners, experts",
        "creative_preference": "warm_artistic",
        "features": ["hero_section", "portfolio_gallery", "service_showcase", "testimonials", "contact_form"],
        "pages": ["Home", "Marketplace Equipment", "Marketplace Products", "About", "Contact"],
        "industry": "agriculture",
        "focus": "frontend_only",
        "quality_level": "enterprise"
    }
    path = await builder.build_creative_frontend(project_spec)
    if path:
        qa = await builder.run_creative_qa(path)
        builder.display_creative_completion_summary(path, qa)
        console.print(f"[bold green]✅ Build finished. Project at {path}[/bold green]")
    else:
        console.print("[red]❌ Build failed.[/red]")

if __name__ == '__main__':
    asyncio.run(main())