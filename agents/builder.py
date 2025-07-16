import json
import os
import shutil
from typing import Dict, Any, Optional, List
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, TaskID

from utils.ollama_client import OllamaClient

console = Console()

class BuilderAgent:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
        self.model = "deepseek-coder:33b"
        self.agent_name = "Builder (Full-Stack Developer)"
        
    def load_prompt(self) -> str:
        """Load the builder prompt from file."""
        try:
            with open("prompts/builder_prompt.txt", "r") as f:
                return f.read()
        except FileNotFoundError:
            console.print("[red]Error: builder_prompt.txt not found[/red]")
            return ""
    
    def create_project_structure(self, project_name: str, output_dir: str = "output") -> str:
        """Create the basic project structure."""
        project_path = os.path.join(output_dir, project_name)
        
        # Remove existing directory if it exists
        if os.path.exists(project_path):
            shutil.rmtree(project_path)
        
        # Create project directory
        os.makedirs(project_path, exist_ok=True)
        
        console.print(f"[green]✅ Created project directory: {project_path}[/green]")
        return project_path
    
    def generate_codebase(self, technical_spec: Dict[str, Any], project_path: str) -> bool:
        """Generate the complete codebase based on technical specifications."""
        console.print(Panel(
            f"🏗️ {self.agent_name} is building the application...",
            title="Development Phase",
            border_style="green"
        ))
        
        # Load system prompt
        system_prompt = self.load_prompt()
        if not system_prompt:
            return False
        
        # Create user prompt with technical specification
        user_prompt = f"""
Please implement a complete Next.js 14 web application based on the following technical specification:

TECHNICAL SPECIFICATION:
{json.dumps(technical_spec, indent=2)}

Requirements:
1. Create a production-ready Next.js 14 application with TypeScript
2. Use Tailwind CSS for styling
3. Implement Prisma for database management
4. Follow the app router pattern
5. Include all specified features and pages
6. Implement proper authentication if required
7. Create responsive, accessible components
8. Include proper error handling and loading states
9. Follow best practices for security and performance
10. Structure code following atomic design principles

IMPORTANT: You MUST provide the complete file structure and implementation. Include all necessary configuration files, components, pages, API routes, database schemas, and utilities.

CRITICAL: Your response MUST follow this exact format for each file:

FILE: path/to/file.ext
PURPOSE: Brief description of what this file does
---
[Complete file content]
---

Generate a production-ready codebase that can be deployed immediately. Do not skip any files or provide incomplete implementations.
        """
        
        console.print("[yellow]Generating complete application codebase...[/yellow]")
        console.print("[dim]This may take several minutes for complex applications...[/dim]")
        
        # Try multiple generation attempts with different settings
        for attempt in range(3):
            if attempt > 0:
                console.print(f"[yellow]Retry attempt {attempt + 1}/3...[/yellow]")
            
            # Adjust parameters for each attempt
            temperature = 0.1 + (attempt * 0.1)  # 0.1, 0.2, 0.3
            max_tokens = 8000 if attempt == 0 else 6000  # Reduce tokens on retries
            
            # Generate codebase using Ollama
            response = self.ollama_client.generate(
                model=self.model,
                prompt=user_prompt,
                system=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            if response and len(response.strip()) > 1000:  # Ensure substantial response
                console.print(f"[green]✅ Generated substantial response ({len(response)} chars)[/green]")
                
                # Parse and create files from response
                if self.parse_and_create_files(response, project_path):
                    return True
                else:
                    console.print(f"[yellow]Attempt {attempt + 1} failed to parse files, retrying...[/yellow]")
            else:
                console.print(f"[yellow]Attempt {attempt + 1} generated insufficient response, retrying...[/yellow]")
        
        # If all attempts fail, try chunked generation
        console.print("[yellow]Trying chunked generation as last resort...[/yellow]")
        chunked_response = self.ollama_client.generate_chunked(
            model=self.model,
            prompt=user_prompt,
            system=system_prompt,
            temperature=0.2,
            chunk_size=3000
        )
        
        if chunked_response and self.parse_and_create_files(chunked_response, project_path):
            return True
        
        console.print("[red]All generation attempts failed. Creating enhanced basic structure...[/red]")
        return self.create_enhanced_basic_structure(project_path, technical_spec)
    
    def parse_and_create_files(self, response: str, project_path: str) -> bool:
        """Parse the AI response and create the actual files with improved parsing."""
        try:
            console.print("[yellow]Parsing response and creating files...[/yellow]")
            
            # Try multiple parsing strategies
            parsing_strategies = [
                self._parse_file_markers,
                self._parse_code_blocks,
                self._parse_markdown_blocks,
                self._parse_manual_extraction
            ]
            
            for i, strategy in enumerate(parsing_strategies):
                console.print(f"[dim]Trying parsing strategy {i+1}/{len(parsing_strategies)}[/dim]")
                
                files_created = strategy(response, project_path)
                
                if files_created > 5:  # Require at least 5 files for success
                    console.print(f"[green]✅ Strategy {i+1} created {files_created} files[/green]")
                    return True
                else:
                    console.print(f"[yellow]Strategy {i+1} only created {files_created} files, trying next...[/yellow]")
            
            console.print("[red]All parsing strategies failed[/red]")
            return False
            
        except Exception as e:
            console.print(f"[red]Error parsing response: {e}[/red]")
            return False
    
    def _parse_file_markers(self, response: str, project_path: str) -> int:
        """Parse using FILE: markers."""
        files_created = 0
        current_file = None
        current_content = []
        in_file_content = False
        
        lines = response.split('\n')
        
        for line in lines:
            if line.startswith('FILE: '):
                # Save previous file if exists
                if current_file and current_content:
                    self.create_file(project_path, current_file, '\n'.join(current_content))
                    files_created += 1
                
                # Start new file
                current_file = line.replace('FILE: ', '').strip()
                current_content = []
                in_file_content = False
                
            elif line.startswith('PURPOSE: '):
                # Skip purpose line
                continue
                
            elif line.strip() == '---':
                # Toggle file content mode
                in_file_content = not in_file_content
                
            elif in_file_content and current_file:
                # Add content to current file
                current_content.append(line)
            
            elif current_file and not in_file_content and line.strip():
                # Add content if we're in a file but not in content mode
                current_content.append(line)
        
        # Save last file
        if current_file and current_content:
            self.create_file(project_path, current_file, '\n'.join(current_content))
            files_created += 1
        
        return files_created
    
    def _parse_code_blocks(self, response: str, project_path: str) -> int:
        """Parse using markdown code blocks."""
        import re
        
        files_created = 0
        
        # Pattern to match code blocks with file paths
        code_block_pattern = r'```(?:typescript|javascript|json|css|tsx|jsx|ts|js)?\s*([^\n]+)\n(.*?)```'
        
        matches = re.findall(code_block_pattern, response, re.DOTALL)
        
        for file_path, content in matches:
            if file_path.strip() and content.strip():
                # Clean up file path
                file_path = file_path.strip()
                if file_path.startswith('//'):
                    file_path = file_path[2:].strip()
                
                self.create_file(project_path, file_path, content.strip())
                files_created += 1
        
        return files_created
    
    def _parse_markdown_blocks(self, response: str, project_path: str) -> int:
        """Parse using markdown headers as file indicators."""
        import re
        
        files_created = 0
        
        # Split by markdown headers
        sections = re.split(r'^##\s+', response, flags=re.MULTILINE)
        
        for section in sections[1:]:  # Skip first empty section
            lines = section.split('\n')
            if lines:
                # First line is the file path
                file_path = lines[0].strip()
                content = '\n'.join(lines[1:]).strip()
                
                if file_path and content:
                    self.create_file(project_path, file_path, content)
                    files_created += 1
        
        return files_created
    
    def _parse_manual_extraction(self, response: str, project_path: str) -> int:
        """Manual extraction of common file patterns."""
        import re
        
        files_created = 0
        
        # Common file patterns to look for
        file_patterns = [
            (r'package\.json[:\s]*\n(.*?)(?=\n\n|\n[A-Z]|\Z)', 'package.json'),
            (r'tsconfig\.json[:\s]*\n(.*?)(?=\n\n|\n[A-Z]|\Z)', 'tsconfig.json'),
            (r'next\.config\.js[:\s]*\n(.*?)(?=\n\n|\n[A-Z]|\Z)', 'next.config.js'),
            (r'tailwind\.config\.js[:\s]*\n(.*?)(?=\n\n|\n[A-Z]|\Z)', 'tailwind.config.js'),
            (r'app/layout\.tsx[:\s]*\n(.*?)(?=\n\n|\n[A-Z]|\Z)', 'app/layout.tsx'),
            (r'app/page\.tsx[:\s]*\n(.*?)(?=\n\n|\n[A-Z]|\Z)', 'app/page.tsx'),
            (r'app/globals\.css[:\s]*\n(.*?)(?=\n\n|\n[A-Z]|\Z)', 'app/globals.css'),
        ]
        
        for pattern, file_path in file_patterns:
            match = re.search(pattern, response, re.DOTALL)
            if match:
                content = match.group(1).strip()
                if content:
                    self.create_file(project_path, file_path, content)
                    files_created += 1
        
        return files_created
    
    def create_enhanced_basic_structure(self, project_path: str, technical_spec: Dict[str, Any]) -> bool:
        """Create an enhanced basic structure with more features than the simple fallback."""
        console.print("[yellow]Creating enhanced basic structure...[/yellow]")
        
        # Extract project info from technical spec
        project_name = technical_spec.get("project_overview", {}).get("name", "generated-app")
        project_description = technical_spec.get("project_overview", {}).get("description", "A modern web application")
        
        enhanced_files = {
            "package.json": f"""{{
  "name": "{project_name.lower().replace(' ', '-')}",
  "version": "0.1.0",
  "private": true,
  "description": "{project_description}",
  "scripts": {{
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit"
  }},
  "dependencies": {{
    "next": "14.0.0",
    "react": "^18",
    "react-dom": "^18",
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.0.1",
    "postcss": "^8",
    "@prisma/client": "^5.0.0",
    "next-auth": "^4.24.0",
    "bcryptjs": "^2.4.3",
    "@types/bcryptjs": "^2.4.6"
  }},
  "devDependencies": {{
    "prisma": "^5.0.0",
    "eslint": "^8",
    "eslint-config-next": "14.0.0",
    "@types/bcryptjs": "^2.4.6"
  }}
}}""",
            "next.config.js": """/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: ['localhost'],
  },
}

module.exports = nextConfig""",
            "tsconfig.json": """{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}""",
            "tailwind.config.js": """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        }
      }
    },
  },
  plugins: [],
}""",
            "postcss.config.js": """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}""",
            "prisma/schema.prisma": """// This is your Prisma schema file,
// learn more about it in the docs: https://pris.ly/d/prisma-schema

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  password  String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}""",
            "app/layout.tsx": """import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Generated App',
  description: 'Generated by AI Development Team',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gray-50">
          <header className="bg-white shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex items-center">
                  <h1 className="text-xl font-semibold text-gray-900">
                    Generated App
                  </h1>
                </div>
              </div>
            </div>
          </header>
          <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
}""",
            "app/page.tsx": """import Link from 'next/link'

export default function Home() {
  return (
    <div className="bg-white">
      <div className="relative isolate px-6 pt-14 lg:px-8">
        <div className="mx-auto max-w-2xl py-32 sm:py-48 lg:py-56">
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              Welcome to Your Generated App
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              This application was generated by the AI Development Team Orchestrator.
              It includes a modern Next.js 14 setup with TypeScript, Tailwind CSS, and Prisma.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                href="/dashboard"
                className="rounded-md bg-primary-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
              >
                Get started
              </Link>
              <Link href="/about" className="text-sm font-semibold leading-6 text-gray-900">
                Learn more <span aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}""",
            "app/globals.css": """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-start-rgb: 214, 219, 220;
  --background-end-rgb: 255, 255, 255;
}

@media (prefers-color-scheme: dark) {
  :root {
    --foreground-rgb: 255, 255, 255;
    --background-start-rgb: 0, 0, 0;
    --background-end-rgb: 0, 0, 0;
  }
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
      to bottom,
      transparent,
      rgb(var(--background-end-rgb))
    )
    rgb(var(--background-start-rgb));
}""",
            "app/dashboard/page.tsx": """export default function Dashboard() {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Dashboard</h2>
      <p className="text-gray-600">
        This is your application dashboard. Add your main features here.
      </p>
      <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="font-semibold text-gray-900">Feature 1</h3>
          <p className="text-sm text-gray-600">Description of your first feature</p>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="font-semibold text-gray-900">Feature 2</h3>
          <p className="text-sm text-gray-600">Description of your second feature</p>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="font-semibold text-gray-900">Feature 3</h3>
          <p className="text-sm text-gray-600">Description of your third feature</p>
        </div>
      </div>
    </div>
  )
}""",
            "app/about/page.tsx": """export default function About() {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">About</h2>
      <p className="text-gray-600 mb-4">
        This application was generated using the AI Development Team Orchestrator.
      </p>
      <p className="text-gray-600">
        The orchestrator uses multiple AI agents to create production-ready web applications
        with modern technologies like Next.js 14, TypeScript, and Tailwind CSS.
      </p>
    </div>
  )
}""",
            "components/ui/Button.tsx": """import React from 'react'

interface ButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  onClick?: () => void
  disabled?: boolean
  className?: string
}

export default function Button({
  children,
  variant = 'primary',
  size = 'md',
  onClick,
  disabled = false,
  className = ''
}: ButtonProps) {
  const baseClasses = 'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none'
  
  const variantClasses = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    outline: 'border border-gray-300 bg-transparent hover:bg-gray-50'
  }
  
  const sizeClasses = {
    sm: 'h-8 px-3 text-sm',
    md: 'h-10 px-4 py-2',
    lg: 'h-12 px-6 text-lg'
  }
  
  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  )
}""",
            "lib/db.ts": """import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient()

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma""",
            "README.md": f"""# {project_name}

{project_description}

## Getting Started

First, install dependencies:

```bash
npm install
```

Set up your environment variables:

```bash
cp .env.example .env.local
# Edit .env.local with your values
```

Set up the database:

```bash
npx prisma generate
npx prisma db push
```

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Tech Stack

- Next.js 14 with App Router
- TypeScript
- Tailwind CSS
- Prisma (Database ORM)
- NextAuth.js (Authentication)

## Features

This application includes:
- Modern Next.js 14 setup
- TypeScript for type safety
- Tailwind CSS for styling
- Database integration with Prisma
- Authentication system
- Responsive design
- SEO optimization

## Project Structure

```
app/
├── layout.tsx          # Root layout
├── page.tsx           # Home page
├── dashboard/         # Dashboard pages
├── about/            # About page
└── globals.css       # Global styles

components/
└── ui/               # Reusable UI components

lib/
└── db.ts            # Database configuration

prisma/
└── schema.prisma    # Database schema
```

## Deployment

This application is ready for deployment on:
- Vercel (recommended)
- Netlify
- Railway
- Any Node.js hosting platform

## Generated by

This application was generated by the AI Development Team Orchestrator.
""",
            ".env.example": """# Environment Variables Template
# Copy this file to .env.local and fill in your values

# Database
DATABASE_URL="postgresql://user:password@localhost:5432/database"

# Authentication
NEXTAUTH_SECRET="your-secret-key"
NEXTAUTH_URL="http://localhost:3000"

# API Keys (add as needed)
# STRIPE_SECRET_KEY=""
# SENDGRID_API_KEY=""
# CLOUDINARY_URL=""
""",
            ".gitignore": """# Dependencies
node_modules/
/.pnp
.pnp.js

# Testing
/coverage

# Next.js
/.next/
/out/

# Production
/build

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env*.local
.env

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts

# Prisma
prisma/migrations/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs
*.log

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# OS generated files
Thumbs.db
"""
        }
        
        files_created = 0
        for file_path, content in enhanced_files.items():
            self.create_file(project_path, file_path, content)
            files_created += 1
        
        console.print(f"[green]✅ Created enhanced structure with {files_created} files[/green]")
        return files_created > 0
    
    def create_file(self, project_path: str, file_path: str, content: str):
        """Create a file with the given content."""
        try:
            full_path = os.path.join(project_path, file_path)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Write file content
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            console.print(f"[dim]Created: {file_path}[/dim]")
            
        except Exception as e:
            console.print(f"[red]Error creating file {file_path}: {e}[/red]")
    
    def validate_project_structure(self, project_path: str) -> bool:
        """Validate that the project has the basic required files."""
        required_files = [
            "package.json",
            "tsconfig.json",
            "next.config.js"
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(os.path.join(project_path, file)):
                missing_files.append(file)
        
        if missing_files:
            console.print(f"[yellow]Warning: Missing required files: {', '.join(missing_files)}[/yellow]")
            return False
        
        console.print("[green]✅ Project structure validation passed[/green]")
        return True
    
    def run(self, technical_spec_path: str) -> Optional[str]:
        """Run the builder agent and return the path to the generated project."""
        console.print(f"\n[bold blue]🔄 Starting {self.agent_name}[/bold blue]")
        
        # Load technical specification
        try:
            with open(technical_spec_path, "r") as f:
                technical_spec = json.load(f)
        except FileNotFoundError:
            console.print(f"[red]Error: Technical specification file not found: {technical_spec_path}[/red]")
            return None
        except json.JSONDecodeError:
            console.print(f"[red]Error: Invalid JSON in technical specification file[/red]")
            return None
        
        # Get project name
        project_name = technical_spec.get("project_overview", {}).get("name", "generated-app")
        project_name = project_name.lower().replace(" ", "-").replace("_", "-")
        
        # Create project structure
        project_path = self.create_project_structure(project_name)
        
        # Generate codebase
        if self.generate_codebase(technical_spec, project_path):
            # Validate project structure
            if self.validate_project_structure(project_path):
                console.print(f"\n[green]✅ {self.agent_name} completed successfully[/green]")
                return project_path
            else:
                console.print(f"\n[yellow]⚠️ {self.agent_name} completed with warnings[/yellow]")
                return project_path
        else:
            console.print(f"\n[red]❌ {self.agent_name} failed to generate codebase[/red]")
            return None

def main():
    """Test the builder agent standalone."""
    ollama_client = OllamaClient()
    builder = BuilderAgent(ollama_client)
    
    # Test with a sample technical spec
    result = builder.run("data/technical_spec.json")
    if result:
        console.print(f"Project generated at: {result}")
    else:
        console.print("Failed to generate project")

if __name__ == "__main__":
    main()