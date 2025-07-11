#!/usr/bin/env python3
"""
Diagnostic script for AI Development Team Orchestrator
Helps identify and fix issues causing basic outputs instead of comprehensive applications.
"""

import json
import os
import subprocess
import requests
from typing import Dict, Any, List

def check_ollama_status() -> Dict[str, Any]:
    """Check Ollama service status and model availability."""
    print("🔍 Checking Ollama service...")
    
    status = {
        "ollama_running": False,
        "models_available": [],
        "models_working": [],
        "issues": []
    }
    
    try:
        # Check if Ollama is running
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            status["ollama_running"] = True
            models = response.json().get("models", [])
            status["models_available"] = [model["name"] for model in models]
            
            # Test each model
            for model in status["models_available"]:
                if test_model_response(model):
                    status["models_working"].append(model)
                else:
                    status["issues"].append(f"Model {model} is not responding properly")
        else:
            status["issues"].append(f"Ollama API returned status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        status["issues"].append("Ollama service is not running or not accessible")
    except Exception as e:
        status["issues"].append(f"Error checking Ollama: {e}")
    
    return status

def test_model_response(model: str) -> bool:
    """Test if a model can generate a response."""
    try:
        payload = {
            "model": model,
            "prompt": "Say 'Hello World'",
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_ctx": 100
            }
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return len(result.get("response", "").strip()) > 0
        return False
        
    except Exception:
        return False

def check_system_resources() -> Dict[str, Any]:
    """Check system resources."""
    print("💻 Checking system resources...")
    
    resources = {
        "memory_available": "Unknown",
        "disk_space": "Unknown",
        "cpu_cores": "Unknown",
        "issues": []
    }
    
    try:
        # Check memory (Linux/Mac)
        if os.name != 'nt':  # Not Windows
            result = subprocess.run(['free', '-h'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                if len(lines) > 1:
                    mem_line = lines[1].split()
                    if len(mem_line) > 1:
                        resources["memory_available"] = mem_line[1]
        
        # Check disk space
        if os.name != 'nt':
            result = subprocess.run(['df', '-h', '.'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                if len(lines) > 1:
                    disk_line = lines[1].split()
                    if len(disk_line) > 3:
                        resources["disk_space"] = disk_line[3]
        
        # Check CPU cores
        import multiprocessing
        resources["cpu_cores"] = str(multiprocessing.cpu_count())
        
    except Exception as e:
        resources["issues"].append(f"Error checking resources: {e}")
    
    return resources

def check_python_environment() -> Dict[str, Any]:
    """Check Python environment and dependencies."""
    print("🐍 Checking Python environment...")
    
    env = {
        "python_version": "Unknown",
        "dependencies_installed": [],
        "missing_dependencies": [],
        "issues": []
    }
    
    try:
        # Check Python version
        import sys
        env["python_version"] = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        
        # Check required dependencies
        required_deps = [
            "requests", "rich", "click", "pydantic", 
            "jsonschema", "gitpython", "python-dotenv"
        ]
        
        for dep in required_deps:
            try:
                __import__(dep)
                env["dependencies_installed"].append(dep)
            except ImportError:
                env["missing_dependencies"].append(dep)
        
        if env["missing_dependencies"]:
            env["issues"].append(f"Missing dependencies: {', '.join(env['missing_dependencies'])}")
            
    except Exception as e:
        env["issues"].append(f"Error checking Python environment: {e}")
    
    return env

def check_project_structure() -> Dict[str, Any]:
    """Check if project structure is correct."""
    print("📁 Checking project structure...")
    
    structure = {
        "files_present": [],
        "files_missing": [],
        "issues": []
    }
    
    required_files = [
        "main.py",
        "cli_wizard.py",
        "requirements.txt",
        "agents/planner.py",
        "agents/builder.py",
        "agents/reviewer.py",
        "agents/fixer.py",
        "agents/finalizer.py",
        "agents/git_pusher.py",
        "prompts/planner_prompt.txt",
        "prompts/builder_prompt.txt",
        "prompts/reviewer_prompt.txt",
        "prompts/fixer_prompt.txt",
        "prompts/finalizer_prompt.txt",
        "prompts/git_pusher_prompt.txt",
        "utils/ollama_client.py"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            structure["files_present"].append(file_path)
        else:
            structure["files_missing"].append(file_path)
    
    if structure["files_missing"]:
        structure["issues"].append(f"Missing files: {', '.join(structure['files_missing'])}")
    
    return structure

def test_model_generation() -> Dict[str, Any]:
    """Test actual model generation capabilities."""
    print("🧪 Testing model generation...")
    
    test_results = {
        "planner_test": {"success": False, "response_length": 0, "error": None},
        "builder_test": {"success": False, "response_length": 0, "error": None},
        "issues": []
    }
    
    try:
        # Test planner model
        planner_prompt = "Create a simple technical specification for a todo app."
        payload = {
            "model": "llama2:7b-chat",
            "prompt": planner_prompt,
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
            test_results["planner_test"]["success"] = True
            test_results["planner_test"]["response_length"] = len(response_text)
            
            if len(response_text) < 100:
                test_results["issues"].append("Planner model generated very short response")
        else:
            test_results["planner_test"]["error"] = f"HTTP {response.status_code}"
            
    except Exception as e:
        test_results["planner_test"]["error"] = str(e)
        test_results["issues"].append(f"Planner test failed: {e}")
    
    try:
        # Test builder model
        builder_prompt = "Create a simple React component for a button."
        payload = {
            "model": "deepseek-coder:33b",
            "prompt": builder_prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
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
            test_results["builder_test"]["success"] = True
            test_results["builder_test"]["response_length"] = len(response_text)
            
            if len(response_text) < 50:
                test_results["issues"].append("Builder model generated very short response")
        else:
            test_results["builder_test"]["error"] = f"HTTP {response.status_code}"
            
    except Exception as e:
        test_results["builder_test"]["error"] = str(e)
        test_results["issues"].append(f"Builder test failed: {e}")
    
    return test_results

def generate_fixes(issues: List[str]) -> List[str]:
    """Generate fix suggestions based on identified issues."""
    fixes = []
    
    for issue in issues:
        if "Ollama service is not running" in issue:
            fixes.append("🔧 Start Ollama: ollama serve")
        elif "Model" in issue and "not responding" in issue:
            fixes.append("🔧 Re-pull the problematic model: ollama pull <model-name>")
        elif "Missing dependencies" in issue:
            fixes.append("🔧 Install missing dependencies: pip install -r requirements.txt")
        elif "very short response" in issue:
            fixes.append("🔧 Increase model context or try different temperature settings")
        elif "timeout" in issue.lower():
            fixes.append("🔧 Increase timeout settings or reduce prompt size")
        else:
            fixes.append(f"🔧 Investigate: {issue}")
    
    return fixes

def main():
    """Run comprehensive diagnostics."""
    print("🚀 AI Development Team Orchestrator - Diagnostic Tool")
    print("=" * 60)
    
    # Run all checks
    ollama_status = check_ollama_status()
    system_resources = check_system_resources()
    python_env = check_python_environment()
    project_structure = check_project_structure()
    model_tests = test_model_generation()
    
    # Compile all issues
    all_issues = []
    all_issues.extend(ollama_status["issues"])
    all_issues.extend(system_resources["issues"])
    all_issues.extend(python_env["issues"])
    all_issues.extend(project_structure["issues"])
    all_issues.extend(model_tests["issues"])
    
    # Generate fixes
    fixes = generate_fixes(all_issues)
    
    # Print results
    print("\n📊 DIAGNOSTIC RESULTS")
    print("=" * 60)
    
    print(f"\n🤖 Ollama Status:")
    print(f"  Running: {'✅' if ollama_status['ollama_running'] else '❌'}")
    print(f"  Available Models: {', '.join(ollama_status['models_available'])}")
    print(f"  Working Models: {', '.join(ollama_status['models_working'])}")
    
    print(f"\n💻 System Resources:")
    print(f"  Memory: {system_resources['memory_available']}")
    print(f"  Disk Space: {system_resources['disk_space']}")
    print(f"  CPU Cores: {system_resources['cpu_cores']}")
    
    print(f"\n🐍 Python Environment:")
    print(f"  Version: {python_env['python_version']}")
    print(f"  Dependencies: {len(python_env['dependencies_installed'])}/{len(python_env['dependencies_installed']) + len(python_env['missing_dependencies'])} installed")
    
    print(f"\n📁 Project Structure:")
    print(f"  Files Present: {len(project_structure['files_present'])}/{len(project_structure['files_present']) + len(project_structure['files_missing'])}")
    
    print(f"\n🧪 Model Tests:")
    print(f"  Planner: {'✅' if model_tests['planner_test']['success'] else '❌'} ({model_tests['planner_test']['response_length']} chars)")
    print(f"  Builder: {'✅' if model_tests['builder_test']['success'] else '❌'} ({model_tests['builder_test']['response_length']} chars)")
    
    if all_issues:
        print(f"\n❌ ISSUES FOUND ({len(all_issues)}):")
        for i, issue in enumerate(all_issues, 1):
            print(f"  {i}. {issue}")
        
        print(f"\n🔧 RECOMMENDED FIXES:")
        for i, fix in enumerate(fixes, 1):
            print(f"  {i}. {fix}")
        
        print(f"\n💡 QUICK FIXES:")
        print("  1. Restart Ollama: pkill ollama && ollama serve")
        print("  2. Re-pull models: ollama pull llama2:7b-chat && ollama pull deepseek-coder:33b")
        print("  3. Check system resources (RAM, disk space)")
        print("  4. Verify all project files are present")
        
    else:
        print(f"\n✅ No issues found! Your setup should work correctly.")
        print("If you're still getting basic outputs, try:")
        print("  1. Increase timeout settings in ollama_client.py")
        print("  2. Reduce max_tokens to avoid timeouts")
        print("  3. Check if models are generating proper responses")
    
    print(f"\n📝 Next Steps:")
    print("  1. Apply the recommended fixes above")
    print("  2. Run this diagnostic again to verify fixes")
    print("  3. Try running the orchestrator: python main.py")
    print("  4. Monitor the output for specific error messages")

if __name__ == "__main__":
    main() 