#!/usr/bin/env python3
"""
Quick Fix Script for AI Development Team Orchestrator
Automatically fixes common issues causing basic outputs instead of comprehensive applications.
"""

import os
import subprocess
import requests
import time
import json

def run_command(command: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def check_ollama_running() -> bool:
    """Check if Ollama is running."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def fix_ollama_service():
    """Fix Ollama service issues."""
    print("\n🤖 Fixing Ollama Service...")
    
    # Kill any existing Ollama processes
    run_command("pkill -f ollama", "Stopping existing Ollama processes")
    time.sleep(2)
    
    # Start Ollama service
    if run_command("ollama serve &", "Starting Ollama service"):
        print("⏳ Waiting for Ollama to start...")
        time.sleep(5)
        
        # Test if it's working
        if check_ollama_running():
            print("✅ Ollama service is now running")
            return True
        else:
            print("❌ Ollama service failed to start properly")
            return False
    return False

def fix_models():
    """Fix model issues by re-pulling them."""
    print("\n📦 Fixing Models...")
    
    models = ["llama2:7b-chat", "deepseek-coder:33b"]
    success_count = 0
    
    for model in models:
        print(f"📥 Re-pulling {model}...")
        if run_command(f"ollama pull {model}", f"Pulling {model}"):
            success_count += 1
        else:
            print(f"⚠️ Failed to pull {model}, continuing...")
    
    return success_count > 0

def fix_python_dependencies():
    """Fix Python dependency issues."""
    print("\n🐍 Fixing Python Dependencies...")
    
    # Upgrade pip
    run_command("pip install --upgrade pip", "Upgrading pip")
    
    # Install requirements
    if os.path.exists("requirements.txt"):
        return run_command("pip install -r requirements.txt", "Installing Python dependencies")
    else:
        print("❌ requirements.txt not found")
        return False

def fix_permissions():
    """Fix file permission issues."""
    print("\n🔐 Fixing Permissions...")
    
    # Make scripts executable
    scripts = ["main.py", "setup.sh", "diagnose_issues.py", "quick_fix.py"]
    for script in scripts:
        if os.path.exists(script):
            run_command(f"chmod +x {script}", f"Making {script} executable")
    
    return True

def optimize_ollama_settings():
    """Optimize Ollama settings for better performance."""
    print("\n⚡ Optimizing Ollama Settings...")
    
    # Create optimized Ollama configuration
    config_dir = os.path.expanduser("~/.ollama")
    os.makedirs(config_dir, exist_ok=True)
    
    # Set environment variables for better performance
    env_vars = {
        "OLLAMA_HOST": "0.0.0.0:11434",
        "OLLAMA_ORIGINS": "*",
        "OLLAMA_MAX_LOADED_MODELS": "2",
        "OLLAMA_NUM_PARALLEL": "4",
        "OLLAMA_MAX_QUEUE": "512"
    }
    
    # Add to shell profile
    shell_profile = os.path.expanduser("~/.bashrc")
    if os.path.exists(shell_profile):
        with open(shell_profile, "a") as f:
            f.write("\n# Ollama Optimizations\n")
            for key, value in env_vars.items():
                f.write(f"export {key}={value}\n")
        print("✅ Added Ollama optimizations to ~/.bashrc")
    
    return True

def test_model_response():
    """Test if models are responding properly."""
    print("\n🧪 Testing Model Responses...")
    
    test_prompts = {
        "llama2:7b-chat": "Create a simple technical specification for a todo app in JSON format.",
        "deepseek-coder:33b": "Create a simple React component for a button with TypeScript."
    }
    
    success_count = 0
    
    for model, prompt in test_prompts.items():
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_ctx": 2000
                }
            }
            
            response = requests.post(
                "http://localhost:11434/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "")
                
                if len(response_text) > 100:
                    print(f"✅ {model} generated substantial response ({len(response_text)} chars)")
                    success_count += 1
                else:
                    print(f"⚠️ {model} generated short response ({len(response_text)} chars)")
            else:
                print(f"❌ {model} failed with status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {model} test failed: {e}")
    
    return success_count > 0

def create_backup_config():
    """Create a backup configuration for the orchestrator."""
    print("\n💾 Creating Backup Configuration...")
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Create a sample project specification
    sample_spec = {
        "project_name": "sample-app",
        "description": "A sample application for testing",
        "purpose": "saas",
        "target_audience": "developers",
        "design_style": "modern",
        "color_scheme": "blue",
        "mobile_first": True,
        "pages": ["Landing/Home", "About", "Contact"],
        "auth_required": True,
        "auth_methods": "email",
        "features": ["user_management", "api"],
        "database_type": "postgresql",
        "deployment_preference": "vercel",
        "third_party_integrations": [],
        "expected_users": "100-1000",
        "performance_priority": "user_experience",
        "seo_important": True,
        "analytics_required": False,
        "cms_needed": False,
        "multi_language": False,
        "custom_requirements": "",
        "budget_tier": "free"
    }
    
    with open("data/sample_project_spec.json", "w") as f:
        json.dump(sample_spec, f, indent=2)
    
    print("✅ Created sample project specification")
    return True

def main():
    """Run all quick fixes."""
    print("🚀 AI Development Team Orchestrator - Quick Fix Tool")
    print("=" * 60)
    
    fixes_applied = 0
    total_fixes = 6
    
    # Fix 1: Ollama Service
    if fix_ollama_service():
        fixes_applied += 1
    
    # Fix 2: Models
    if fix_models():
        fixes_applied += 1
    
    # Fix 3: Python Dependencies
    if fix_python_dependencies():
        fixes_applied += 1
    
    # Fix 4: Permissions
    if fix_permissions():
        fixes_applied += 1
    
    # Fix 5: Ollama Settings
    if optimize_ollama_settings():
        fixes_applied += 1
    
    # Fix 6: Test Models
    if test_model_response():
        fixes_applied += 1
    
    # Create backup config
    create_backup_config()
    
    print(f"\n📊 QUICK FIX RESULTS")
    print("=" * 60)
    print(f"✅ Fixes Applied: {fixes_applied}/{total_fixes}")
    
    if fixes_applied >= 4:
        print("\n🎉 Most issues have been fixed!")
        print("Try running the orchestrator now:")
        print("  python main.py")
    else:
        print("\n⚠️ Some issues remain. Run the diagnostic tool:")
        print("  python diagnose_issues.py")
    
    print(f"\n💡 Next Steps:")
    print("1. Restart your terminal to apply environment changes")
    print("2. Run: python diagnose_issues.py")
    print("3. Try: python main.py")
    print("4. If issues persist, check the diagnostic output")

if __name__ == "__main__":
    main() 