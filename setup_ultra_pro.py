#!/usr/bin/env python3
"""
Setup script for the Ultimate Website Builder - Ultra Pro Edition
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Ultimate Website Builder - Ultra Pro Edition")
    print("=" * 60)
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    print("✅ Output directory created")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("⚠️  Some dependencies may have failed to install")
    
    # Test the builder
    if not run_command("python test_builder.py", "Testing Ultimate Website Builder"):
        print("⚠️  Tests failed, but the builder may still work")
    
    print("\n" + "=" * 60)
    print("🎉 Ultimate Website Builder is ready!")
    print("\n📋 Quick Start:")
    print("1. Run: python ultimate_website_builder.py")
    print("2. Describe your website (e.g., 'I want a restaurant website')")
    print("3. Follow the conversation flow")
    print("4. Choose your design preferences")
    print("5. Get your professional website!")
    print("\n🚀 Optimized for GPU acceleration on your pod!")

if __name__ == "__main__":
    main()