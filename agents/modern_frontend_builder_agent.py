#!/usr/bin/env python3
"""
Modern Frontend Builder Agent - 2025 Edition
Builds production-ready, enterprise-grade frontend applications with the latest tech stack.

Tech Stack (July 2025):
✅ React 19 with Server & Client Components
✅ Next.js 15.4 with App Router system
✅ TypeScript 5.4 with strict mode
✅ Tailwind CSS 4.0 with RTL and theming
✅ shadcn/ui for components
✅ Framer Motion 12 for animations
✅ Vitest 1.3+ & Playwright 1.45+ for testing
✅ react-hook-form + zod for forms
✅ lucide-react for icons
✅ next-intl for i18n
✅ PWA ready with full accessibility
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

from core.openrouter_client import OpenRouterClient

console = Console()

class ModernFrontendBuilderAgent:
    """Advanced frontend builder for 2025 tech stack"""
    
    def __init__(self, openrouter_client: Optional[OpenRouterClient] = None):
        self.client = openrouter_client or OpenRouterClient()
        self.console = console
        
        # Modern tech stack configuration
        self.tech_stack = {
            "react": "19.0.0",
            "next": "15.4.0", 
            "typescript": "5.4.0",
            "tailwindcss": "4.0.0",
            "framer_motion": "12.0.0",
            "vitest": "1.3.0",
            "playwright": "1.45.0",
            "react_hook_form": "7.52.0",
            "zod": "3.23.0",
            "lucide_react": "0.400.0",
            "next_intl": "3.15.0",
            "shadcn_ui": "latest"
        }
        
        # Quality standards for $1M websites
        self.quality_standards = {
            "performance": {
                "lighthouse_score": 95,
                "core_web_vitals": "all_green",
                "bundle_size_limit": "< 500KB",
                "loading_time": "< 2s"
            },
            "accessibility": {
                "wcag_level": "AA",
                "aria_compliance": True,
                "keyboard_navigation": True,
                "screen_reader_support": True
            },
            "seo": {
                "meta_optimization": True,
                "structured_data": True,
                "sitemap": True,
                "robots_txt": True
            },
            "code_quality": {
                "typescript_strict": True,
                "eslint_zero_warnings": True,
                "test_coverage": "> 90%",
                "documentation": "comprehensive"
            }
        }
    
    async def build_modern_frontend(self, project_spec: Dict[str, Any]) -> Optional[str]:
        """Build a modern frontend application with 2025 tech stack"""
        
        console.print(Panel(
            "[bold green]🚀 Building Modern Frontend Application[/bold green]\n"
            "[cyan]Using React 19 + Next.js 15.4 + Latest Tech Stack[/cyan]",
            title="Modern Frontend Builder",
            border_style="magenta"
        ))
        
        try:
            # Step 1: Generate project structure
            project_structure = await self._generate_project_structure(project_spec)
            
            # Step 2: Create package.json with modern dependencies
            package_json = await self._create_package_json(project_spec)
            
            # Step 3: Generate TypeScript configuration
            ts_config = await self._create_typescript_config()
            
            # Step 4: Generate Tailwind CSS 4.0 configuration
            tailwind_config = await self._create_tailwind_config()
            
            # Step 5: Generate Next.js 15.4 configuration
            next_config = await self._create_next_config()
            
            # Step 6: Generate app router structure
            app_router_files = await self._generate_app_router_structure(project_spec)
            
            # Step 7: Generate shadcn/ui components
            shadcn_components = await self._generate_shadcn_components(project_spec)
            
            # Step 8: Generate pages with Framer Motion
            pages = await self._generate_pages_with_animations(project_spec)
            
            # Step 9: Generate forms with react-hook-form + zod
            forms = await self._generate_forms_with_validation(project_spec)
            
            # Step 10: Generate internationalization setup
            i18n_setup = await self._generate_i18n_setup()
            
            # Step 11: Generate PWA configuration
            pwa_config = await self._generate_pwa_config()
            
            # Step 12: Generate testing setup
            testing_setup = await self._generate_testing_setup()
            
            # Step 13: Create project files
            project_path = await self._create_project_files({
                "structure": project_structure,
                "package_json": package_json,
                "ts_config": ts_config,
                "tailwind_config": tailwind_config,
                "next_config": next_config,
                "app_router_files": app_router_files,
                "shadcn_components": shadcn_components,
                "pages": pages,
                "forms": forms,
                "i18n_setup": i18n_setup,
                "pwa_config": pwa_config,
                "testing_setup": testing_setup
            }, project_spec)
            
            return project_path
            
        except Exception as e:
            console.print(f"[red]❌ Build failed: {e}[/red]")
            return None
    
    async def _generate_project_structure(self, project_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate modern Next.js 15.4 project structure"""
        
        prompt = f"""
Generate a modern Next.js 15.4 project structure for: {project_spec['name']}

Requirements:
- App Router structure (app/ directory)
- TypeScript 5.4 with strict mode
- Modern component organization
- Proper separation of concerns
- Enterprise-grade architecture

Project Type: {project_spec.get('type', 'business')}
Features: {project_spec.get('features', [])}

Return a detailed JSON structure with:
1. Directory structure
2. File purposes
3. Import/export patterns
4. Component hierarchy
"""
        
        response, model, cost = await self.client.generate_with_fallback(
            prompt,
            task_type="architecture",
            complexity="high"
        )
        
        return json.loads(response)
    
    async def _create_package_json(self, project_spec: Dict[str, Any]) -> str:
        """Create package.json with modern 2025 dependencies"""
        
        prompt = f"""
Create a package.json for a modern React 19 + Next.js 15.4 application.

Project: {project_spec['name']}
Description: {project_spec.get('description', '')}

REQUIRED DEPENDENCIES (exact versions):
- react: ^19.0.0
- next: ^15.4.0
- typescript: ^5.4.0
- @types/react: ^18.3.0
- @types/node: ^20.0.0
- tailwindcss: ^4.0.0
- framer-motion: ^12.0.0
- @hookform/resolvers: ^3.3.0
- react-hook-form: ^7.52.0
- zod: ^3.23.0
- lucide-react: ^0.400.0
- next-intl: ^3.15.0
- @radix-ui/react-* (shadcn/ui components)

DEV DEPENDENCIES:
- vitest: ^1.3.0
- @playwright/test: ^1.45.0
- eslint: ^8.0.0
- prettier: ^3.0.0
- @types/jest: ^29.0.0

SCRIPTS:
- dev, build, start, lint, test, test:e2e, type-check

Include proper metadata, keywords, and configuration.
Return valid JSON only.
"""
        
        response, model, cost = await self.client.generate_with_fallback(
            prompt,
            task_type="configuration",
            complexity="medium"
        )
        
        return response
    
    async def _create_typescript_config(self) -> str:
        """Create TypeScript 5.4 configuration with strict mode"""
        
        prompt = """
Create a TypeScript 5.4 configuration for Next.js 15.4 with strict mode enabled.

Requirements:
- strict: true
- Modern ES target
- Next.js 15.4 optimizations
- Path mapping for clean imports
- Optimal type checking
- Performance optimized

Return tsconfig.json content only.
"""
        
        response, model, cost = await self.client.generate_with_fallback(
            prompt,
            task_type="configuration",
            complexity="simple"
        )
        
        return response
    
    async def _create_tailwind_config(self) -> str:
        """Create Tailwind CSS 4.0 configuration with RTL and theming"""
        
        prompt = """
Create a Tailwind CSS 4.0 configuration with:

- RTL language support
- Dark/light theme system
- Custom design tokens
- Animation utilities
- Responsive breakpoints
- Typography plugin
- Forms plugin
- Accessibility utilities

Modern CSS-in-JS approach with CSS variables.
Return complete tailwind.config.js content.
"""
        
        response, model, cost = await self.client.generate_with_fallback(
            prompt,
            task_type="styling",
            complexity="medium"
        )
        
        return response
    
    async def _create_next_config(self) -> str:
        """Create Next.js 15.4 configuration"""
        
        prompt = """
Create a Next.js 15.4 configuration with:

- App Router enabled
- TypeScript support
- Tailwind CSS integration
- Image optimization
- PWA support
- Internationalization
- Performance optimizations
- Security headers
- Bundle optimization

Include experimental features for React 19.
Return next.config.js content.
"""
        
        response, model, cost = await self.client.generate_with_fallback(
            prompt,
            task_type="configuration",
            complexity="medium"
        )
        
        return response
    
    async def _generate_app_router_structure(self, project_spec: Dict[str, Any]) -> Dict[str, str]:
        """Generate Next.js 15.4 App Router structure"""
        
        pages = project_spec.get('pages', ['Home', 'About', 'Contact'])
        
        files = {}
        
        # Generate layout.tsx
        layout_prompt = f"""
Create a modern Next.js 15.4 app/layout.tsx with:

- React 19 Server Component
- TypeScript 5.4 strict mode
- next-intl provider
- Tailwind CSS 4.0
- PWA manifest
- SEO metadata
- Accessibility features

Project: {project_spec['name']}
Description: {project_spec.get('description', '')}

Return complete layout.tsx code.
"""
        
        layout_response, _, _ = await self.client.generate_with_fallback(
            layout_prompt,
            task_type="frontend",
            complexity="high"
        )
        
        files['app/layout.tsx'] = layout_response
        
        # Generate page.tsx (home)
        home_prompt = f"""
Create a modern Next.js 15.4 app/page.tsx (home page) with:

- React 19 Server Component
- Framer Motion 12 animations
- shadcn/ui components
- Tailwind CSS 4.0 styling
- lucide-react icons
- Responsive design
- Accessibility features

Project: {project_spec['name']}
Type: {project_spec.get('type', 'business')}
Features: {project_spec.get('features', [])}

Return complete page.tsx code.
"""
        
        home_response, _, _ = await self.client.generate_with_fallback(
            home_prompt,
            task_type="frontend",
            complexity="high"
        )
        
        files['app/page.tsx'] = home_response
        
        # Generate additional pages
        for page in pages[1:]:  # Skip home page
            page_prompt = f"""
Create a {page} page for Next.js 15.4 app router.

Path: app/{page.lower()}/page.tsx
Requirements:
- React 19 Server Component
- shadcn/ui components
- Framer Motion animations
- Responsive design
- Proper SEO metadata

Project context: {project_spec['name']}
Return complete page.tsx code.
"""
            
            page_response, _, _ = await self.client.generate_with_fallback(
                page_prompt,
                task_type="frontend",
                complexity="medium"
            )
            
            files[f'app/{page.lower()}/page.tsx'] = page_response
        
        return files
    
    async def _generate_shadcn_components(self, project_spec: Dict[str, Any]) -> Dict[str, str]:
        """Generate shadcn/ui components"""
        
        components_needed = [
            'button', 'card', 'input', 'form', 'dialog', 'dropdown-menu',
            'avatar', 'badge', 'toast', 'tabs', 'accordion', 'navigation-menu'
        ]
        
        components = {}
        
        for component in components_needed:
            prompt = f"""
Create a {component} component using shadcn/ui patterns.

Requirements:
- TypeScript 5.4 with strict mode
- Tailwind CSS 4.0
- Radix UI primitives
- Full accessibility (WCAG AA)
- Variant system
- Forward refs
- Proper typing

Return the complete component code for components/ui/{component}.tsx
"""
            
            response, _, _ = await self.client.generate_with_fallback(
                prompt,
                task_type="frontend",
                complexity="medium"
            )
            
            components[f'components/ui/{component}.tsx'] = response
        
        return components
    
    async def _generate_pages_with_animations(self, project_spec: Dict[str, Any]) -> Dict[str, str]:
        """Generate pages with Framer Motion 12 animations"""
        
        pages = {}
        page_types = project_spec.get('pages', ['Landing', 'Features', 'Pricing', 'Contact'])
        
        for page_type in page_types:
            prompt = f"""
Create a {page_type} page component with Framer Motion 12 animations.

Requirements:
- React 19 Client Component ("use client")
- TypeScript 5.4 strict mode
- Framer Motion 12 animations
- shadcn/ui components
- lucide-react icons
- Responsive design
- Performance optimized
- Accessibility features

Project: {project_spec['name']}
Industry: {project_spec.get('industry', 'technology')}

Return complete component code for components/pages/{page_type}Page.tsx
"""
            
            response, _, _ = await self.client.generate_with_fallback(
                prompt,
                task_type="frontend",
                complexity="high"
            )
            
            pages[f'components/pages/{page_type}Page.tsx'] = response
        
        return pages
    
    async def _generate_forms_with_validation(self, project_spec: Dict[str, Any]) -> Dict[str, str]:
        """Generate forms with react-hook-form + zod validation"""
        
        forms = {}
        form_types = ['contact', 'newsletter', 'auth']
        
        for form_type in form_types:
            prompt = f"""
Create a {form_type} form using react-hook-form + zod validation.

Requirements:
- React 19 Client Component
- react-hook-form ^7.52.0
- zod ^3.23.0 for validation
- shadcn/ui form components
- TypeScript 5.4 strict typing
- Error handling
- Loading states
- Accessibility
- Real-time validation

Return complete form component code for components/forms/{form_type.title()}Form.tsx
"""
            
            response, _, _ = await self.client.generate_with_fallback(
                prompt,
                task_type="frontend",
                complexity="high"
            )
            
            forms[f'components/forms/{form_type.title()}Form.tsx'] = response
        
        return forms
    
    async def _generate_i18n_setup(self) -> Dict[str, str]:
        """Generate next-intl internationalization setup"""
        
        i18n_files = {}
        
        # Generate i18n configuration
        config_prompt = """
Create next-intl configuration for Next.js 15.4 with:

- Multiple language support (en, es, fr, ar for RTL)
- App Router integration
- Type-safe translations
- RTL language support
- Default locale handling
- Automatic language detection

Return code for:
1. i18n.ts configuration
2. middleware.ts for locale routing
3. messages/en.json structure
4. messages/ar.json for RTL testing
"""
        
        response, _, _ = await self.client.generate_with_fallback(
            config_prompt,
            task_type="configuration",
            complexity="medium"
        )
        
        # Parse response to separate files
        i18n_files['i18n.ts'] = response
        i18n_files['middleware.ts'] = response
        i18n_files['messages/en.json'] = response
        i18n_files['messages/ar.json'] = response
        
        return i18n_files
    
    async def _generate_pwa_config(self) -> Dict[str, str]:
        """Generate PWA configuration"""
        
        pwa_files = {}
        
        prompt = """
Create PWA configuration for Next.js 15.4:

1. manifest.json with modern PWA features
2. service worker registration
3. offline page
4. PWA installation prompt component

Requirements:
- Modern PWA standards
- Offline functionality
- App-like experience
- Cross-platform support

Return code for each file.
"""
        
        response, _, _ = await self.client.generate_with_fallback(
            prompt,
            task_type="configuration",
            complexity="medium"
        )
        
        pwa_files['public/manifest.json'] = response
        pwa_files['public/sw.js'] = response
        pwa_files['app/offline/page.tsx'] = response
        
        return pwa_files
    
    async def _generate_testing_setup(self) -> Dict[str, str]:
        """Generate Vitest + Playwright testing setup"""
        
        test_files = {}
        
        # Vitest configuration
        vitest_prompt = """
Create Vitest 1.3+ configuration for React 19 + Next.js 15.4:

1. vitest.config.ts
2. setupTests.ts
3. Example component test
4. Example integration test

Requirements:
- React Testing Library
- TypeScript support
- Coverage reporting
- Snapshot testing
"""
        
        vitest_response, _, _ = await self.client.generate_with_fallback(
            vitest_prompt,
            task_type="testing",
            complexity="medium"
        )
        
        test_files['vitest.config.ts'] = vitest_response
        
        # Playwright configuration
        playwright_prompt = """
Create Playwright 1.45+ configuration for Next.js 15.4:

1. playwright.config.ts
2. Example e2e test
3. Page object model example

Requirements:
- Multiple browsers
- Mobile testing
- Screenshots
- Video recording
"""
        
        playwright_response, _, _ = await self.client.generate_with_fallback(
            playwright_prompt,
            task_type="testing",
            complexity="medium"
        )
        
        test_files['playwright.config.ts'] = playwright_response
        test_files['tests/e2e/home.spec.ts'] = playwright_response
        
        return test_files
    
    async def _create_project_files(self, generated_content: Dict[str, Any], project_spec: Dict[str, Any]) -> str:
        """Create all project files in the workspace"""
        
        project_name = project_spec['name'].lower().replace(' ', '-')
        project_path = Path(f"/workspace/generated_projects/{project_name}")
        
        # Create project directory
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Create all files
        all_files = {}
        
        # Merge all generated content
        for content_type, content in generated_content.items():
            if isinstance(content, dict):
                all_files.update(content)
            else:
                # Handle single file content
                if content_type == "package_json":
                    all_files["package.json"] = content
                elif content_type == "ts_config":
                    all_files["tsconfig.json"] = content
                elif content_type == "tailwind_config":
                    all_files["tailwind.config.js"] = content
                elif content_type == "next_config":
                    all_files["next.config.js"] = content
        
        # Write files
        for file_path, file_content in all_files.items():
            full_path = project_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
        
        # Create additional necessary files
        await self._create_additional_files(project_path, project_spec)
        
        console.print(f"✅ Project created at: {project_path}")
        return str(project_path)
    
    async def _create_additional_files(self, project_path: Path, project_spec: Dict[str, Any]):
        """Create additional necessary files"""
        
        # .env.local template
        env_content = """# Environment Variables
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_APP_NAME="{}"

# Add your environment variables here
""".format(project_spec['name'])
        
        with open(project_path / '.env.local.example', 'w') as f:
            f.write(env_content)
        
        # README.md
        readme_content = f"""# {project_spec['name']}

{project_spec.get('description', 'A modern React 19 + Next.js 15.4 application')}

## Tech Stack

- ⚛️ React 19 with Server & Client Components
- 🚀 Next.js 15.4 with App Router
- 📘 TypeScript 5.4 with strict mode
- 🎨 Tailwind CSS 4.0 with RTL support
- 🧩 shadcn/ui components
- 🎭 Framer Motion 12 animations
- 📋 react-hook-form + zod validation
- 🎯 lucide-react icons
- 🌍 next-intl internationalization
- 📱 PWA ready
- 🧪 Vitest + Playwright testing

## Getting Started

```bash
npm install
npm run dev
```

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run test` - Run unit tests
- `npm run test:e2e` - Run e2e tests
- `npm run lint` - Lint code
- `npm run type-check` - Type checking

## Features

{chr(10).join(f'- {feature}' for feature in project_spec.get('features', []))}

Built with 💎 quality standards for enterprise applications.
"""
        
        with open(project_path / 'README.md', 'w') as f:
            f.write(readme_content)
        
        # .gitignore
        gitignore_content = """# Dependencies
/node_modules
/.pnp
.pnp.js

# Testing
/coverage
/test-results
/playwright-report

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

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts
"""
        
        with open(project_path / '.gitignore', 'w') as f:
            f.write(gitignore_content)