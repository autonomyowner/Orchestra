class ComponentLibrary:
    def get_components_for_industry(self, industry):
        # Return a list of professional, reusable components for the given industry
        base_components = [
            'hero_section', 'navigation_bar', 'about_section', 'services_showcase',
            'testimonials', 'contact_form', 'footer', 'cta_banner', 'gallery', 'pricing',
            'blog_preview', 'faq', 'features_grid', 'team_section', 'micro_interactions'
        ]
        if industry == 'restaurant':
            return base_components + ['menu_showcase', 'reservation_form', 'chef_profile', 'location_map']
        if industry == 'portfolio':
            return base_components + ['portfolio_gallery', 'case_study', 'skills_section', 'resume_download']
        if industry == 'ecommerce':
            return base_components + ['product_catalog', 'shopping_cart', 'checkout_form', 'order_tracking']
        if industry == 'blog':
            return base_components + ['post_list', 'newsletter_signup', 'author_bio', 'comments_section']
        if industry == 'corporate':
            return base_components + ['investor_section', 'careers_section', 'press_section', 'leadership_team']
        return base_components