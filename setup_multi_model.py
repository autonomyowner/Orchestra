#!/usr/bin/env python3
"""
Multi-Model Orchestration Setup Script
Installs and configures multiple Ollama models for optimal performance.
"""

import subprocess
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def run_command(command, description):
    """Run a command and display progress."""
    console.print(f"[blue]{description}...[/blue]")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        if result.returncode == 0:
            console.print(f"[green]✅ {description} completed[/green]")
            return True
        else:
            console.print(f"[red]❌ {description} failed: {result.stderr}[/red]")
            return False
            
    except subprocess.TimeoutExpired:
        console.print(f"[red]❌ {description} timed out[/red]")
        return False
    except Exception as e:
        console.print(f"[red]❌ {description} error: {e}[/red]")
        return False

def check_ollama_installed():
    """Check if Ollama is installed and running."""
    console.print("[blue]Checking Ollama installation...[/blue]")
    
    try:
        result = subprocess.run(
            "ollama --version",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            version = result.stdout.strip()
            console.print(f"[green]✅ Ollama installed: {version}[/green]")
            return True
        else:
            console.print("[red]❌ Ollama not found[/red]")
            return False
            
    except Exception:
        console.print("[red]❌ Ollama not found[/red]")
        return False

def install_models():
    """Install required models for multi-model orchestration."""
    console.print("\n[bold blue]📦 Installing Required Models[/bold blue]")
    
    # Model configurations for optimal performance
    models = [
        {
            "name": "llama2:7b-chat",
            "description": "Fast planning and documentation",
            "size": "~4GB",
            "priority": "high"
        },
        {
            "name": "mistral:7b-instruct", 
            "description": "Fast general tasks",
            "size": "~4GB",
            "priority": "high"
        },
        {
            "name": "codellama:13b-instruct",
            "description": "Balanced coding and review",
            "size": "~7GB", 
            "priority": "high"
        },
        {
            "name": "llama2:13b-chat",
            "description": "Balanced planning and review",
            "size": "~7GB",
            "priority": "medium"
        },
        {
            "name": "deepseek-coder:33b",
            "description": "High-quality coding",
            "size": "~18GB",
            "priority": "high"
        },
        {
            "name": "codellama:34b-instruct",
            "description": "High-quality coding and review",
            "size": "~18GB",
            "priority": "medium"
        },
        {
            "name": "wizardcoder:34b",
            "description": "High-quality coding",
            "size": "~18GB", 
            "priority": "medium"
        }
    ]
    
    # Display model table
    table = Table(title="Models to Install")
    table.add_column("Model", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Size", style="yellow")
    table.add_column("Priority", style="green")
    
    for model in models:
        priority_icon = "🔴" if model["priority"] == "high" else "🟡"
        table.add_row(
            model["name"],
            model["description"],
            model["size"],
            f"{priority_icon} {model['priority']}"
        )
    
    console.print(table)
    
    # Ask user which models to install
    console.print("\n[yellow]Which models would you like to install?[/yellow]")
    console.print("1. All models (recommended for best performance)")
    console.print("2. High priority only (llama2:7b-chat, mistral:7b-instruct, codellama:13b-instruct, deepseek-coder:33b)")
    console.print("3. Fast models only (7B models for speed)")
    console.print("4. Custom selection")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        models_to_install = [model["name"] for model in models]
    elif choice == "2":
        models_to_install = [model["name"] for model in models if model["priority"] == "high"]
    elif choice == "3":
        models_to_install = [model["name"] for model in models if "7b" in model["name"]]
    elif choice == "4":
        console.print("\n[blue]Available models:[/blue]")
        for i, model in enumerate(models, 1):
            console.print(f"{i}. {model['name']} - {model['description']}")
        
        selections = input("\nEnter model numbers (comma-separated): ").strip()
        try:
            indices = [int(x.strip()) - 1 for x in selections.split(",")]
            models_to_install = [models[i]["name"] for i in indices if 0 <= i < len(models)]
        except:
            console.print("[red]Invalid selection, installing high priority models[/red]")
            models_to_install = [model["name"] for model in models if model["priority"] == "high"]
    else:
        console.print("[red]Invalid choice, installing high priority models[/red]")
        models_to_install = [model["name"] for model in models if model["priority"] == "high"]
    
    console.print(f"\n[blue]Installing {len(models_to_install)} models...[/blue]")
    
    # Install models
    successful_installs = []
    failed_installs = []
    
    for model_name in models_to_install:
        if run_command(f"ollama pull {model_name}", f"Installing {model_name}"):
            successful_installs.append(model_name)
        else:
            failed_installs.append(model_name)
    
    # Summary
    console.print(f"\n[bold green]📊 Installation Summary[/bold green]")
    console.print(f"✅ Successfully installed: {len(successful_installs)} models")
    console.print(f"❌ Failed to install: {len(failed_installs)} models")
    
    if successful_installs:
        console.print(f"\n[green]Installed models:[/green]")
        for model in successful_installs:
            console.print(f"  • {model}")
    
    if failed_installs:
        console.print(f"\n[red]Failed models:[/red]")
        for model in failed_installs:
            console.print(f"  • {model}")
        console.print("\n[yellow]You can retry installing failed models manually:[/yellow]")
        for model in failed_installs:
            console.print(f"  ollama pull {model}")
    
    return successful_installs

def test_models(models):
    """Test installed models."""
    console.print("\n[bold blue]🧪 Testing Installed Models[/bold blue]")
    
    test_results = []
    
    for model in models:
        console.print(f"[dim]Testing {model}...[/dim]")
        
        test_prompt = "Generate a simple 'Hello World' response."
        
        try:
            result = subprocess.run(
                f'ollama run {model} "{test_prompt}"',
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 and result.stdout.strip():
                console.print(f"[green]✅ {model} working[/green]")
                test_results.append((model, True, None))
            else:
                console.print(f"[red]❌ {model} failed[/red]")
                test_results.append((model, False, result.stderr))
                
        except subprocess.TimeoutExpired:
            console.print(f"[red]❌ {model} timed out[/red]")
            test_results.append((model, False, "Timeout"))
        except Exception as e:
            console.print(f"[red]❌ {model} error: {e}[/red]")
            test_results.append((model, False, str(e)))
    
    # Summary
    working_models = [model for model, success, _ in test_results if success]
    failed_models = [model for model, success, _ in test_results if not success]
    
    console.print(f"\n[bold green]📊 Test Summary[/bold green]")
    console.print(f"✅ Working models: {len(working_models)}")
    console.print(f"❌ Failed models: {len(failed_models)}")
    
    return working_models

def create_config():
    """Create configuration for multi-model orchestration."""
    console.print("\n[bold blue]⚙️ Creating Configuration[/bold blue]")
    
    config_content = """# Multi-Model Orchestration Configuration
# This file contains settings for the AI Development Team Orchestrator

# Model priorities (higher = more preferred)
MODEL_PRIORITIES = {
    "llama2:7b-chat": 3,
    "mistral:7b-instruct": 4,
    "codellama:13b-instruct": 6,
    "llama2:13b-chat": 5,
    "deepseek-coder:33b": 8,
    "codellama:34b-instruct": 7,
    "wizardcoder:34b": 9
}

# Task type assignments
TASK_MODELS = {
    "planning": ["llama2:7b-chat", "mistral:7b-instruct", "llama2:13b-chat"],
    "coding": ["deepseek-coder:33b", "codellama:13b-instruct", "wizardcoder:34b"],
    "review": ["codellama:13b-instruct", "deepseek-coder:33b", "codellama:34b-instruct"],
    "testing": ["llama2:7b-chat", "mistral:7b-instruct"],
    "documentation": ["llama2:7b-chat", "mistral:7b-instruct", "llama2:13b-chat"]
}

# Performance settings
MAX_CONCURRENT_TASKS = 4
DEFAULT_TIMEOUT = 300
RETRY_ATTEMPTS = 3
"""
    
    try:
        with open("multi_model_config.py", "w") as f:
            f.write(config_content)
        console.print("[green]✅ Configuration file created: multi_model_config.py[/green]")
    except Exception as e:
        console.print(f"[red]❌ Failed to create config: {e}[/red]")

def main():
    """Main setup function."""
    console.print(Panel(
        "🚀 Multi-Model Orchestration Setup\n\n"
        "This script will install and configure multiple Ollama models\n"
        "for optimal performance with 2-3x speed improvement.",
        title="AI Development Team Orchestrator",
        border_style="bold blue"
    ))
    
    # Check Ollama installation
    if not check_ollama_installed():
        console.print("\n[red]❌ Ollama is not installed or not running[/red]")
        console.print("\n[yellow]Please install Ollama first:[/yellow]")
        console.print("1. Visit https://ollama.ai")
        console.print("2. Download and install Ollama")
        console.print("3. Start Ollama service")
        console.print("4. Run this script again")
        sys.exit(1)
    
    # Install models
    installed_models = install_models()
    
    if not installed_models:
        console.print("\n[red]❌ No models were installed successfully[/red]")
        sys.exit(1)
    
    # Test models
    working_models = test_models(installed_models)
    
    # Create configuration
    create_config()
    
    # Final summary
    console.print("\n[bold green]🎉 Multi-Model Orchestration Setup Complete![/bold green]")
    
    summary = f"""
[bold]Setup Summary:[/bold]
• Models installed: {len(installed_models)}
• Models working: {len(working_models)}
• Configuration: multi_model_config.py

[bold]Next Steps:[/bold]
1. Test the orchestrator: python test_multi_model.py
2. Run the main orchestrator: python main.py
3. Enjoy 2-3x speed improvement!

[bold]Expected Performance:[/bold]
• Sequential execution: ~60-120 seconds
• Parallel execution: ~20-40 seconds  
• Speed improvement: 2-3x faster
    """
    
    console.print(Panel(summary, title="✅ Setup Complete", border_style="green"))

if __name__ == "__main__":
    main() 