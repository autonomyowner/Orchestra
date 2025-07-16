#!/usr/bin/env python3
"""
OpenRouter Setup Script for +++A Project Builder 2030
- Configure OpenRouter API integration
- Set up environment variables
- Test connection
- Cost optimization setup
"""

import os
import sys
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        console.print("❌ Python 3.8+ required", style="red")
        return False
    console.print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected", style="green")
    return True

def install_dependencies():
    """Install required dependencies"""
    console.print("📦 Installing dependencies...", style="blue")
    
    dependencies = [
        "openai>=1.0.0",
        "rich>=13.0.0",
        "python-dotenv>=1.0.0",
        "asyncio"
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            console.print(f"✅ Installed {dep}", style="green")
        except subprocess.CalledProcessError:
            console.print(f"❌ Failed to install {dep}", style="red")
            return False
    
    return True

def setup_environment():
    """Set up environment variables"""
    console.print("🔧 Setting up environment...", style="blue")
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        overwrite = Confirm.ask("📄 .env file already exists. Overwrite?")
        if not overwrite:
            console.print("⏭️  Skipping environment setup", style="yellow")
            return True
    
    # Get OpenRouter API key
    api_key = Prompt.ask("🔑 Enter your OpenRouter API key")
    if not api_key:
        console.print("❌ API key is required", style="red")
        return False
    
    # Create .env file
    env_content = f"""# OpenRouter API Configuration
OPENAI_API_KEY={api_key}
OPENAI_BASE_URL=https://openrouter.ai/api/v1

# Model Selection (OpenRouter Models)
ARCHITECT_MODEL=anthropic/claude-3.5-sonnet
FRONTEND_MODEL=openai/gpt-4o
BACKEND_MODEL=anthropic/claude-3.5-sonnet
DATABASE_MODEL=openai/gpt-4o
DEPLOYMENT_MODEL=anthropic/claude-3.5-sonnet
QUALITY_MODEL=openai/gpt-4o

# Fallback Models (if primary fails)
FALLBACK_MODELS=openai/gpt-4o,anthropic/claude-3.5-sonnet,google/gemini-pro

# Cost Optimization
MAX_TOKENS_PER_REQUEST=4000
ENABLE_COST_OPTIMIZATION=true
USE_CHEAPER_MODELS_FOR_SIMPLE_TASKS=true

# Project Settings
DEFAULT_OUTPUT_DIR=generated_projects
ENABLE_REAL_TIME_PROGRESS=true
SAVE_INTERMEDIATE_RESULTS=true
"""
    
    with open(env_file, "w") as f:
        f.write(env_content)
    
    console.print("✅ Environment file created", style="green")
    return True

def test_connection():
    """Test OpenRouter connection"""
    console.print("🧪 Testing OpenRouter connection...", style="blue")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from core.openrouter_client import OpenRouterClient
        import asyncio
        
        async def test():
            client = OpenRouterClient()
            response, model, cost = await client.generate_with_fallback(
                "Hello! This is a test message. Please respond with 'Connection successful!'",
                task_type="simple",
                complexity="simple"
            )
            return response, model, cost
        
        response, model, cost = asyncio.run(test())
        
        if "Connection successful" in response:
            console.print("✅ OpenRouter connection successful!", style="green")
            console.print(f"🤖 Model used: {model}", style="blue")
            console.print(f"💰 Cost: ${cost:.4f}", style="green")
            return True
        else:
            console.print("⚠️  Connection test returned unexpected response", style="yellow")
            return False
            
    except Exception as e:
        console.print(f"❌ Connection test failed: {e}", style="red")
        return False

def show_cost_guide():
    """Show cost optimization guide"""
    console.print(Panel(
        """[bold blue]💰 OpenRouter Cost Guide[/bold blue]

[green]Model Costs (per 1K tokens):[/green]
• Claude 3.5 Sonnet: $0.003 (Best for planning/architecture)
• GPT-4 Omni: $0.005 (Best for frontend/database)
• Gemini Pro: $0.001 (Best for simple tasks)
• Llama 3.1 8B: $0.0002 (Best for prototyping)

[green]Cost Optimization Tips:[/green]
• Simple tasks use cheaper models automatically
• Fallback system prevents failed requests
• Model selection based on task type
• Real-time cost tracking

[green]Estimated Project Costs:[/green]
• Simple project: $0.50 - $2.00
• Medium project: $2.00 - $8.00  
• Complex project: $8.00 - $20.00
• Enterprise project: $20.00 - $50.00

[bold]Your system will automatically optimize costs![/bold]""",
        title="Cost Optimization",
        border_style="blue"
    ))

def main():
    """Main setup function"""
    console.print(Panel.fit(
        "[bold blue]🚀 OpenRouter Setup for +++A Project Builder 2030[/bold blue]\n\n"
        "This will configure your system to use OpenRouter's multi-model AI platform\n"
        "for maximum performance and cost efficiency.",
        style="bold blue"
    ))
    
    # Step 1: Check Python version
    if not check_python_version():
        return False
    
    # Step 2: Install dependencies
    if not install_dependencies():
        return False
    
    # Step 3: Setup environment
    if not setup_environment():
        return False
    
    # Step 4: Test connection
    if not test_connection():
        console.print("⚠️  Connection test failed, but setup can continue", style="yellow")
    
    # Step 5: Show cost guide
    show_cost_guide()
    
    console.print(Panel.fit(
        "[bold green]✅ OpenRouter Setup Complete![/bold green]\n\n"
        "Your +++A Project Builder 2030 is now configured with OpenRouter.\n\n"
        "[bold]Next Steps:[/bold]\n"
        "1. Add credits to your OpenRouter account\n"
        "2. Run: python project_builder.py --interactive\n"
        "3. Start building your $1M projects! 🚀",
        style="bold green"
    ))
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n⏹️  Setup cancelled by user", style="yellow")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n❌ Setup failed: {e}", style="red")
        sys.exit(1) 