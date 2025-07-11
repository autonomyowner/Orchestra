class DesignPreviewAgent:
    def __init__(self, ollama_client, design_system):
        self.ollama_client = ollama_client
        self.design_system = design_system
        
    async def generate_design_previews(self, requirements):
        """Generate multiple professional design options based on requirements"""
        
        industry = requirements.get("industry", "business")
        design_options = await self.create_industry_design_options(industry)
        
        enhanced_options = []
        for option in design_options:
            enhanced_option = await self.enhance_with_design_system(option, industry)
            enhanced_options.append(enhanced_option)
        
        return enhanced_options
    
    async def create_industry_design_options(self, industry):
        """Create industry-specific design options"""
        
        if industry == "restaurant":
            return [
                {
                    "name": "Sophisticated Elegance",
                    "style": "Fine dining with luxurious aesthetics",
                    "color_scheme": "Deep burgundy, gold accents, cream",
                    "typography": "Elegant serif with modern sans-serif",
                    "layout_type": "Full-width hero with refined grid",
                    "hero_style": "Full-screen hero with signature dish imagery",
                    "navigation_style": "Elegant horizontal nav with gold accents",
                    "content_layout": "Refined card-based layout with generous spacing",
                    "call_to_action_style": "Sophisticated buttons with hover animations",
                    "personality": "upscale",
                    "conversion_elements": ["reservation_button", "menu_highlight", "chef_story"]
                },
                {
                    "name": "Modern Minimalist",
                    "style": "Clean, contemporary with food-focused imagery",
                    "color_scheme": "Charcoal, white, warm orange accents",
                    "typography": "Modern geometric sans-serif",
                    "layout_type": "Grid-based with visual hierarchy",
                    "hero_style": "Split-screen with stunning food photography",
                    "navigation_style": "Clean horizontal nav with subtle shadows",
                    "content_layout": "Card-based sections with photo emphasis",
                    "call_to_action_style": "Modern buttons with micro-interactions",
                    "personality": "contemporary",
                    "conversion_elements": ["online_ordering", "location_map", "social_proof"]
                }
            ]
        elif industry == "portfolio":
            return [
                {
                    "name": "Minimalist Showcase",
                    "style": "Clean, work-focused with maximum impact",
                    "color_scheme": "Monochromatic with selective color highlights",
                    "typography": "Modern sans-serif with elegant hierarchy",
                    "layout_type": "Grid-based portfolio with generous whitespace",
                    "hero_style": "Impactful hero with best work preview",
                    "navigation_style": "Minimal nav with smooth transitions",
                    "content_layout": "Masonry grid with detailed case studies",
                    "call_to_action_style": "Subtle but effective contact prompts",
                    "personality": "professional",
                    "conversion_elements": ["work_quality", "process_showcase", "client_testimonials"]
                },
                {
                    "name": "Creative Expression",
                    "style": "Artistic with unique personality",
                    "color_scheme": "Bold artistic palette with creative freedom",
                    "typography": "Creative display fonts with readable body text",
                    "layout_type": "Experimental layouts with creative freedom",
                    "hero_style": "Artistic hero showcasing creative personality",
                    "navigation_style": "Creative nav with unique animations",
                    "content_layout": "Experimental sections with artistic flair",
                    "call_to_action_style": "Creative buttons matching artistic style",
                    "personality": "artistic",
                    "conversion_elements": ["creative_process", "unique_style", "artistic_vision"]
                }
            ]
        else:
            return [
                {
                    "name": "Professional Trust",
                    "style": "Clean, trustworthy with business credibility",
                    "color_scheme": "Corporate blue, white, subtle gray accents",
                    "typography": "Professional sans-serif with clear hierarchy",
                    "layout_type": "Structured layouts with conversion focus",
                    "hero_style": "Professional hero with value proposition",
                    "navigation_style": "Clear nav with trust indicators",
                    "content_layout": "Benefit-focused sections with social proof",
                    "call_to_action_style": "Conversion-optimized buttons with clear value",
                    "personality": "trustworthy",
                    "conversion_elements": ["value_proposition", "social_proof", "clear_benefits"]
                },
                {
                    "name": "Modern Innovation",
                    "style": "Cutting-edge with innovative approach",
                    "color_scheme": "Modern gradients with tech-forward colors",
                    "typography": "Modern geometric fonts with tech appeal",
                    "layout_type": "Dynamic layouts with innovative elements",
                    "hero_style": "Tech-forward hero with innovation focus",
                    "navigation_style": "Modern nav with interactive elements",
                    "content_layout": "Dynamic sections with tech aesthetics",
                    "call_to_action_style": "Modern buttons with tech-forward design",
                    "personality": "innovative",
                    "conversion_elements": ["innovation_story", "tech_advantages", "future_vision"]
                }
            ]
    
    async def enhance_with_design_system(self, option, industry):
        """Enhance design option with professional design system elements"""
        
        enhanced_option = option.copy()
        enhanced_option["spacing_system"] = "Professional spacing with 8px grid system"
        enhanced_option["typography_system"] = "Hierarchical typography with proper line heights"
        enhanced_option["color_system"] = "WCAG AA compliant color palette"
        enhanced_option["component_recommendations"] = f"Industry-specific components for {industry}"
        enhanced_option["accessibility_features"] = "WCAG AA compliance with keyboard navigation"
        enhanced_option["performance_optimizations"] = "Optimized for Core Web Vitals"
        enhanced_option["micro_interactions"] = "Smooth animations and hover effects"
        
        return enhanced_option
    
    async def get_color_customization(self):
        """Get color customization preferences from user"""
        
        return {
            "palette": "Professional Blues & Grays",
            "primary_color": "#2563eb",
            "secondary_color": "#64748b",
            "accent_color": "#f59e0b"
        }
    
    async def get_typography_customization(self):
        """Get typography customization preferences from user"""
        
        return {
            "style": "Modern Sans-Serif (Clean & Professional)",
            "heading_font": "Inter",
            "body_font": "Inter",
            "size_scale": "medium"
        }