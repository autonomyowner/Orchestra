"""
E-commerce Project Template
Complete e-commerce application with product management, cart, and payments.
"""

from typing import Dict, Any, List
from .base_template import BaseTemplate

class EcommerceProjectTemplate(BaseTemplate):
    """E-commerce application template with comprehensive features."""
    
    def __init__(self, project_name: str, description: str = ""):
        super().__init__(project_name, description or f"An e-commerce platform for {project_name}")
        self.payment_provider = "stripe"
        self.has_inventory = True
        self.has_reviews = True
    
    def get_features(self) -> List[str]:
        """Return e-commerce-specific features."""
        return [
            "product_catalog",
            "shopping_cart",
            "checkout_process",
            "payment_processing",
            "order_management",
            "inventory_tracking",
            "product_reviews",
            "wishlist",
            "search_filtering",
            "user_accounts",
            "admin_dashboard",
            "email_notifications",
            "shipping_calculator",
            "discount_codes",
            "analytics_tracking"
        ]
    
    def get_pages(self) -> List[str]:
        """Return e-commerce-specific pages."""
        return [
            "Home",
            "Products",
            "Product Details",
            "Category",
            "Search Results",
            "Cart",
            "Checkout",
            "Order Confirmation",
            "Account",
            "Orders",
            "Wishlist",
            "Reviews",
            "About",
            "Contact",
            "Admin Dashboard",
            "Product Management",
            "Order Management",
            "Customer Management"
        ]
    
    def get_integrations(self) -> List[str]:
        """Return e-commerce-specific integrations."""
        return [
            "stripe",
            "sendgrid",
            "cloudinary",
            "google_analytics",
            "facebook_pixel",
            "shopify_analytics",
            "mailchimp"
        ]
    
    def get_database_schema(self) -> List[Dict[str, Any]]:
        """Return e-commerce-specific database schema."""
        base_schema = super().get_database_schema()
        
        ecommerce_schema = [
            {
                "name": "Product",
                "fields": [
                    {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                    {"name": "name", "type": "string", "required": True, "description": "Product name"},
                    {"name": "description", "type": "text", "required": True, "description": "Product description"},
                    {"name": "price", "type": "decimal", "required": True, "description": "Product price"},
                    {"name": "comparePrice", "type": "decimal", "required": False, "description": "Compare at price"},
                    {"name": "images", "type": "json", "required": True, "description": "Product images"},
                    {"name": "categoryId", "type": "string", "required": True, "description": "Category ID"},
                    {"name": "sku", "type": "string", "required": True, "description": "Stock keeping unit"},
                    {"name": "inventory", "type": "integer", "required": True, "description": "Stock quantity"},
                    {"name": "isActive", "type": "boolean", "required": True, "description": "Product active status"},
                    {"name": "createdAt", "type": "datetime", "required": True, "description": "Creation date"},
                    {"name": "updatedAt", "type": "datetime", "required": True, "description": "Last update date"}
                ],
                "relationships": [
                    {"type": "manyToOne", "with": "Category", "field": "categoryId"},
                    {"type": "oneToMany", "with": "Review", "field": "productId"}
                ]
            },
            {
                "name": "Category",
                "fields": [
                    {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                    {"name": "name", "type": "string", "required": True, "description": "Category name"},
                    {"name": "slug", "type": "string", "required": True, "description": "Category slug"},
                    {"name": "description", "type": "text", "required": False, "description": "Category description"},
                    {"name": "image", "type": "string", "required": False, "description": "Category image"},
                    {"name": "parentId", "type": "string", "required": False, "description": "Parent category ID"},
                    {"name": "createdAt", "type": "datetime", "required": True, "description": "Creation date"},
                    {"name": "updatedAt", "type": "datetime", "required": True, "description": "Last update date"}
                ],
                "relationships": [
                    {"type": "oneToMany", "with": "Product", "field": "categoryId"},
                    {"type": "manyToOne", "with": "Category", "field": "parentId"}
                ]
            },
            {
                "name": "Order",
                "fields": [
                    {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                    {"name": "userId", "type": "string", "required": True, "description": "User ID"},
                    {"name": "orderNumber", "type": "string", "required": True, "description": "Order number"},
                    {"name": "status", "type": "string", "required": True, "description": "Order status"},
                    {"name": "subtotal", "type": "decimal", "required": True, "description": "Order subtotal"},
                    {"name": "tax", "type": "decimal", "required": True, "description": "Tax amount"},
                    {"name": "shipping", "type": "decimal", "required": True, "description": "Shipping cost"},
                    {"name": "total", "type": "decimal", "required": True, "description": "Total amount"},
                    {"name": "shippingAddress", "type": "json", "required": True, "description": "Shipping address"},
                    {"name": "billingAddress", "type": "json", "required": True, "description": "Billing address"},
                    {"name": "paymentIntentId", "type": "string", "required": True, "description": "Stripe payment intent"},
                    {"name": "createdAt", "type": "datetime", "required": True, "description": "Creation date"},
                    {"name": "updatedAt", "type": "datetime", "required": True, "description": "Last update date"}
                ],
                "relationships": [
                    {"type": "manyToOne", "with": "User", "field": "userId"},
                    {"type": "oneToMany", "with": "OrderItem", "field": "orderId"}
                ]
            },
            {
                "name": "OrderItem",
                "fields": [
                    {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                    {"name": "orderId", "type": "string", "required": True, "description": "Order ID"},
                    {"name": "productId", "type": "string", "required": True, "description": "Product ID"},
                    {"name": "quantity", "type": "integer", "required": True, "description": "Quantity ordered"},
                    {"name": "price", "type": "decimal", "required": True, "description": "Price at time of order"},
                    {"name": "createdAt", "type": "datetime", "required": True, "description": "Creation date"}
                ],
                "relationships": [
                    {"type": "manyToOne", "with": "Order", "field": "orderId"},
                    {"type": "manyToOne", "with": "Product", "field": "productId"}
                ]
            },
            {
                "name": "Review",
                "fields": [
                    {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                    {"name": "productId", "type": "string", "required": True, "description": "Product ID"},
                    {"name": "userId", "type": "string", "required": True, "description": "User ID"},
                    {"name": "rating", "type": "integer", "required": True, "description": "Rating (1-5)"},
                    {"name": "title", "type": "string", "required": True, "description": "Review title"},
                    {"name": "comment", "type": "text", "required": True, "description": "Review comment"},
                    {"name": "isVerified", "type": "boolean", "required": True, "description": "Verified purchase"},
                    {"name": "createdAt", "type": "datetime", "required": True, "description": "Creation date"},
                    {"name": "updatedAt", "type": "datetime", "required": True, "description": "Last update date"}
                ],
                "relationships": [
                    {"type": "manyToOne", "with": "Product", "field": "productId"},
                    {"type": "manyToOne", "with": "User", "field": "userId"}
                ]
            },
            {
                "name": "Wishlist",
                "fields": [
                    {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                    {"name": "userId", "type": "string", "required": True, "description": "User ID"},
                    {"name": "productId", "type": "string", "required": True, "description": "Product ID"},
                    {"name": "createdAt", "type": "datetime", "required": True, "description": "Creation date"}
                ],
                "relationships": [
                    {"type": "manyToOne", "with": "User", "field": "userId"},
                    {"type": "manyToOne", "with": "Product", "field": "productId"}
                ]
            }
        ]
        
        return base_schema + ecommerce_schema
    
    def get_api_routes(self) -> List[Dict[str, Any]]:
        """Return e-commerce-specific API routes."""
        base_routes = super().get_api_routes()
        
        ecommerce_routes = [
            # Product routes
            {"method": "GET", "path": "/api/products", "description": "Get products with filters", "authentication_required": False},
            {"method": "GET", "path": "/api/products/[id]", "description": "Get product details", "authentication_required": False},
            {"method": "POST", "path": "/api/products", "description": "Create product (admin)", "authentication_required": True},
            {"method": "PUT", "path": "/api/products/[id]", "description": "Update product (admin)", "authentication_required": True},
            {"method": "DELETE", "path": "/api/products/[id]", "description": "Delete product (admin)", "authentication_required": True},
            
            # Category routes
            {"method": "GET", "path": "/api/categories", "description": "Get categories", "authentication_required": False},
            {"method": "GET", "path": "/api/categories/[id]/products", "description": "Get products by category", "authentication_required": False},
            
            # Cart routes
            {"method": "GET", "path": "/api/cart", "description": "Get user cart", "authentication_required": True},
            {"method": "POST", "path": "/api/cart/add", "description": "Add item to cart", "authentication_required": True},
            {"method": "PUT", "path": "/api/cart/update", "description": "Update cart item", "authentication_required": True},
            {"method": "DELETE", "path": "/api/cart/remove", "description": "Remove item from cart", "authentication_required": True},
            {"method": "DELETE", "path": "/api/cart/clear", "description": "Clear cart", "authentication_required": True},
            
            # Order routes
            {"method": "POST", "path": "/api/orders", "description": "Create order", "authentication_required": True},
            {"method": "GET", "path": "/api/orders", "description": "Get user orders", "authentication_required": True},
            {"method": "GET", "path": "/api/orders/[id]", "description": "Get order details", "authentication_required": True},
            {"method": "PUT", "path": "/api/orders/[id]/status", "description": "Update order status (admin)", "authentication_required": True},
            
            # Payment routes
            {"method": "POST", "path": "/api/payment/create-intent", "description": "Create payment intent", "authentication_required": True},
            {"method": "POST", "path": "/api/payment/confirm", "description": "Confirm payment", "authentication_required": True},
            {"method": "POST", "path": "/api/payment/webhook", "description": "Stripe webhook", "authentication_required": False},
            
            # Review routes
            {"method": "GET", "path": "/api/products/[id]/reviews", "description": "Get product reviews", "authentication_required": False},
            {"method": "POST", "path": "/api/products/[id]/reviews", "description": "Create review", "authentication_required": True},
            {"method": "PUT", "path": "/api/reviews/[id]", "description": "Update review", "authentication_required": True},
            {"method": "DELETE", "path": "/api/reviews/[id]", "description": "Delete review", "authentication_required": True},
            
            # Wishlist routes
            {"method": "GET", "path": "/api/wishlist", "description": "Get user wishlist", "authentication_required": True},
            {"method": "POST", "path": "/api/wishlist/add", "description": "Add to wishlist", "authentication_required": True},
            {"method": "DELETE", "path": "/api/wishlist/remove", "description": "Remove from wishlist", "authentication_required": True},
            
            # Search routes
            {"method": "GET", "path": "/api/search", "description": "Search products", "authentication_required": False},
            
            # Admin routes
            {"method": "GET", "path": "/api/admin/orders", "description": "Get all orders (admin)", "authentication_required": True},
            {"method": "GET", "path": "/api/admin/products", "description": "Get all products (admin)", "authentication_required": True},
            {"method": "GET", "path": "/api/admin/analytics", "description": "Get sales analytics (admin)", "authentication_required": True}
        ]
        
        return base_routes + ecommerce_routes
    
    def get_environment_variables(self) -> List[Dict[str, str]]:
        """Return e-commerce-specific environment variables."""
        base_vars = super().get_environment_variables()
        
        ecommerce_vars = [
            {"name": "STRIPE_SECRET_KEY", "description": "Stripe secret key"},
            {"name": "STRIPE_PUBLISHABLE_KEY", "description": "Stripe publishable key"},
            {"name": "STRIPE_WEBHOOK_SECRET", "description": "Stripe webhook secret"},
            {"name": "SENDGRID_API_KEY", "description": "SendGrid API key for order emails"},
            {"name": "SENDGRID_FROM_EMAIL", "description": "SendGrid from email address"},
            {"name": "CLOUDINARY_URL", "description": "Cloudinary URL for product images"},
            {"name": "GOOGLE_ANALYTICS_ID", "description": "Google Analytics tracking ID"},
            {"name": "FACEBOOK_PIXEL_ID", "description": "Facebook Pixel ID for tracking"},
            {"name": "MAILCHIMP_API_KEY", "description": "Mailchimp API key for newsletters"}
        ]
        
        return base_vars + ecommerce_vars
    
    def get_dependencies(self) -> Dict[str, List[str]]:
        """Return e-commerce-specific dependencies."""
        base_deps = super().get_dependencies()
        
        ecommerce_deps = {
            "dependencies": base_deps["dependencies"] + [
                "stripe@^12.0.0",
                "@stripe/stripe-js@^1.54.0",
                "sendgrid@^7.7.0",
                "cloudinary@^1.37.0",
                "react-hot-toast@^2.4.0",
                "react-image-gallery@^1.2.11",
                "react-rating-stars-component@^2.2.5",
                "react-slick@^0.29.0",
                "slick-carousel@^1.8.1",
                "zod@^3.22.0",
                "react-hook-form@^7.47.0",
                "framer-motion@^10.16.0"
            ],
            "devDependencies": base_deps["devDependencies"] + [
                "@types/stripe@^8.0.417",
                "@types/react-slick@^0.23.10"
            ]
        }
        
        return ecommerce_deps
    
    def get_project_spec(self) -> Dict[str, Any]:
        """Return complete e-commerce project specification."""
        return {
            "project_name": self.project_name,
            "description": self.description,
            "purpose": "ecommerce",
            "target_audience": "shoppers",
            "design_style": "modern",
            "color_scheme": "green",
            "mobile_first": True,
            "pages": self.get_pages(),
            "auth_required": True,
            "auth_methods": "email",
            "features": self.get_features(),
            "database_type": "postgresql",
            "deployment_preference": "vercel",
            "third_party_integrations": self.get_integrations(),
            "expected_users": "1000-50000",
            "performance_priority": "conversion",
            "seo_important": True,
            "analytics_required": True,
            "cms_needed": False,
            "multi_language": False,
            "custom_requirements": "E-commerce platform with product management, cart, checkout, and payment processing",
            "budget_tier": "medium",
            "technical_stack": self.get_technical_stack(),
            "database_schema": self.get_database_schema(),
            "api_routes": self.get_api_routes(),
            "environment_variables": self.get_environment_variables(),
            "dependencies": self.get_dependencies(),
            "scripts": self.get_scripts(),
            "file_structure": self.get_file_structure(),
            "quality_standards": self.get_quality_standards()
        } 