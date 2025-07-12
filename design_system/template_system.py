class UltimateTemplateSystem:
    def get_industry_template(self, industry):
        # Return a dictionary representing a professional template for the given industry
        templates = {
            'restaurant': {
                'name': 'Restaurant Ultra Pro',
                'features': ['menu_showcase', 'reservation_form', 'chef_profile', 'gallery', 'testimonials'],
                'style': 'Elegant, appetizing, conversion-optimized',
                'color_palette': 'Warm earth tones, gold accents',
                'typography': 'Serif display with modern sans-serif',
            },
            'portfolio': {
                'name': 'Portfolio Ultra Pro',
                'features': ['portfolio_gallery', 'case_study', 'skills_section', 'testimonials', 'resume_download'],
                'style': 'Minimalist, creative, visually impactful',
                'color_palette': 'Monochrome with accent',
                'typography': 'Modern sans-serif',
            },
            'ecommerce': {
                'name': 'E-commerce Ultra Pro',
                'features': ['product_catalog', 'shopping_cart', 'checkout_form', 'order_tracking', 'reviews'],
                'style': 'Conversion-focused, modern, trustworthy',
                'color_palette': 'Conversion-optimized',
                'typography': 'Clear, readable',
            },
            'blog': {
                'name': 'Blog Ultra Pro',
                'features': ['post_list', 'newsletter_signup', 'author_bio', 'comments_section', 'faq'],
                'style': 'Readable, content-focused, engaging',
                'color_palette': 'Reading-friendly',
                'typography': 'Readable serif/sans-serif',
            },
            'corporate': {
                'name': 'Corporate Ultra Pro',
                'features': ['investor_section', 'careers_section', 'press_section', 'leadership_team', 'news_updates'],
                'style': 'Professional, authoritative, brand-driven',
                'color_palette': 'Corporate blue/gray',
                'typography': 'Professional sans-serif',
            }
        }
        return templates.get(industry, {'name': 'Business Ultra Pro', 'features': [], 'style': 'Professional', 'color_palette': 'Blue/gray', 'typography': 'Sans-serif'})