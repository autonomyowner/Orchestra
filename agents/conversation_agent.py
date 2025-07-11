"""
Conversation Agent - Natural Language Interface for Website Requirements

Conducts intelligent conversations with users to gather comprehensive website requirements
through industry-specific dialogue flows and smart follow-up questions.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from ..utils.ollama_client import OllamaClient

class ConversationAgent:
    """Professional conversation agent for gathering website requirements"""
    
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
        self.console = Console()
        self.conversation_history = []
        
    async def conduct_professional_conversation(self, initial_input: str) -> Optional[Dict[str, Any]]:
        """Conduct a professional conversation to gather comprehensive requirements"""
        
        # Analyze initial input to determine industry and context
        industry_analysis = await self.analyze_industry_context(initial_input)
        
        self.console.print(f"\n[bold green]🎯 I understand you want to create a {industry_analysis['industry']} website![/bold green]")
        self.console.print(f"[cyan]{industry_analysis['summary']}[/cyan]\n")
        
        # Gather comprehensive requirements through industry-specific flow
        requirements = await self.gather_requirements_by_industry(industry_analysis, initial_input)
        
        if not requirements:
            return None
        
        # Validate and summarize requirements
        return await self.validate_and_summarize_requirements(requirements)
    
    async def analyze_industry_context(self, input_text: str) -> Dict[str, Any]:
        """Analyze user input to determine industry and context"""
        
        analysis_prompt = f"""
        Analyze this user input to determine the industry type and context for their website:
        
        User Input: "{input_text}"
        
        Return a JSON response with:
        {{
            "industry": "restaurant|portfolio|business|ecommerce|blog|corporate|creative|nonprofit|health|tech",
            "confidence": 0.0-1.0,
            "summary": "Brief understanding of what they want",
            "key_indicators": ["list", "of", "indicators"],
            "suggested_features": ["feature1", "feature2"],
            "business_type": "specific business type if mentioned"
        }}
        
        Focus on identifying:
        - Industry type (restaurant, portfolio, business, etc.)
        - Business goals and objectives
        - Target audience hints
        - Specific features mentioned
        - Professional tone and sophistication level
        """
        
        response = await self.ollama_client.generate_response(analysis_prompt, "mistral:7b-instruct")
        
        try:
            analysis = json.loads(response)
            return analysis
        except json.JSONDecodeError:
            # Fallback analysis
            return {
                "industry": "business",
                "confidence": 0.5,
                "summary": "I'll help you create a professional website",
                "key_indicators": [],
                "suggested_features": [],
                "business_type": "general business"
            }
    
    async def gather_requirements_by_industry(self, industry_analysis: Dict[str, Any], initial_input: str) -> Dict[str, Any]:
        """Gather requirements using industry-specific conversation flow"""
        
        industry = industry_analysis["industry"]
        requirements = {
            "industry": industry,
            "initial_input": initial_input,
            "business_name": "",
            "description": "",
            "target_audience": "",
            "primary_goals": [],
            "key_features": [],
            "design_preferences": {},
            "color_scheme": "",
            "typography_style": "",
            "content_tone": "",
            "specific_needs": [],
            "competitive_references": [],
            "timeline": "",
            "budget_range": ""
        }
        
        # Industry-specific conversation flows
        if industry == "restaurant":
            return await self.restaurant_conversation_flow(requirements)
        elif industry == "portfolio":
            return await self.portfolio_conversation_flow(requirements)
        elif industry == "ecommerce":
            return await self.ecommerce_conversation_flow(requirements)
        elif industry == "blog":
            return await self.blog_conversation_flow(requirements)
        elif industry == "corporate":
            return await self.corporate_conversation_flow(requirements)
        else:
            return await self.business_conversation_flow(requirements)
    
    async def restaurant_conversation_flow(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Restaurant-specific conversation flow"""
        
        self.console.print("[bold blue]🍽️ Restaurant Website Requirements[/bold blue]")
        
        # Business details
        requirements["business_name"] = Prompt.ask("[cyan]What's your restaurant's name?[/cyan]")
        
        # Restaurant type and cuisine
        restaurant_type = Prompt.ask(
            "[cyan]What type of restaurant is it?[/cyan]",
            choices=["fine-dining", "casual", "fast-casual", "cafe", "bar", "food-truck", "bakery", "other"]
        )
        
        cuisine_type = Prompt.ask("[cyan]What cuisine do you serve?[/cyan]")
        
        requirements["description"] = f"{restaurant_type} {cuisine_type} restaurant"
        
        # Target audience
        target_audience = Prompt.ask(
            "[cyan]Who is your target audience?[/cyan]",
            choices=["families", "young-professionals", "food-enthusiasts", "tourists", "locals", "fine-dining-guests", "mixed"]
        )
        requirements["target_audience"] = target_audience
        
        # Primary goals
        self.console.print("\n[bold]What are your main goals for the website?[/bold]")
        goals = []
        
        if Confirm.ask("[cyan]• Showcase your menu and dishes?[/cyan]"):
            goals.append("menu_showcase")
        if Confirm.ask("[cyan]• Take online reservations?[/cyan]"):
            goals.append("reservations")
        if Confirm.ask("[cyan]• Online ordering/delivery?[/cyan]"):
            goals.append("online_ordering")
        if Confirm.ask("[cyan]• Share your story and atmosphere?[/cyan]"):
            goals.append("brand_storytelling")
        if Confirm.ask("[cyan]• Show location and hours?[/cyan]"):
            goals.append("location_info")
        if Confirm.ask("[cyan]• Display customer reviews?[/cyan]"):
            goals.append("reviews")
        
        requirements["primary_goals"] = goals
        
        # Key features
        features = ["hero_section", "menu_display", "about_section", "contact_info"]
        
        if "reservations" in goals:
            features.append("reservation_system")
        if "online_ordering" in goals:
            features.append("online_ordering")
        if "reviews" in goals:
            features.append("testimonials")
        
        requirements["key_features"] = features
        
        # Design preferences
        design_style = Prompt.ask(
            "[cyan]What design style appeals to you?[/cyan]",
            choices=["elegant", "modern", "rustic", "minimalist", "warm", "sophisticated"]
        )
        
        requirements["design_preferences"] = {
            "style": design_style,
            "atmosphere": "welcoming",
            "imagery": "food_photography"
        }
        
        # Color preferences
        color_preference = Prompt.ask(
            "[cyan]Color preference?[/cyan]",
            choices=["warm-earth-tones", "elegant-dark", "fresh-bright", "classic-neutral", "brand-colors"]
        )
        requirements["color_scheme"] = color_preference
        
        # Content tone
        requirements["content_tone"] = "welcoming and appetizing"
        
        # Specific needs
        specific_needs = []
        if Confirm.ask("[cyan]Need to display dietary information (vegan, gluten-free, etc.)?[/cyan]"):
            specific_needs.append("dietary_information")
        if Confirm.ask("[cyan]Multiple locations?[/cyan]"):
            specific_needs.append("multiple_locations")
        if Confirm.ask("[cyan]Event hosting/catering info?[/cyan]"):
            specific_needs.append("events_catering")
        if Confirm.ask("[cyan]Chef profiles or team info?[/cyan]"):
            specific_needs.append("chef_profiles")
        
        requirements["specific_needs"] = specific_needs
        
        # Timeline
        requirements["timeline"] = Prompt.ask(
            "[cyan]When do you need the website live?[/cyan]",
            choices=["asap", "1-week", "2-weeks", "1-month", "flexible"]
        )
        
        return requirements
    
    async def portfolio_conversation_flow(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Portfolio-specific conversation flow"""
        
        self.console.print("[bold blue]🎨 Portfolio Website Requirements[/bold blue]")
        
        # Personal/professional details
        requirements["business_name"] = Prompt.ask("[cyan]What's your name or brand?[/cyan]")
        
        # Portfolio type
        portfolio_type = Prompt.ask(
            "[cyan]What type of portfolio?[/cyan]",
            choices=["designer", "photographer", "developer", "artist", "writer", "architect", "musician", "other"]
        )
        
        requirements["description"] = f"{portfolio_type} portfolio"
        
        # Target audience
        target_audience = Prompt.ask(
            "[cyan]Who do you want to impress?[/cyan]",
            choices=["potential-clients", "employers", "collaborators", "art-buyers", "general-public", "industry-peers"]
        )
        requirements["target_audience"] = target_audience
        
        # Primary goals
        self.console.print("\n[bold]What are your main goals?[/bold]")
        goals = []
        
        if Confirm.ask("[cyan]• Showcase your best work?[/cyan]"):
            goals.append("work_showcase")
        if Confirm.ask("[cyan]• Get hired or attract clients?[/cyan]"):
            goals.append("lead_generation")
        if Confirm.ask("[cyan]• Tell your professional story?[/cyan]"):
            goals.append("personal_branding")
        if Confirm.ask("[cyan]• Display your skills and services?[/cyan]"):
            goals.append("skills_display")
        if Confirm.ask("[cyan]• Include a blog or insights?[/cyan]"):
            goals.append("blog_content")
        
        requirements["primary_goals"] = goals
        
        # Key features
        features = ["hero_section", "portfolio_gallery", "about_section", "contact_form"]
        
        if "skills_display" in goals:
            features.append("skills_section")
        if "blog_content" in goals:
            features.append("blog_section")
        if "personal_branding" in goals:
            features.append("testimonials")
        
        requirements["key_features"] = features
        
        # Design preferences
        design_style = Prompt.ask(
            "[cyan]What design style represents you?[/cyan]",
            choices=["minimalist", "creative", "professional", "artistic", "modern", "unique"]
        )
        
        requirements["design_preferences"] = {
            "style": design_style,
            "personality": "professional",
            "focus": "visual_impact"
        }
        
        # Color preferences
        color_preference = Prompt.ask(
            "[cyan]Color approach?[/cyan]",
            choices=["monochrome", "brand-colors", "colorful", "muted-tones", "high-contrast", "neutral"]
        )
        requirements["color_scheme"] = color_preference
        
        # Content tone
        requirements["content_tone"] = "professional and confident"
        
        # Specific needs
        specific_needs = []
        if Confirm.ask("[cyan]Need case studies or project details?[/cyan]"):
            specific_needs.append("case_studies")
        if Confirm.ask("[cyan]Downloadable resume/CV?[/cyan]"):
            specific_needs.append("resume_download")
        if Confirm.ask("[cyan]Client testimonials?[/cyan]"):
            specific_needs.append("testimonials")
        if Confirm.ask("[cyan]Award or recognition section?[/cyan]"):
            specific_needs.append("awards")
        
        requirements["specific_needs"] = specific_needs
        
        return requirements
    
    async def business_conversation_flow(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """General business conversation flow"""
        
        self.console.print("[bold blue]💼 Business Website Requirements[/bold blue]")
        
        # Business details
        requirements["business_name"] = Prompt.ask("[cyan]What's your business name?[/cyan]")
        
        # Business type
        business_type = Prompt.ask("[cyan]What type of business?[/cyan]")
        requirements["description"] = business_type
        
        # Target audience
        target_audience = Prompt.ask(
            "[cyan]Who are your target customers?[/cyan]",
            choices=["small-businesses", "enterprises", "consumers", "professionals", "local-customers", "online-customers"]
        )
        requirements["target_audience"] = target_audience
        
        # Primary goals
        self.console.print("\n[bold]What are your main business goals?[/bold]")
        goals = []
        
        if Confirm.ask("[cyan]• Generate leads and inquiries?[/cyan]"):
            goals.append("lead_generation")
        if Confirm.ask("[cyan]• Showcase your services?[/cyan]"):
            goals.append("service_showcase")
        if Confirm.ask("[cyan]• Build trust and credibility?[/cyan]"):
            goals.append("trust_building")
        if Confirm.ask("[cyan]• Provide customer support?[/cyan]"):
            goals.append("customer_support")
        if Confirm.ask("[cyan]• Online sales?[/cyan]"):
            goals.append("online_sales")
        
        requirements["primary_goals"] = goals
        
        # Key features
        features = ["hero_section", "services_section", "about_section", "contact_form"]
        
        if "trust_building" in goals:
            features.append("testimonials")
        if "customer_support" in goals:
            features.append("faq_section")
        if "online_sales" in goals:
            features.append("pricing_section")
        
        requirements["key_features"] = features
        
        # Design preferences
        design_style = Prompt.ask(
            "[cyan]What design style fits your brand?[/cyan]",
            choices=["professional", "modern", "trustworthy", "innovative", "approachable", "premium"]
        )
        
        requirements["design_preferences"] = {
            "style": design_style,
            "brand_personality": "professional",
            "conversion_focus": True
        }
        
        # Color preferences
        color_preference = Prompt.ask(
            "[cyan]Color preference?[/cyan]",
            choices=["corporate-blue", "trustworthy-dark", "energetic-bright", "professional-neutral", "brand-colors"]
        )
        requirements["color_scheme"] = color_preference
        
        # Content tone
        requirements["content_tone"] = "professional and trustworthy"
        
        return requirements
    
    async def ecommerce_conversation_flow(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """E-commerce specific conversation flow"""
        
        self.console.print("[bold blue]🛒 E-commerce Website Requirements[/bold blue]")
        
        # Store details
        requirements["business_name"] = Prompt.ask("[cyan]What's your store name?[/cyan]")
        
        # Product type
        product_type = Prompt.ask("[cyan]What do you sell?[/cyan]")
        requirements["description"] = f"Online store selling {product_type}"
        
        # Target audience
        target_audience = Prompt.ask(
            "[cyan]Who are your customers?[/cyan]",
            choices=["general-consumers", "niche-enthusiasts", "professionals", "businesses", "local-customers", "global-customers"]
        )
        requirements["target_audience"] = target_audience
        
        # Primary goals
        goals = ["product_sales", "brand_awareness", "customer_retention"]
        requirements["primary_goals"] = goals
        
        # Key features
        features = ["hero_section", "product_catalog", "shopping_cart", "checkout_process", "user_accounts", "payment_processing"]
        
        if Confirm.ask("[cyan]Need customer reviews?[/cyan]"):
            features.append("product_reviews")
        if Confirm.ask("[cyan]Need inventory management?[/cyan]"):
            features.append("inventory_management")
        if Confirm.ask("[cyan]Need order tracking?[/cyan]"):
            features.append("order_tracking")
        
        requirements["key_features"] = features
        
        # Design preferences
        requirements["design_preferences"] = {
            "style": "modern",
            "conversion_optimized": True,
            "mobile_commerce": True
        }
        
        # Color preferences
        requirements["color_scheme"] = "conversion-optimized"
        
        # Content tone
        requirements["content_tone"] = "persuasive and trustworthy"
        
        return requirements
    
    async def blog_conversation_flow(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Blog-specific conversation flow"""
        
        self.console.print("[bold blue]📝 Blog Website Requirements[/bold blue]")
        
        # Blog details
        requirements["business_name"] = Prompt.ask("[cyan]What's your blog name?[/cyan]")
        
        # Blog niche
        blog_niche = Prompt.ask("[cyan]What's your blog about?[/cyan]")
        requirements["description"] = f"Blog about {blog_niche}"
        
        # Target audience
        target_audience = Prompt.ask(
            "[cyan]Who are your readers?[/cyan]",
            choices=["general-audience", "niche-community", "professionals", "enthusiasts", "beginners", "experts"]
        )
        requirements["target_audience"] = target_audience
        
        # Primary goals
        goals = ["content_sharing", "audience_building", "thought_leadership"]
        
        if Confirm.ask("[cyan]Want to monetize your blog?[/cyan]"):
            goals.append("monetization")
        if Confirm.ask("[cyan]Building an email list?[/cyan]"):
            goals.append("email_collection")
        
        requirements["primary_goals"] = goals
        
        # Key features
        features = ["hero_section", "blog_posts", "categories", "search", "about_section", "contact_form"]
        
        if "email_collection" in goals:
            features.append("newsletter_signup")
        if "monetization" in goals:
            features.append("advertising_spaces")
        
        requirements["key_features"] = features
        
        # Design preferences
        requirements["design_preferences"] = {
            "style": "readable",
            "content_focused": True,
            "readability_optimized": True
        }
        
        # Color preferences
        requirements["color_scheme"] = "reading-friendly"
        
        # Content tone
        requirements["content_tone"] = "engaging and informative"
        
        return requirements
    
    async def corporate_conversation_flow(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Corporate-specific conversation flow"""
        
        self.console.print("[bold blue]🏢 Corporate Website Requirements[/bold blue]")
        
        # Company details
        requirements["business_name"] = Prompt.ask("[cyan]What's your company name?[/cyan]")
        
        # Company type
        company_type = Prompt.ask("[cyan]What industry are you in?[/cyan]")
        requirements["description"] = f"Corporate website for {company_type} company"
        
        # Target audience
        target_audience = Prompt.ask(
            "[cyan]Who needs to find you?[/cyan]",
            choices=["customers", "investors", "partners", "employees", "media", "stakeholders"]
        )
        requirements["target_audience"] = target_audience
        
        # Primary goals
        goals = ["brand_presence", "credibility", "information_sharing"]
        
        if Confirm.ask("[cyan]Attract investors?[/cyan]"):
            goals.append("investor_relations")
        if Confirm.ask("[cyan]Recruit talent?[/cyan]"):
            goals.append("talent_acquisition")
        if Confirm.ask("[cyan]Media and press relations?[/cyan]"):
            goals.append("media_relations")
        
        requirements["primary_goals"] = goals
        
        # Key features
        features = ["hero_section", "company_overview", "services_products", "leadership_team", "news_updates", "contact_info"]
        
        if "investor_relations" in goals:
            features.append("investor_section")
        if "talent_acquisition" in goals:
            features.append("careers_section")
        if "media_relations" in goals:
            features.append("press_section")
        
        requirements["key_features"] = features
        
        # Design preferences
        requirements["design_preferences"] = {
            "style": "professional",
            "corporate_identity": True,
            "trust_building": True
        }
        
        # Color preferences
        requirements["color_scheme"] = "corporate-professional"
        
        # Content tone
        requirements["content_tone"] = "professional and authoritative"
        
        return requirements
    
    async def validate_and_summarize_requirements(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and summarize the gathered requirements"""
        
        self.console.print("\n[bold green]📋 Requirements Summary[/bold green]")
        
        # Display summary
        summary_text = f"""
[bold]Business:[/bold] {requirements['business_name']}
[bold]Type:[/bold] {requirements['description']}
[bold]Target Audience:[/bold] {requirements['target_audience']}
[bold]Primary Goals:[/bold] {', '.join(requirements['primary_goals'])}
[bold]Key Features:[/bold] {', '.join(requirements['key_features'])}
[bold]Design Style:[/bold] {requirements['design_preferences'].get('style', 'Not specified')}
[bold]Color Scheme:[/bold] {requirements['color_scheme']}
[bold]Content Tone:[/bold] {requirements['content_tone']}
        """
        
        self.console.print(Panel(summary_text, title="Requirements Summary", border_style="green"))
        
        # Confirm with user
        if Confirm.ask("\n[cyan]Does this look correct?[/cyan]"):
            return requirements
        else:
            self.console.print("[yellow]Let's refine the requirements...[/yellow]")
            # Could add refinement logic here
            return requirements