"""
Project Templates Module
Pre-built project specifications for common application types.
"""

from .base_template import BaseTemplate
from .saas_template import SAASProjectTemplate
from .ecommerce_template import EcommerceProjectTemplate
from .blog_template import BlogProjectTemplate
from .portfolio_template import PortfolioProjectTemplate
from .dashboard_template import DashboardProjectTemplate
from .social_template import SocialProjectTemplate

__all__ = [
    'BaseTemplate',
    'SAASProjectTemplate', 
    'EcommerceProjectTemplate',
    'BlogProjectTemplate',
    'PortfolioProjectTemplate',
    'DashboardProjectTemplate',
    'SocialProjectTemplate'
] 