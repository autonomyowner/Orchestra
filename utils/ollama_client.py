import requests
import json
import time
from typing import Optional, Dict, Any
from rich.console import Console

console = Console()

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
    
    def is_model_available(self, model_name: str) -> bool:
        """Check if a model is available locally."""
        try:
            response = requests.get(f"{self.api_url}/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return any(model["name"].startswith(model_name) for model in models)
            return False
        except requests.exceptions.RequestException:
            return False
    
    def pull_model(self, model_name: str) -> bool:
        """Pull a model from the Ollama registry."""
        try:
            console.print(f"[yellow]Pulling model {model_name}...[/yellow]")
            response = requests.post(
                f"{self.api_url}/pull",
                json={"name": model_name},
                stream=True,
                timeout=600  # 10 minute timeout for model downloads
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line.decode('utf-8'))
                        if "status" in data:
                            console.print(f"[blue]{data['status']}[/blue]")
                return True
            return False
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error pulling model: {e}[/red]")
            return False
    
    def generate(self, model: str, prompt: str, system: Optional[str] = None, 
                 temperature: float = 0.7, max_tokens: Optional[int] = None) -> Optional[str]:
        """Generate a response using the specified model with improved error handling."""
        try:
            # Adjust max_tokens based on model capabilities
            if max_tokens and max_tokens > 8000:
                console.print(f"[yellow]Warning: Large token count ({max_tokens}) may cause timeouts. Using 8000.[/yellow]")
                max_tokens = 8000
            
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "top_p": 0.9,
                    "top_k": 40,
                    "repeat_penalty": 1.1
                }
            }
            
            if system:
                payload["system"] = system
            
            if max_tokens:
                payload["options"]["num_ctx"] = max_tokens
            
            console.print(f"[dim]Generating response with {model} (temp: {temperature}, tokens: {max_tokens or 'default'})[/dim]")
            
            # Try with shorter timeout first, then longer if needed
            timeouts = [120, 300, 600]  # 2min, 5min, 10min
            
            for timeout in timeouts:
                try:
                    response = requests.post(
                        f"{self.api_url}/generate",
                        json=payload,
                        timeout=timeout
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        response_text = result.get("response", "")
                        
                        if response_text.strip():
                            console.print(f"[green]✅ Generated {len(response_text)} characters[/green]")
                            return response_text
                        else:
                            console.print("[yellow]Warning: Empty response received[/yellow]")
                            continue
                    else:
                        console.print(f"[red]Error: {response.status_code} - {response.text}[/red]")
                        continue
                        
                except requests.exceptions.Timeout:
                    console.print(f"[yellow]Timeout after {timeout}s, trying longer timeout...[/yellow]")
                    continue
                except requests.exceptions.RequestException as e:
                    console.print(f"[red]Request failed: {e}[/red]")
                    break
            
            console.print("[red]All generation attempts failed[/red]")
            return None
                
        except Exception as e:
            console.print(f"[red]Unexpected error in generate: {e}[/red]")
            return None
    
    def generate_response(self, model: str, prompt: str, max_tokens: Optional[int] = None, 
                         temperature: float = 0.7) -> str:
        """Generate response for orchestrator (synchronous version)."""
        result = self.generate(model, prompt, temperature=temperature, max_tokens=max_tokens)
        return result if result else ""
    
    def list_models(self) -> list:
        """List all available models."""
        try:
            response = requests.get(f"{self.api_url}/tags", timeout=10)
            if response.status_code == 200:
                return response.json().get("models", [])
            return []
        except requests.exceptions.RequestException:
            return []
    
    def generate_chunked(self, model: str, prompt: str, system: Optional[str] = None, 
                        temperature: float = 0.7, chunk_size: int = 4000) -> Optional[str]:
        """Generate response in chunks for very large prompts."""
        try:
            console.print(f"[yellow]Using chunked generation for large prompt ({len(prompt)} chars)[/yellow]")
            
            # Split prompt into manageable chunks
            chunks = [prompt[i:i+chunk_size] for i in range(0, len(prompt), chunk_size)]
            
            full_response = ""
            
            for i, chunk in enumerate(chunks):
                console.print(f"[dim]Processing chunk {i+1}/{len(chunks)}[/dim]")
                
                chunk_response = self.generate(
                    model=model,
                    prompt=chunk,
                    system=system if i == 0 else None,  # Only include system prompt in first chunk
                    temperature=temperature,
                    max_tokens=4000
                )
                
                if chunk_response:
                    full_response += chunk_response + "\n"
                else:
                    console.print(f"[red]Failed to generate chunk {i+1}[/red]")
                    return None
            
            return full_response.strip()
            
        except Exception as e:
            console.print(f"[red]Error in chunked generation: {e}[/red]")
            return None
    
    def chat(self, model: str, messages: list, temperature: float = 0.7) -> Optional[str]:
        """Chat with a model using conversation format."""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "top_p": 0.9,
                    "top_k": 40,
                    "repeat_penalty": 1.1
                }
            }
            
            response = requests.post(
                f"{self.api_url}/chat",
                json=payload,
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("message", {}).get("content", "")
            else:
                console.print(f"[red]Error: {response.status_code} - {response.text}[/red]")
                return None
                
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Request failed: {e}[/red]")
            return None
    
    def test_model_response(self, model: str) -> bool:
        """Test if a model can generate a basic response."""
        try:
            test_prompt = "Generate a simple 'Hello World' response."
            response = self.generate(model, test_prompt, temperature=0.1, max_tokens=100)
            return response is not None and len(response.strip()) > 0
        except Exception as e:
            console.print(f"[red]Model test failed: {e}[/red]")
            return False
    
    def ensure_models_available(self, models: list) -> bool:
        """Ensure all required models are available, pull if necessary."""
        for model in models:
            if not self.is_model_available(model):
                console.print(f"[yellow]Model {model} not found locally. Pulling...[/yellow]")
                if not self.pull_model(model):
                    console.print(f"[red]Failed to pull model {model}[/red]")
                    return False
                console.print(f"[green]Successfully pulled {model}[/green]")
            else:
                console.print(f"[green]Model {model} is available[/green]")
                
                # Test model response
                console.print(f"[dim]Testing {model} response capability...[/dim]")
                if not self.test_model_response(model):
                    console.print(f"[yellow]Warning: {model} may not be responding properly[/yellow]")
                    console.print(f"[yellow]Consider re-pulling: ollama pull {model}[/yellow]")
        
        return True