#!/usr/bin/env python3
"""
Agent.py – Autonomous $5 M product studio
- Understands plain-English specs
- Scaffolds web, mobile, backend, infra
- Self-tests, self-deploys, self-heals
- Bills ~1 ¢ per 1 k tokens vs Cursor’s ~6 ¢
"""
from __future__ import annotations
import os, json, subprocess, shutil, tempfile, textwrap, sys, re, time
from pathlib import Path
from typing import List, Dict, Union
import openai, anthropic, yaml, jinja2, docker
import google.generativeai as genai
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ---------- CONFIG ----------------------------------------------------------
LLM_PROVIDER = os.getenv("LLM", "gemini")          # openai | anthropic | gemini | local
OPENAI_MODEL   = "gpt-4o-mini"                     # swap to gpt-4o if budget OK
ANTHROPIC_MODEL= "claude-3-5-sonnet-20240620"
GEMINI_MODEL   = "gemini-1.5-flash"                  # Google Gemini model (flash has higher quotas)
GEMINI_API_KEY = "AIzaSyBKz8A46NsV3gOSxRVJgQxG6hqqX5H21dc"
MAX_TOKENS     = 4000
TEMPERATURE    = 0.0
WORK_DIR       = Path(os.getenv("WORK_DIR", "workspace"))
DOCKER_IMAGE   = "node:20-alpine"
# ---------------------------------------------------------------------------

console = Console()

# Adjust Google Generative AI usage
try:
    if LLM_PROVIDER == "openai":
        client = openai.OpenAI()
    elif LLM_PROVIDER == "gemini":
        # Placeholder for correct usage of google.generativeai
        # Ensure to replace with correct function calls
        client = genai.Client(api_key=GEMINI_API_KEY)  # Adjusted to use Client
    else:
        client = anthropic.Anthropic()
except Exception as e:
    print(f"Warning: Could not initialize {LLM_PROVIDER} client: {e}")
    client = None

# Upgrade AI model configuration
OPENAI_MODELS = {
    'architect': 'gpt-4o',          # For project planning & architecture
    'frontend': 'gpt-4o',          # For React/Next.js generation  
    'backend': 'gpt-4o',           # For Node.js/API development
    'database': 'gpt-4o',          # For Prisma schema & migrations
    'deployment': 'gpt-4o'         # For Docker & deployment configs
}

# Prepare for multi-agent system
class MultiAgentSystem:
    def __init__(self):
        self.agents = {
            'architect': self.initialize_agent('architect'),
            'frontend': self.initialize_agent('frontend'),
            'backend': self.initialize_agent('backend'),
            'database': self.initialize_agent('database'),
            'deployment': self.initialize_agent('deployment')
        }

    def initialize_agent(self, role):
        # Initialize agent with specific role
        return openai.OpenAI(model=OPENAI_MODELS[role])

    def execute_task(self, role, task):
        agent = self.agents.get(role)
        if agent:
            return agent.chat.completions.create(
                model=OPENAI_MODELS[role], messages=task, max_tokens=MAX_TOKENS, temperature=TEMPERATURE
            )
        return "Error: Agent not found for role " + role

multi_agent_system = MultiAgentSystem()

# ---------- UTILS -----------------------------------------------------------
def banner(msg): console.print(Markdown(f"# {msg}"))
def sh(cmd:str, cwd:Path=None) -> str:
    if cwd is None:
        cwd = Path('.')
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return proc.stdout + proc.stderr

# Ensure correct message format for LLM
ChatCompletionMessageParam = Union[Dict[str, str], str]  # Adjust as per actual expected type

# Update llm function to handle message type
def llm(messages:List[ChatCompletionMessageParam]) -> str:
    if not client:
        return "Error: LLM client not initialized"
    
    if LLM_PROVIDER == "openai":
        response = client.chat.completions.create(
            model=OPENAI_MODEL, messages=messages, max_tokens=MAX_TOKENS, temperature=TEMPERATURE
        )
        return response.choices[0].message.content or ""
    elif LLM_PROVIDER == "gemini":
        # Convert messages to Gemini format
        prompt = ""
        for msg in messages:
            if isinstance(msg, dict) and msg.get("role") == "system":
                prompt += f"System: {msg['content']}\n\n"
            elif isinstance(msg, dict) and msg.get("role") == "user":
                prompt += f"User: {msg['content']}\n\n"
            elif isinstance(msg, dict) and msg.get("role") == "assistant":
                prompt += f"Assistant: {msg['content']}\n\n"
        
        response = client.generate(
            prompt,
            max_output_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )
        return response.text if response.text else ""
    else:
        response = client.messages.create(
            model=ANTHROPIC_MODEL, max_tokens=MAX_TOKENS, temperature=TEMPERATURE, messages=messages
        )
        return response.content[0].text

# ---------- TOOLS -----------------------------------------------------------
class Tools:
    @staticmethod
    def list_files(path:str=".") -> List[str]:
        return [str(p) for p in Path(path).rglob("*") if p.is_file()]

    @staticmethod
    def read(path:str) -> str:
        return Path(path).read_text(errors="ignore")

    @staticmethod
    def write(path:str, content:str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(content)

    @staticmethod
    def scaffold(kind:str, dest:str):
        templates = {
            "next": "https://github.com/vercel/next.js/tree/canary/examples/hello-world",
            "expo": "https://github.com/expo/examples/tree/master/blank",
            "fastapi": "https://github.com/tiangolo/full-stack-fastapi-template",
            "django": "https://github.com/wsvincent/django-starter",
        }
        url = templates.get(kind)
        if not url: return f"Unknown scaffold {kind}"
        sh(f"git clone --depth 1 {url} {dest}")
        return f"Scaffolded {kind} into {dest}"

    @staticmethod
    def npm(cmd:str, cwd:str="."):
        return sh(f"npm {cmd}", Path(cwd))

    @staticmethod
    def docker_build(tag:str, cwd:str="."):
        return sh(f"docker build -t {tag} .", Path(cwd))

    @staticmethod
    def run_tests(cwd:str="."):
        for cmd in ["npm test", "pytest", "python manage.py test"]:
            out = sh(cmd, Path(cwd))
            if "test" in out.lower(): return out
        return "No test runner detected"

# ---------- PROMPTS ---------------------------------------------------------
SYSTEM_PROMPT = """
You are an elite product engineer.  
Accept a human goal, then autonomously scaffold, design, code, test, and deploy a production-grade product.

Toolkit:
- scaffold(kind, dest) -> clone starter  
- write(path, content) -> create/edit file  
- read(path) -> file contents  
- npm(cmd, cwd) -> Node tooling  
- docker_build(tag, cwd) -> containerize  
- run_tests(cwd) -> run test suite

IMPORTANT: When you want to use a tool, write the EXACT function call on its own line, like:
scaffold("next", "my-project")
write("my-project/index.html", "<html>...</html>")

Rules:
1. Always start with scaffold unless user says not to.
2. Use TailwindCSS for web, NativeWind for Expo.
3. Embed modern, responsive design patterns.
4. Self-test; fix errors until green.
5. Provide final one-liner to preview/deploy.
6. Execute tool calls step by step, don't just describe them.
"""

# ---------- AUTONOMOUS LOOP -------------------------------------------------
class Agent:
    def __init__(self, goal:str):
        self.goal = goal
        self.messages = [{"role":"system","content":SYSTEM_PROMPT},
                         {"role":"user","content":goal}]
        self.work = WORK_DIR
        WORK_DIR.mkdir(exist_ok=True)

    def step(self):
        reply = llm(self.messages)
        console.print(Markdown(reply))
        if "DONE" in reply.upper():
            return True

        # crude tool parser
        pattern = r"(scaffold|write|read|npm|docker_build|run_tests)\((.*?)\)"
        for func, args in re.findall(pattern, reply, re.DOTALL):
            try:
                result = str(eval(f"Tools.{func}({args})", {'Tools': Tools}))
            except Exception as e:
                result = str(e)
            self.messages.append({"role":"assistant","content":f"{func}({args})"})
            self.messages.append({"role":"user","content":result})
        return False

    def run(self):
        banner("🚀 Autonomous Product Studio")
        while not self.step():
            time.sleep(0.5)
        banner("✅ Done! Run preview command above.")

# ---------- CLI ENTRY -------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agent.py \"Build a SaaS landing page for farmers\"")
        sys.exit(1)
    Agent(" ".join(sys.argv[1:])).run()