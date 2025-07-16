#!/usr/bin/env python3
"""
🎨 Creative Frontend Builder - Quick Start Demo
Test the upgraded creative frontend system with a sample project.
"""

import asyncio
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from core.openrouter_client import OpenRouterClient
    from agents.creative_frontend_builder_agent import CreativeFrontendBuilderAgent
    from main import CreativeFrontendSystem
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("🔧 Make sure you have set up OpenRouter properly")
    sys.exit(1)

console = Console()

async def quick_demo():
    """Quick demo of the creative frontend builder"""
    
    console.print(Panel(
        "[bold cyan]🎨 Creative Frontend Builder - Quick Demo[/bold cyan]\n\n"
        "[green]This demo will create a sample portfolio website to test the system.[/green]\n"
        "[yellow]Make sure you have set up OpenRouter API key first![/yellow]",
        title="Quick Start Demo",
        border_style="magenta"
    ))
    
    try:
        # Initialize the system
        console.print("\n[blue]🔧 Initializing Creative Frontend System...[/blue]")
        builder = CreativeFrontendSystem()
        
        # Sample project specification
        sample_project = {
            "name": "Creative Portfolio",
            "type": "portfolio",
            "description": "A stunning portfolio website showcasing creative work and professional skills",
            "target_audience": "potential clients and employers",
            "creative_preference": "vibrant_creative",
            "features": ["hero_section", "portfolio_gallery", "testimonials", "contact_form"],
            "pages": ["Home", "About", "Portfolio", "Contact"],
            "industry": "portfolio",
            "focus": "frontend_only",
            "quality_level": "enterprise"
        }
        
        console.print("[green]✅ System initialized successfully![/green]")
        console.print("\n[cyan]📋 Sample Project Specification:[/cyan]")
        
        # Display project details
        for key, value in sample_project.items():
            if isinstance(value, list):
                value = ", ".join(value)
            console.print(f"  • [bold]{key.replace('_', ' ').title()}:[/bold] {value}")
        
        # Build the project
        console.print(f"\n[bold green]🚀 Building Creative Frontend...[/bold green]")
        project_path = await builder.build_creative_frontend(sample_project)
        
        if project_path:
            # Run QA
            qa_results = await builder.run_creative_qa(project_path)
            
            # Display results
            console.print(f"\n[bold green]🎉 SUCCESS![/bold green]")
            console.print(f"[cyan]Project created at:[/cyan] {project_path}")
            
            # Show project structure
            console.print("\n[bold]📁 Generated Project Structure:[/bold]")
            project_dir = Path(project_path)
            if project_dir.exists():
                for item in sorted(project_dir.iterdir())[:10]:  # Show first 10 items
                    if item.is_file():
                        console.print(f"  📄 {item.name}")
                    else:
                        console.print(f"  📁 {item.name}/")
                
                if len(list(project_dir.iterdir())) > 10:
                    console.print("  ...")
            
            # Quick start instructions
            instructions = f"""
[bold yellow]🚀 Quick Start Instructions:[/bold yellow]

1. Navigate to your project:
   [cyan]cd {project_path}[/cyan]

2. Install dependencies:
   [cyan]npm install[/cyan]

3. Start development server:
   [cyan]npm run dev[/cyan]

4. Open in browser:
   [cyan]http://localhost:3000[/cyan]

5. Build for production:
   [cyan]npm run build[/cyan]

[bold green]Your creative frontend is ready! 🎨[/bold green]
            """
            
            console.print(Panel(instructions, title="Next Steps", border_style="green"))
            
        else:
            console.print("[red]❌ Build failed. Check your OpenRouter setup.[/red]")
            
    except Exception as e:
        console.print(f"[red]❌ Demo failed: {e}[/red]")
        console.print("[yellow]💡 Make sure you have run 'python setup_openrouter.py' first[/yellow]")

async def test_system_components():
    """Test individual system components"""
    
    console.print(Panel(
        "[bold blue]🔍 Testing System Components[/bold blue]",
        border_style="blue"
    ))
    
    # Test OpenRouter client
    try:
        console.print("[blue]Testing OpenRouter connection...[/blue]")
        client = OpenRouterClient()
        
        # Simple test prompt
        response, model, cost = await client.generate_with_fallback(
            "Hello! Please respond with 'System test successful'",
            task_type="simple",
            complexity="simple"
        )
        
        if "successful" in response.lower():
            console.print("[green]✅ OpenRouter connection working[/green]")
        else:
            console.print("[yellow]⚠️ OpenRouter responding but unexpected output[/yellow]")
            
    except Exception as e:
        console.print(f"[red]❌ OpenRouter test failed: {e}[/red]")
        return False
    
    # Test Creative Builder Agent
    try:
        console.print("[blue]Testing Creative Builder Agent...[/blue]")
        builder_agent = CreativeFrontendBuilderAgent()
        console.print("[green]✅ Creative Builder Agent initialized[/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Creative Builder Agent test failed: {e}[/red]")
        return False
    
    console.print("[bold green]🎉 All system components working![/bold green]")
    return True

def check_environment():
    """Check if environment is properly set up"""
    
    console.print(Panel(
        "[bold yellow]🔧 Environment Check[/bold yellow]",
        border_style="yellow"
    ))
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        console.print("[green]✅ .env file found[/green]")
    else:
        console.print("[red]❌ .env file not found[/red]")
        console.print("[yellow]💡 Run 'python setup_openrouter.py' to create it[/yellow]")
        return False
    
    # Check OpenRouter API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        console.print("[green]✅ OpenRouter API key configured[/green]")
    else:
        console.print("[red]❌ OpenRouter API key not found[/red]")
        console.print("[yellow]💡 Set OPENAI_API_KEY in your .env file[/yellow]")
        return False
    
    # Check output directory
    output_dir = Path("generated_projects")
    output_dir.mkdir(exist_ok=True)
    console.print("[green]✅ Output directory ready[/green]")
    
    return True

async def main():
    """Main quick start function"""
    
    console.print(Panel.fit(
        "[bold magenta]🎨 CREATIVE FRONTEND BUILDER[/bold magenta]\n"
        "[cyan]Quick Start Demo & System Test[/cyan]",
        style="bold magenta"
    ))
    
    # Check environment
    if not check_environment():
        console.print("\n[red]❌ Environment setup required[/red]")
        console.print("[yellow]Please run 'python setup_openrouter.py' first[/yellow]")
        return
    
    # Test system components
    if not await test_system_components():
        console.print("\n[red]❌ System component tests failed[/red]")
        return
    
    # Run demo
    console.print("\n" + "="*60)
    await quick_demo()

if __name__ == "__main__":
    asyncio.run(main())