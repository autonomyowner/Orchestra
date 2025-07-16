#!/usr/bin/env python3
"""
OpenRouter Client for +++A Project Builder 2030
- Multi-model support with intelligent selection
- Automatic fallbacks for reliability
- Cost optimization features
- Model-specific task optimization
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import openai
from rich.console import Console
from rich.panel import Panel
import time

console = Console()

@dataclass
class ModelConfig:
    """Configuration for different models"""
    name: str
    cost_per_1k_tokens: float
    max_tokens: int
    best_for: List[str]
    reliability_score: float

class OpenRouterClient:
    """Advanced OpenRouter client with model management"""
    
    def __init__(self):
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OpenRouter API key not found. Please set OPENAI_API_KEY environment variable.")
        
        self.client = openai.OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        
        # Model configurations with costs and capabilities
        self.models = {
            "anthropic/claude-3.5-sonnet": ModelConfig(
                name="Claude 3.5 Sonnet",
                cost_per_1k_tokens=0.003,
                max_tokens=200000,
                best_for=["planning", "architecture", "backend", "deployment"],
                reliability_score=0.95
            ),
            "openai/gpt-4o": ModelConfig(
                name="GPT-4 Omni",
                cost_per_1k_tokens=0.005,
                max_tokens=128000,
                best_for=["frontend", "database", "testing", "general"],
                reliability_score=0.90
            ),
            "google/gemini-pro": ModelConfig(
                name="Gemini Pro",
                cost_per_1k_tokens=0.001,
                max_tokens=1000000,
                best_for=["simple_tasks", "documentation", "cost_optimization"],
                reliability_score=0.85
            ),
            "meta-llama/llama-3.1-8b-instruct": ModelConfig(
                name="Llama 3.1 8B",
                cost_per_1k_tokens=0.0002,
                max_tokens=8192,
                best_for=["very_simple_tasks", "prototyping"],
                reliability_score=0.80
            )
        }
        
        # Task to model mapping
        self.task_model_mapping = {
            "architecture": "anthropic/claude-3.5-sonnet",
            "planning": "anthropic/claude-3.5-sonnet",
            "frontend": "openai/gpt-4o",
            "backend": "anthropic/claude-3.5-sonnet",
            "database": "openai/gpt-4o",
            "deployment": "anthropic/claude-3.5-sonnet",
            "testing": "openai/gpt-4o",
            "documentation": "google/gemini-pro",
            "simple": "google/gemini-pro",
            "prototype": "meta-llama/llama-3.1-8b-instruct"
        }
        
        self.fallback_models = [
            "openai/gpt-4o",
            "anthropic/claude-3.5-sonnet", 
            "google/gemini-pro"
        ]
        
        self.request_history = []
        self.total_cost = 0.0
    
    def get_optimal_model(self, task_type: str, complexity: str = "medium") -> str:
        """Select the best model for a given task and complexity"""
        
        # For simple tasks, use cheaper models if enabled
        if complexity == "simple" and os.getenv("USE_CHEAPER_MODELS_FOR_SIMPLE_TASKS", "true").lower() == "true":
            return "google/gemini-pro"
        
        # Get the recommended model for this task type
        recommended_model = self.task_model_mapping.get(task_type, "openai/gpt-4o")
        
        # Check if model is available and reliable
        if recommended_model in self.models:
            return recommended_model
        
        # Fallback to GPT-4o if recommended model not available
        return "openai/gpt-4o"
    
    async def generate_with_fallback(self, 
                                   prompt: str, 
                                   task_type: str = "general",
                                   complexity: str = "medium",
                                   max_retries: int = 3) -> Tuple[str, str, float]:
        """Generate response with automatic fallback to other models"""
        
        selected_model = self.get_optimal_model(task_type, complexity)
        models_to_try = [selected_model] + [m for m in self.fallback_models if m != selected_model]
        
        for attempt, model in enumerate(models_to_try[:max_retries]):
            try:
                console.print(f"🤖 Using model: {self.models[model].name} (Attempt {attempt + 1})", style="blue")
                
                start_time = time.time()
                
                response = await asyncio.to_thread(
                    self.client.chat.completions.create,
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=int(os.getenv("MAX_TOKENS_PER_REQUEST", "4000")),
                    temperature=0.7
                )
                
                end_time = time.time()
                response_time = end_time - start_time
                
                content = response.choices[0].message.content
                if content is None:
                    raise Exception("Empty response from model")
                tokens_used = response.usage.total_tokens if response.usage else 0
                
                # Calculate cost
                model_config = self.models[model]
                cost = (tokens_used / 1000) * model_config.cost_per_1k_tokens
                self.total_cost += cost
                
                # Log request
                self.request_history.append({
                    "model": model,
                    "task_type": task_type,
                    "tokens_used": tokens_used,
                    "cost": cost,
                    "response_time": response_time,
                    "success": True
                })
                
                console.print(f"✅ Success! Cost: ${cost:.4f}, Tokens: {tokens_used}, Time: {response_time:.2f}s", style="green")
                
                return content, model, cost
                
            except Exception as e:
                console.print(f"❌ Failed with {self.models[model].name}: {str(e)}", style="red")
                
                # Log failed request
                self.request_history.append({
                    "model": model,
                    "task_type": task_type,
                    "error": str(e),
                    "success": False
                })
                
                if attempt == max_retries - 1:
                    raise Exception(f"All models failed after {max_retries} attempts. Last error: {str(e)}")
                
                # Wait before retrying
                await asyncio.sleep(1)
        
        raise Exception("Unexpected error in fallback system")
    
    def get_cost_summary(self) -> Dict[str, Any]:
        """Get detailed cost and usage summary"""
        total_requests = len(self.request_history)
        successful_requests = len([r for r in self.request_history if r.get("success", False)])
        
        model_usage = {}
        for request in self.request_history:
            model = request.get("model", "unknown")
            if model not in model_usage:
                model_usage[model] = {"requests": 0, "cost": 0, "tokens": 0}
            
            model_usage[model]["requests"] += 1
            if request.get("success", False):
                model_usage[model]["cost"] += request.get("cost", 0)
                model_usage[model]["tokens"] += request.get("tokens_used", 0)
        
        return {
            "total_cost": self.total_cost,
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "success_rate": (successful_requests / total_requests * 100) if total_requests > 0 else 0,
            "model_usage": model_usage,
            "average_cost_per_request": self.total_cost / successful_requests if successful_requests > 0 else 0
        }
    
    def print_cost_summary(self):
        """Display cost summary in a nice format"""
        summary = self.get_cost_summary()
        
        console.print(Panel(
            f"[bold blue]💰 OpenRouter Cost Summary[/bold blue]\n\n"
            f"Total Cost: [green]${summary['total_cost']:.4f}[/green]\n"
            f"Total Requests: [yellow]{summary['total_requests']}[/yellow]\n"
            f"Success Rate: [green]{summary['success_rate']:.1f}%[/green]\n"
            f"Avg Cost/Request: [yellow]${summary['average_cost_per_request']:.4f}[/yellow]\n\n"
            f"[bold]Model Usage:[/bold]\n" + 
            "\n".join([
                f"• {self.models[model].name}: {usage['requests']} reqs, ${usage['cost']:.4f}, {usage['tokens']} tokens"
                for model, usage in summary['model_usage'].items()
            ]),
            title="OpenRouter Analytics",
            border_style="blue"
        ))

# Convenience function for easy usage
async def generate_ai_response(prompt: str, task_type: str = "general", complexity: str = "medium") -> str:
    """Simple function to generate AI response using OpenRouter"""
    client = OpenRouterClient()
    response, model, cost = await client.generate_with_fallback(prompt, task_type, complexity)
    return response 