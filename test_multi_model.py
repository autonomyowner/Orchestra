#!/usr/bin/env python3
"""
Multi-Model Orchestration Test Script
Demonstrates the 2-3x speed improvement using multiple Ollama models simultaneously.
"""

import asyncio
import time
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from model_orchestrator import get_orchestrator, TaskType
from utils.ollama_client import OllamaClient

console = Console()

async def test_sequential_execution():
    """Test sequential execution for comparison."""
    console.print("\n[bold blue]🔄 Testing Sequential Execution[/bold blue]")
    
    ollama_client = OllamaClient()
    
    tasks = [
        ("Planning", "Create a technical specification for a SaaS platform"),
        ("Coding", "Write a React component for user authentication"),
        ("Review", "Review this code for security issues: console.log(password)"),
        ("Documentation", "Write API documentation for user endpoints")
    ]
    
    start_time = time.time()
    results = []
    
    for task_name, prompt in tasks:
        console.print(f"[dim]Executing {task_name}...[/dim]")
        result = ollama_client.generate("llama2:7b-chat", prompt, temperature=0.7)
        results.append((task_name, result))
    
    sequential_time = time.time() - start_time
    console.print(f"[yellow]Sequential execution time: {sequential_time:.2f} seconds[/yellow]")
    
    return sequential_time, results

async def test_parallel_execution():
    """Test parallel execution with orchestrator."""
    console.print("\n[bold green]🚀 Testing Parallel Execution with Multi-Model Orchestrator[/bold green]")
    
    orchestrator = get_orchestrator()
    
    # Get available models
    available_models = orchestrator.get_available_models()
    console.print(f"[blue]Available models: {len(available_models)}[/blue]")
    for model in available_models:
        config = orchestrator.model_configs[model]
        console.print(f"  • {model} ({config.tier.value})")
    
    # Define parallel tasks
    parallel_tasks = [
        (TaskType.PLANNING, "Create a technical specification for a SaaS platform", "medium"),
        (TaskType.CODING, "Write a React component for user authentication", "simple"),
        (TaskType.REVIEW, "Review this code for security issues: console.log(password)", "simple"),
        (TaskType.DOCUMENTATION, "Write API documentation for user endpoints", "simple")
    ]
    
    start_time = time.time()
    
    # Execute tasks in parallel
    results = await orchestrator.execute_parallel_tasks(parallel_tasks)
    
    parallel_time = time.time() - start_time
    console.print(f"[green]Parallel execution time: {parallel_time:.2f} seconds[/green]")
    
    return parallel_time, results

async def test_model_performance():
    """Test individual model performance."""
    console.print("\n[bold magenta]📊 Testing Individual Model Performance[/bold magenta]")
    
    orchestrator = get_orchestrator()
    available_models = orchestrator.get_available_models()
    
    # Test each model with a simple task
    test_prompt = "Write a simple 'Hello World' function in JavaScript"
    
    model_results = []
    
    for model in available_models[:5]:  # Test first 5 models
        console.print(f"[dim]Testing {model}...[/dim]")
        
        start_time = time.time()
        result = await orchestrator.execute_task(
            TaskType.CODING,
            test_prompt,
            "simple"
        )
        response_time = time.time() - start_time
        
        model_results.append({
            'model': model,
            'response_time': response_time,
            'quality_score': result.quality_score,
            'success': result.success
        })
    
    # Display results
    table = Table(title="Model Performance Results")
    table.add_column("Model", style="cyan")
    table.add_column("Response Time", style="yellow")
    table.add_column("Quality Score", style="green")
    table.add_column("Success", style="blue")
    
    for result in model_results:
        table.add_row(
            result['model'],
            f"{result['response_time']:.2f}s",
            f"{result['quality_score']:.2f}",
            "✅" if result['success'] else "❌"
        )
    
    console.print(table)
    return model_results

async def test_orchestrator_features():
    """Test orchestrator features."""
    console.print("\n[bold cyan]🔧 Testing Orchestrator Features[/bold cyan]")
    
    orchestrator = get_orchestrator()
    
    # Test model recommendations
    console.print("[blue]Getting model recommendations...[/blue]")
    recommendations = orchestrator.get_model_recommendations()
    
    for task_type, models in recommendations.items():
        if models:
            console.print(f"  {task_type.value}: {', '.join(models[:3])}")
    
    # Test performance report
    console.print("\n[blue]Generating performance report...[/blue]")
    report = orchestrator.get_performance_report()
    
    console.print(f"  Total tasks: {report['overall']['total_tasks']}")
    console.print(f"  Average response time: {report['overall']['average_response_time']:.2f}s")
    console.print(f"  Average quality score: {report['overall']['average_quality_score']:.2f}")

async def main():
    """Main test function."""
    console.print(Panel(
        "🚀 Multi-Model Orchestration Test\n\n"
        "Testing 2-3x speed improvement using multiple Ollama models simultaneously",
        title="AI Development Team Orchestrator",
        border_style="bold blue"
    ))
    
    try:
        # Test sequential execution
        sequential_time, sequential_results = await test_sequential_execution()
        
        # Test parallel execution
        parallel_time, parallel_results = await test_parallel_execution()
        
        # Calculate speed improvement
        speed_improvement = sequential_time / parallel_time if parallel_time > 0 else 0
        
        console.print("\n[bold green]📈 Performance Comparison[/bold green]")
        
        comparison_table = Table(title="Speed Improvement Results")
        comparison_table.add_column("Metric", style="cyan")
        comparison_table.add_column("Value", style="yellow")
        
        comparison_table.add_row("Sequential Time", f"{sequential_time:.2f}s")
        comparison_table.add_row("Parallel Time", f"{parallel_time:.2f}s")
        comparison_table.add_row("Speed Improvement", f"{speed_improvement:.1f}x")
        comparison_table.add_row("Time Saved", f"{sequential_time - parallel_time:.2f}s")
        
        console.print(comparison_table)
        
        if speed_improvement >= 2.0:
            console.print(f"\n[bold green]🎉 Success! Achieved {speed_improvement:.1f}x speed improvement![/bold green]")
        else:
            console.print(f"\n[yellow]⚠️ Speed improvement: {speed_improvement:.1f}x (target: 2-3x)[/yellow]")
        
        # Test individual model performance
        await test_model_performance()
        
        # Test orchestrator features
        await test_orchestrator_features()
        
        # Display results summary
        console.print("\n[bold green]✅ Multi-Model Orchestration Test Completed![/bold green]")
        
        # Show parallel results
        console.print("\n[bold blue]📋 Parallel Execution Results:[/bold blue]")
        for i, result in enumerate(parallel_results, 1):
            if result.success:
                console.print(f"  {i}. {result.task_type.value} ({result.model_name}): {result.response_time:.2f}s")
            else:
                console.print(f"  {i}. {result.task_type.value}: Failed - {result.error}")
        
    except Exception as e:
        console.print(f"\n[red]❌ Test failed: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main()) 