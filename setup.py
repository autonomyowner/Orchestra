#!/usr/bin/env python3
"""
+++A Project Builder 2030 Setup Script
Automated installation and configuration
"""

import os
import sys
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def check_prerequisites():
    """Check system prerequisites"""
    
    console.print("🔍 Checking system prerequisites...")
    
    # Check Python version
    if sys.version_info < (3, 9):
        console.print("❌ Python 3.9+ required. Please upgrade Python.", style="red")
        return False
    
    console.print("✅ Python version check passed", style="green")
    
    # Check pip
    try:
        subprocess.run(["pip", "--version"], check=True, capture_output=True)
        console.print("✅ pip is available", style="green")
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print("❌ pip not found. Please install pip.", style="red")
        return False
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    
    console.print("\n📦 Installing Python dependencies...")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Installing packages...", total=None)
            
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                console.print("✅ Dependencies installed successfully", style="green")
                return True
            else:
                console.print(f"❌ Failed to install dependencies: {result.stderr}", style="red")
                return False
                
    except Exception as e:
        console.print(f"❌ Installation error: {e}", style="red")
        return False

def setup_environment():
    """Setup environment configuration"""
    
    console.print("\n⚙️ Setting up environment configuration...")
    
    env_file = Path(".env")
    env_example = Path("config/env_example.txt")
    
    if not env_file.exists() and env_example.exists():
        # Copy example to .env
        env_content = env_example.read_text()
        env_file.write_text(env_content)
        console.print("✅ Created .env file from template", style="green")
        console.print("📝 Please edit .env file and add your API keys", style="yellow")
    else:
        console.print("ℹ️ Environment file already exists", style="blue")
    
    return True

def create_directories():
    """Create necessary directories"""
    
    console.print("\n📁 Creating project directories...")
    
    directories = [
        "generated_projects",
        "logs",
        "cache"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        console.print(f"✅ Created {directory}/", style="green")
    
    return True

def verify_installation():
    """Verify installation by running a simple test"""
    
    console.print("\n🧪 Verifying installation...")
    
    try:
        # Test import of main modules
        sys.path.append(str(Path("core")))
        sys.path.append(str(Path("integrations")))
        
        from multi_agent_system import MultiAgentOrchestrator
        from api_integration_system import APIIntegrationManager
        
        console.print("✅ Core modules imported successfully", style="green")
        
        # Test OpenAI key presence (not validity)
        if os.getenv("OPENAI_API_KEY"):
            console.print("✅ OpenAI API key found in environment", style="green")
        else:
            console.print("⚠️ OpenAI API key not found. Add it to .env file", style="yellow")
        
        return True
        
    except ImportError as e:
        console.print(f"❌ Module import failed: {e}", style="red")
        return False

def display_success():
    """Display success message and next steps"""
    
    success_text = """
🎉 +++A Project Builder 2030 Setup Complete!

✅ Dependencies installed
✅ Environment configured  
✅ Directories created
✅ Installation verified

🚀 NEXT STEPS:

1. Add your OpenAI API key to .env file:
   OPENAI_API_KEY=sk-your-key-here

2. Try the demo:
   python project_builder.py --demo

3. Go interactive:
   python project_builder.py --interactive

4. Build your first project:
   python project_builder.py "Build a SaaS platform"

📚 Documentation: docs/README.md
💡 Examples: examples/
🔧 Configuration: config/

Happy building! 🚀
"""
    
    console.print(Panel.fit(success_text, style="bold green", title="🏆 SETUP COMPLETE"))

def main():
    """Main setup function"""
    
    console.print(Panel.fit("""
🚀 +++A Project Builder 2030 Setup

This script will:
• Check system prerequisites
• Install Python dependencies  
• Setup environment configuration
• Create necessary directories
• Verify installation
    """, style="bold blue", title="🛠️ SETUP"))
    
    # Check prerequisites
    if not check_prerequisites():
        console.print("\n❌ Prerequisites check failed. Please fix issues and try again.")
        return 1
    
    # Install dependencies
    if not install_dependencies():
        console.print("\n❌ Dependency installation failed.")
        return 1
    
    # Setup environment
    if not setup_environment():
        console.print("\n❌ Environment setup failed.")
        return 1
    
    # Create directories
    if not create_directories():
        console.print("\n❌ Directory creation failed.")
        return 1
    
    # Verify installation
    if not verify_installation():
        console.print("\n❌ Installation verification failed.")
        return 1
    
    # Success!
    display_success()
    return 0

if __name__ == "__main__":
    sys.exit(main()) 