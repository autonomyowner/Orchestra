class ProfessionalDesignSystem:
    def get_spacing_system(self):
        return "8px grid system with generous whitespace and consistent rhythm"
    def get_typography_system(self, style=None):
        return {
            'default': 'Inter, system-ui, sans-serif',
            'serif': 'Merriweather, serif',
            'display': 'Montserrat, Inter',
            'line_height': 1.6,
            'scales': [12, 14, 16, 20, 24, 32, 40, 56, 72]
        }
    def get_color_system(self, palette=None):
        return {
            'primary': '#2563eb',
            'secondary': '#64748b',
            'accent': '#f59e0b',
            'background': '#fff',
            'surface': '#f8fafc',
            'text': '#1e293b',
            'muted': '#94a3b8',
            'error': '#ef4444',
            'success': '#22c55e',
            'warning': '#f59e0b',
            'info': '#0ea5e9'
        }
    def get_industry_components(self, industry):
        return [
            'hero_section', 'navigation_bar', 'about_section', 'services_showcase',
            'testimonials', 'contact_form', 'footer', 'cta_banner', 'gallery', 'pricing',
            'blog_preview', 'faq', 'features_grid', 'team_section', 'micro_interactions'
        ]
    def get_accessibility_features(self):
        return ['WCAG AA compliance', 'keyboard navigation', 'focus indicators', 'aria labels', 'alt text']
    def get_performance_optimizations(self):
        return ['image optimization', 'code splitting', 'lazy loading', 'caching', 'core web vitals']
    def get_micro_interactions(self, personality=None):
        return ['smooth page transitions', 'hover effects', 'scroll animations', 'loading states', 'interactive elements']