#!/usr/bin/env python3
"""
Multi-Model Orchestration System
Dramatically improves AI Development Team Orchestrator performance by using multiple models simultaneously.
"""

import asyncio
import concurrent.futures
import time
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import threading
from queue import Queue

from utils.ollama_client import OllamaClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskType(Enum):
    """Different types of AI tasks."""
    PLANNING = "planning"
    CODING = "coding"
    REVIEW = "review"
    TESTING = "testing"
    DEBUGGING = "debugging"
    DOCUMENTATION = "documentation"
    DEPLOYMENT = "deployment"

class ModelTier(Enum):
    """Model performance tiers."""
    FAST = "fast"      # 7B models - quick responses
    BALANCED = "balanced"  # 13B models - good balance
    POWERFUL = "powerful"  # 33B+ models - best quality

@dataclass
class ModelConfig:
    """Configuration for a specific model."""
    name: str
    task_types: List[TaskType]
    tier: ModelTier
    max_tokens: int
    temperature: float
    priority: int  # Higher = more preferred
    concurrent_limit: int = 1

@dataclass
class TaskResult:
    """Result from a model task."""
    task_id: str
    model_name: str
    task_type: TaskType
    result: str
    quality_score: float
    response_time: float
    tokens_used: int
    success: bool
    error: Optional[str] = None

class ModelOrchestrator:
    """
    Multi-Model Orchestration System
    Manages multiple Ollama models for optimal performance.
    """
    
    def __init__(self):
        self.ollama_client = OllamaClient()
        self.model_configs = self._initialize_model_configs()
        self.performance_metrics = {}
        self.active_tasks = {}
        self.model_queues = {}
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        self.lock = threading.Lock()
        
        # Initialize model queues
        for model_name in self.model_configs.keys():
            self.model_queues[model_name] = Queue()
    
    def _initialize_model_configs(self) -> Dict[str, ModelConfig]:
        """Initialize model configurations for available Ollama models."""
        return {
            # Fast models (7B) - Quick responses
            "llama2:7b-chat": ModelConfig(
                name="llama2:7b-chat",
                task_types=[TaskType.PLANNING, TaskType.TESTING, TaskType.DOCUMENTATION],
                tier=ModelTier.FAST,
                max_tokens=4096,
                temperature=0.7,
                priority=3,
                concurrent_limit=3
            ),
            
            "mistral:7b-instruct": ModelConfig(
                name="mistral:7b-instruct",
                task_types=[TaskType.PLANNING, TaskType.TESTING, TaskType.DOCUMENTATION],
                tier=ModelTier.FAST,
                max_tokens=4096,
                temperature=0.7,
                priority=4,
                concurrent_limit=3
            ),
            
            # Balanced models (13B) - Good balance
            "llama2:13b-chat": ModelConfig(
                name="llama2:13b-chat",
                task_types=[TaskType.PLANNING, TaskType.REVIEW, TaskType.DOCUMENTATION],
                tier=ModelTier.BALANCED,
                max_tokens=4096,
                temperature=0.7,
                priority=5,
                concurrent_limit=2
            ),
            
            "codellama:13b-instruct": ModelConfig(
                name="codellama:13b-instruct",
                task_types=[TaskType.CODING, TaskType.REVIEW, TaskType.DEBUGGING],
                tier=ModelTier.BALANCED,
                max_tokens=4096,
                temperature=0.3,
                priority=6,
                concurrent_limit=2
            ),
            
            # Powerful models (33B+) - Best quality
            "deepseek-coder:33b": ModelConfig(
                name="deepseek-coder:33b",
                task_types=[TaskType.CODING, TaskType.REVIEW, TaskType.DEBUGGING],
                tier=ModelTier.POWERFUL,
                max_tokens=8192,
                temperature=0.2,
                priority=8,
                concurrent_limit=1
            ),
            
            "codellama:34b-instruct": ModelConfig(
                name="codellama:34b-instruct",
                task_types=[TaskType.CODING, TaskType.REVIEW, TaskType.DEBUGGING],
                tier=ModelTier.POWERFUL,
                max_tokens=8192,
                temperature=0.2,
                priority=7,
                concurrent_limit=1
            ),
            
            "wizardcoder:34b": ModelConfig(
                name="wizardcoder:34b",
                task_types=[TaskType.CODING, TaskType.REVIEW, TaskType.DEBUGGING],
                tier=ModelTier.POWERFUL,
                max_tokens=8192,
                temperature=0.2,
                priority=9,
                concurrent_limit=1
            ),
            
            # Specialized models
            "llama2:7b": ModelConfig(
                name="llama2:7b",
                task_types=[TaskType.PLANNING, TaskType.TESTING],
                tier=ModelTier.FAST,
                max_tokens=4096,
                temperature=0.7,
                priority=2,
                concurrent_limit=3
            ),
            
            "neural-chat:7b": ModelConfig(
                name="neural-chat:7b",
                task_types=[TaskType.PLANNING, TaskType.DOCUMENTATION],
                tier=ModelTier.FAST,
                max_tokens=4096,
                temperature=0.7,
                priority=3,
                concurrent_limit=3
            )
        }
    
    def get_available_models(self) -> List[str]:
        """Get list of available models on the system."""
        try:
            models = self.ollama_client.list_models()
            available_models = []
            
            for model in models:
                model_name = model.get('name', '')
                if model_name in self.model_configs:
                    available_models.append(model_name)
                else:
                    # Add unknown models with default config
                    self.model_configs[model_name] = ModelConfig(
                        name=model_name,
                        task_types=[TaskType.PLANNING, TaskType.CODING, TaskType.REVIEW],
                        tier=ModelTier.BALANCED,
                        max_tokens=4096,
                        temperature=0.7,
                        priority=5,
                        concurrent_limit=2
                    )
                    available_models.append(model_name)
            
            logger.info(f"Available models: {available_models}")
            return available_models
            
        except Exception as e:
            logger.error(f"Error getting available models: {e}")
            return []
    
    def get_optimal_model(self, task_type: TaskType, complexity: str = "medium") -> Optional[str]:
        """Get the optimal model for a specific task and complexity."""
        available_models = self.get_available_models()
        
        # Filter models by task type
        suitable_models = [
            model_name for model_name, config in self.model_configs.items()
            if model_name in available_models and task_type in config.task_types
        ]
        
        if not suitable_models:
            logger.warning(f"No suitable models found for task type: {task_type}")
            return None
        
        # Select model based on complexity and availability
        if complexity == "simple":
            # Use fast models for simple tasks
            fast_models = [
                model for model in suitable_models
                if self.model_configs[model].tier == ModelTier.FAST
            ]
            if fast_models:
                return self._select_best_model(fast_models)
        
        elif complexity == "complex":
            # Use powerful models for complex tasks
            powerful_models = [
                model for model in suitable_models
                if self.model_configs[model].tier == ModelTier.POWERFUL
            ]
            if powerful_models:
                return self._select_best_model(powerful_models)
        
        # Default to best available model
        return self._select_best_model(suitable_models)
    
    def _select_best_model(self, models: List[str]) -> str:
        """Select the best model based on priority and current load."""
        if not models:
            return None
        
        # Sort by priority (higher is better)
        sorted_models = sorted(
            models,
            key=lambda m: self.model_configs[m].priority,
            reverse=True
        )
        
        # Check current load and select least loaded model
        for model in sorted_models:
            current_load = self._get_model_current_load(model)
            max_load = self.model_configs[model].concurrent_limit
            
            if current_load < max_load:
                return model
        
        # If all models are at capacity, return the highest priority one
        return sorted_models[0]
    
    def _get_model_current_load(self, model_name: str) -> int:
        """Get current load (active tasks) for a model."""
        with self.lock:
            return len([task for task in self.active_tasks.values() if task.get('model') == model_name])
    
    async def execute_task(self, task_type: TaskType, prompt: str, complexity: str = "medium", 
                          task_id: Optional[str] = None) -> TaskResult:
        """Execute a task using the optimal model."""
        if task_id is None:
            task_id = f"{task_type.value}_{int(time.time())}"
        
        # Get optimal model
        model_name = self.get_optimal_model(task_type, complexity)
        if not model_name:
            return TaskResult(
                task_id=task_id,
                model_name="none",
                task_type=task_type,
                result="",
                quality_score=0.0,
                response_time=0.0,
                tokens_used=0,
                success=False,
                error="No suitable model available"
            )
        
        # Mark task as active
        with self.lock:
            self.active_tasks[task_id] = {
                'model': model_name,
                'task_type': task_type,
                'start_time': time.time()
            }
        
        try:
            # Execute task
            start_time = time.time()
            result = await self._execute_with_model(model_name, prompt, task_type)
            response_time = time.time() - start_time
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(result, task_type, response_time)
            
            # Update performance metrics
            self._update_performance_metrics(model_name, task_type, response_time, quality_score)
            
            return TaskResult(
                task_id=task_id,
                model_name=model_name,
                task_type=task_type,
                result=result,
                quality_score=quality_score,
                response_time=response_time,
                tokens_used=len(result.split()),  # Approximate
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error executing task {task_id}: {e}")
            return TaskResult(
                task_id=task_id,
                model_name=model_name,
                task_type=task_type,
                result="",
                quality_score=0.0,
                response_time=time.time() - start_time,
                tokens_used=0,
                success=False,
                error=str(e)
            )
        finally:
            # Remove task from active tasks
            with self.lock:
                self.active_tasks.pop(task_id, None)
    
    async def _execute_with_model(self, model_name: str, prompt: str, task_type: TaskType) -> str:
        """Execute a task with a specific model."""
        config = self.model_configs[model_name]
        
        # Prepare prompt based on task type
        enhanced_prompt = self._enhance_prompt_for_task(prompt, task_type, config)
        
        # Execute with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    self.ollama_client.generate_response,
                    model_name,
                    enhanced_prompt,
                    config.max_tokens,
                    config.temperature
                )
                return response
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                logger.warning(f"Attempt {attempt + 1} failed for {model_name}: {e}")
                await asyncio.sleep(1)
    
    def _enhance_prompt_for_task(self, prompt: str, task_type: TaskType, config: ModelConfig) -> str:
        """Enhance prompt based on task type and model configuration."""
        task_instructions = {
            TaskType.PLANNING: "You are a Product Manager. Create a detailed technical specification.",
            TaskType.CODING: "You are a Senior Full-Stack Developer. Write production-ready code.",
            TaskType.REVIEW: "You are a Lead Engineer. Review code for quality and security.",
            TaskType.TESTING: "You are a QA Engineer. Create comprehensive tests.",
            TaskType.DEBUGGING: "You are a Senior Debugger. Find and fix issues.",
            TaskType.DOCUMENTATION: "You are a Technical Writer. Create clear documentation.",
            TaskType.DEPLOYMENT: "You are a DevOps Engineer. Set up deployment configurations."
        }
        
        instruction = task_instructions.get(task_type, "")
        return f"{instruction}\n\n{prompt}"
    
    def _calculate_quality_score(self, result: str, task_type: TaskType, response_time: float) -> float:
        """Calculate quality score based on result and task type."""
        base_score = 0.5
        
        # Length factor (longer responses often better)
        length_factor = min(len(result) / 1000, 1.0) * 0.2
        
        # Speed factor (faster is better, but not too fast)
        speed_factor = max(0, (5.0 - response_time) / 5.0) * 0.1
        
        # Task-specific factors
        task_factors = {
            TaskType.CODING: self._calculate_code_quality(result),
            TaskType.REVIEW: self._calculate_review_quality(result),
            TaskType.PLANNING: self._calculate_planning_quality(result),
            TaskType.TESTING: self._calculate_testing_quality(result),
            TaskType.DOCUMENTATION: self._calculate_documentation_quality(result)
        }
        
        task_factor = task_factors.get(task_type, 0.2)
        
        return min(base_score + length_factor + speed_factor + task_factor, 1.0)
    
    def _calculate_code_quality(self, result: str) -> float:
        """Calculate code quality score."""
        score = 0.0
        
        # Check for code blocks
        if "```" in result:
            score += 0.2
        
        # Check for proper syntax
        if any(keyword in result.lower() for keyword in ["function", "class", "import", "export"]):
            score += 0.2
        
        # Check for comments
        if "//" in result or "#" in result:
            score += 0.1
        
        return score
    
    def _calculate_review_quality(self, result: str) -> float:
        """Calculate review quality score."""
        score = 0.0
        
        # Check for review indicators
        review_keywords = ["security", "performance", "best practice", "improvement", "issue"]
        for keyword in review_keywords:
            if keyword.lower() in result.lower():
                score += 0.1
        
        return min(score, 0.3)
    
    def _calculate_planning_quality(self, result: str) -> float:
        """Calculate planning quality score."""
        score = 0.0
        
        # Check for planning indicators
        planning_keywords = ["architecture", "structure", "components", "database", "api"]
        for keyword in planning_keywords:
            if keyword.lower() in result.lower():
                score += 0.1
        
        return min(score, 0.3)
    
    def _calculate_testing_quality(self, result: str) -> float:
        """Calculate testing quality score."""
        score = 0.0
        
        # Check for testing indicators
        testing_keywords = ["test", "assert", "expect", "coverage", "scenario"]
        for keyword in testing_keywords:
            if keyword.lower() in result.lower():
                score += 0.1
        
        return min(score, 0.3)
    
    def _calculate_documentation_quality(self, result: str) -> float:
        """Calculate documentation quality score."""
        score = 0.0
        
        # Check for documentation indicators
        doc_keywords = ["usage", "example", "parameter", "return", "description"]
        for keyword in doc_keywords:
            if keyword.lower() in result.lower():
                score += 0.1
        
        return min(score, 0.3)
    
    def _update_performance_metrics(self, model_name: str, task_type: TaskType, 
                                  response_time: float, quality_score: float):
        """Update performance metrics for a model."""
        with self.lock:
            if model_name not in self.performance_metrics:
                self.performance_metrics[model_name] = {}
            
            if task_type.value not in self.performance_metrics[model_name]:
                self.performance_metrics[model_name][task_type.value] = {
                    'response_times': [],
                    'quality_scores': [],
                    'total_tasks': 0
                }
            
            metrics = self.performance_metrics[model_name][task_type.value]
            metrics['response_times'].append(response_time)
            metrics['quality_scores'].append(quality_score)
            metrics['total_tasks'] += 1
    
    async def execute_parallel_tasks(self, tasks: List[Tuple[TaskType, str, str]]) -> List[TaskResult]:
        """Execute multiple tasks in parallel for maximum speed."""
        # Create tasks
        task_futures = []
        for i, (task_type, prompt, complexity) in enumerate(tasks):
            task_id = f"parallel_{i}_{int(time.time())}"
            future = self.execute_task(task_type, prompt, complexity, task_id)
            task_futures.append(future)
        
        # Execute all tasks in parallel
        results = await asyncio.gather(*task_futures, return_exceptions=True)
        
        # Convert exceptions to failed results
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                task_type, prompt, complexity = tasks[i]
                final_results.append(TaskResult(
                    task_id=f"parallel_{i}_{int(time.time())}",
                    model_name="none",
                    task_type=task_type,
                    result="",
                    quality_score=0.0,
                    response_time=0.0,
                    tokens_used=0,
                    success=False,
                    error=str(result)
                ))
            else:
                final_results.append(result)
        
        return final_results
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report."""
        with self.lock:
            report = {
                'models': {},
                'task_types': {},
                'overall': {
                    'total_tasks': 0,
                    'average_response_time': 0.0,
                    'average_quality_score': 0.0
                }
            }
            
            total_tasks = 0
            total_response_time = 0.0
            total_quality_score = 0.0
            
            for model_name, model_metrics in self.performance_metrics.items():
                report['models'][model_name] = {
                    'task_types': {},
                    'total_tasks': 0,
                    'average_response_time': 0.0,
                    'average_quality_score': 0.0
                }
                
                model_total_tasks = 0
                model_total_response_time = 0.0
                model_total_quality_score = 0.0
                
                for task_type, metrics in model_metrics.items():
                    if metrics['total_tasks'] > 0:
                        avg_response_time = sum(metrics['response_times']) / len(metrics['response_times'])
                        avg_quality_score = sum(metrics['quality_scores']) / len(metrics['quality_scores'])
                        
                        report['models'][model_name]['task_types'][task_type] = {
                            'total_tasks': metrics['total_tasks'],
                            'average_response_time': avg_response_time,
                            'average_quality_score': avg_quality_score
                        }
                        
                        model_total_tasks += metrics['total_tasks']
                        model_total_response_time += sum(metrics['response_times'])
                        model_total_quality_score += sum(metrics['quality_scores'])
                        
                        total_tasks += metrics['total_tasks']
                        total_response_time += sum(metrics['response_times'])
                        total_quality_score += sum(metrics['quality_scores'])
                
                if model_total_tasks > 0:
                    report['models'][model_name]['total_tasks'] = model_total_tasks
                    report['models'][model_name]['average_response_time'] = model_total_response_time / model_total_tasks
                    report['models'][model_name]['average_quality_score'] = model_total_quality_score / model_total_tasks
            
            if total_tasks > 0:
                report['overall']['total_tasks'] = total_tasks
                report['overall']['average_response_time'] = total_response_time / total_tasks
                report['overall']['average_quality_score'] = total_quality_score / total_tasks
            
            return report
    
    def get_model_recommendations(self) -> Dict[TaskType, List[str]]:
        """Get model recommendations based on performance."""
        recommendations = {}
        
        for task_type in TaskType:
            best_models = []
            
            for model_name, model_metrics in self.performance_metrics.items():
                if task_type.value in model_metrics:
                    metrics = model_metrics[task_type.value]
                    if metrics['total_tasks'] >= 3:  # Minimum tasks for reliable recommendation
                        avg_quality = sum(metrics['quality_scores']) / len(metrics['quality_scores'])
                        avg_speed = sum(metrics['response_times']) / len(metrics['response_times'])
                        
                        # Calculate efficiency score (quality / time)
                        efficiency = avg_quality / max(avg_speed, 0.1)
                        
                        best_models.append((model_name, efficiency))
            
            # Sort by efficiency and return top 3
            best_models.sort(key=lambda x: x[1], reverse=True)
            recommendations[task_type] = [model for model, _ in best_models[:3]]
        
        return recommendations
    
    def cleanup(self):
        """Cleanup resources."""
        self.executor.shutdown(wait=True)


# Global orchestrator instance
orchestrator = ModelOrchestrator()


def get_orchestrator() -> ModelOrchestrator:
    """Get the global orchestrator instance."""
    return orchestrator


async def demo_orchestrator():
    """Demo the multi-model orchestration system."""
    print("🚀 Multi-Model Orchestration Demo")
    print("=" * 50)
    
    # Get available models
    available_models = orchestrator.get_available_models()
    print(f"📋 Available models: {len(available_models)}")
    for model in available_models:
        config = orchestrator.model_configs[model]
        print(f"  • {model} ({config.tier.value}) - {', '.join([t.value for t in config.task_types])}")
    
    print("\n🎯 Testing parallel task execution...")
    
    # Test parallel tasks
    tasks = [
        (TaskType.PLANNING, "Create a technical specification for a SaaS platform", "medium"),
        (TaskType.CODING, "Write a React component for user authentication", "simple"),
        (TaskType.REVIEW, "Review this code for security issues: console.log(password)", "simple"),
        (TaskType.DOCUMENTATION, "Write API documentation for user endpoints", "simple")
    ]
    
    start_time = time.time()
    results = await orchestrator.execute_parallel_tasks(tasks)
    total_time = time.time() - start_time
    
    print(f"\n⏱️ Total execution time: {total_time:.2f} seconds")
    print(f"🚀 Speed improvement: {len(tasks) * 5 / total_time:.1f}x faster than sequential")
    
    print("\n📊 Results:")
    for i, result in enumerate(results):
        print(f"  Task {i+1} ({result.task_type.value}):")
        print(f"    Model: {result.model_name}")
        print(f"    Time: {result.response_time:.2f}s")
        print(f"    Quality: {result.quality_score:.2f}")
        print(f"    Success: {result.success}")
        if result.error:
            print(f"    Error: {result.error}")
        print()
    
    # Performance report
    report = orchestrator.get_performance_report()
    print("📈 Performance Report:")
    print(f"  Total tasks: {report['overall']['total_tasks']}")
    print(f"  Average response time: {report['overall']['average_response_time']:.2f}s")
    print(f"  Average quality score: {report['overall']['average_quality_score']:.2f}")
    
    # Model recommendations
    recommendations = orchestrator.get_model_recommendations()
    print("\n🎯 Model Recommendations:")
    for task_type, models in recommendations.items():
        if models:
            print(f"  {task_type.value}: {', '.join(models)}")


if __name__ == "__main__":
    # Run demo
    asyncio.run(demo_orchestrator()) 