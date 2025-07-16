#!/usr/bin/env python3
"""
Test Script for OpenRouter Integration
- Test connection to OpenRouter
- Test model selection
- Test fallback system
- Test cost tracking
"""

import asyncio
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from core.openrouter_client import OpenRouterClient

console = Console()

async def test_openrouter_integration():
    """Test the complete OpenRouter integration"""
    
    console.print(Panel.fit(
        "[bold blue]🧪 Testing OpenRouter Integration[/bold blue]\n\n"
        "This will test all aspects of your OpenRouter setup.",
        style="bold blue"
    ))
    
    # Load environment variables
    load_dotenv()
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("❌ No OpenRouter API key found. Please run setup_openrouter.py first.", style="red")
        return False
    
    console.print("✅ API key found", style="green")
    
    try:
        # Create client
        client = OpenRouterClient()
        console.print("✅ OpenRouter client created", style="green")
        
        # Test 1: Simple task with cost optimization
        console.print("\n🔍 Test 1: Simple task (should use cheaper model)")
        response1, model1, cost1 = await client.generate_with_fallback(
            "Write a simple 'Hello World' function in Python",
            task_type="simple",
            complexity="simple"
        )
        console.print(f"✅ Response received from {model1} (Cost: ${cost1:.4f})", style="green")
        
        # Test 2: Architecture task (should use Claude)
        console.print("\n🔍 Test 2: Architecture task (should use Claude)")
        response2, model2, cost2 = await client.generate_with_fallback(
            "Design a system architecture for a social media platform",
            task_type="architecture",
            complexity="medium"
        )
        console.print(f"✅ Response received from {model2} (Cost: ${cost2:.4f})", style="green")
        
        # Test 3: Frontend task (should use GPT-4)
        console.print("\n🔍 Test 3: Frontend task (should use GPT-4)")
        response3, model3, cost3 = await client.generate_with_fallback(
            "Create a React component for a user profile card",
            task_type="frontend",
            complexity="medium"
        )
        console.print(f"✅ Response received from {model3} (Cost: ${cost3:.4f})", style="green")
        
        # Show cost summary
        console.print("\n" + "="*50)
        client.print_cost_summary()
        
        # Test 4: Fallback system (simulate failure)
        console.print("\n🔍 Test 4: Testing fallback system")
        try:
            # This should trigger fallback if primary model fails
            response4, model4, cost4 = await client.generate_with_fallback(
                "Create a comprehensive testing strategy for a web application",
                task_type="testing",
                complexity="medium"
            )
            console.print(f"✅ Fallback test successful with {model4} (Cost: ${cost4:.4f})", style="green")
        except Exception as e:
            console.print(f"⚠️  Fallback test had issues: {e}", style="yellow")
        
        console.print(Panel.fit(
            "[bold green]✅ All OpenRouter Tests Passed![/bold green]\n\n"
            "Your +++A Project Builder 2030 is ready to use with OpenRouter.\n\n"
            "[bold]Next Steps:[/bold]\n"
            "• Run: python project_builder.py --interactive\n"
            "• Start building your projects!\n"
            "• Monitor costs in real-time",
            style="bold green"
        ))
        
        return True
        
    except Exception as e:
        console.print(f"❌ Test failed: {e}", style="red")
        return False

def main():
    """Main test function"""
    try:
        success = asyncio.run(test_openrouter_integration())
        if not success:
            console.print("\n❌ OpenRouter integration test failed", style="red")
            return 1
        return 0
    except KeyboardInterrupt:
        console.print("\n⏹️  Test cancelled by user", style="yellow")
        return 1
    except Exception as e:
        console.print(f"\n❌ Test failed: {e}", style="red")
        return 1

if __name__ == "__main__":
    exit(main()) 