#!/usr/bin/env python3
"""
API Integration System for +++A Project Builder 2030
- Third-party service integrations
- Authentication providers
- Payment processing
- Analytics and monitoring
"""

import os
import json
import requests
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import stripe
from rich.console import Console

console = Console()

class ServiceType(Enum):
    """Types of integrated services"""
    AUTHENTICATION = "auth"
    PAYMENT = "payment"
    ANALYTICS = "analytics"
    EMAIL = "email"
    STORAGE = "storage"
    DATABASE = "database"
    MONITORING = "monitoring"
    CDN = "cdn"
    DEPLOYMENT = "deployment"

@dataclass
class ServiceConfig:
    """Configuration for third-party services"""
    name: str
    service_type: ServiceType
    api_key: str
    endpoint: str
    documentation_url: str
    integration_complexity: str  # 'simple', 'medium', 'complex'
    pricing_model: str
    features: List[str]

class APIIntegrationManager:
    """Manages all third-party API integrations"""
    
    def __init__(self):
        self.services = self._initialize_services()
        self.console = console
    
    def _initialize_services(self) -> Dict[str, ServiceConfig]:
        """Initialize supported third-party services"""
        return {
            # Authentication Services
            "auth0": ServiceConfig(
                name="Auth0",
                service_type=ServiceType.AUTHENTICATION,
                api_key="",
                endpoint="https://dev-{domain}.auth0.com",
                documentation_url="https://auth0.com/docs",
                integration_complexity="medium",
                pricing_model="freemium",
                features=["SSO", "Social Login", "MFA", "User Management"]
            ),
            "firebase_auth": ServiceConfig(
                name="Firebase Authentication",
                service_type=ServiceType.AUTHENTICATION,
                api_key="",
                endpoint="https://identitytoolkit.googleapis.com",
                documentation_url="https://firebase.google.com/docs/auth",
                integration_complexity="simple",
                pricing_model="pay_per_use",
                features=["Email/Password", "Social Login", "Phone Auth", "Anonymous Auth"]
            ),
            "clerk": ServiceConfig(
                name="Clerk",
                service_type=ServiceType.AUTHENTICATION,
                api_key="",
                endpoint="https://api.clerk.dev",
                documentation_url="https://clerk.com/docs",
                integration_complexity="simple",
                pricing_model="freemium",
                features=["Complete Auth UI", "User Management", "Organizations", "Webhooks"]
            ),
            
            # Payment Services
            "stripe": ServiceConfig(
                name="Stripe",
                service_type=ServiceType.PAYMENT,
                api_key="",
                endpoint="https://api.stripe.com",
                documentation_url="https://stripe.com/docs",
                integration_complexity="medium",
                pricing_model="transaction_fee",
                features=["Payments", "Subscriptions", "Invoicing", "Connect", "Terminal"]
            ),
            "paypal": ServiceConfig(
                name="PayPal",
                service_type=ServiceType.PAYMENT,
                api_key="",
                endpoint="https://api.paypal.com",
                documentation_url="https://developer.paypal.com/docs",
                integration_complexity="medium",
                pricing_model="transaction_fee",
                features=["Payments", "Subscriptions", "Payouts", "Invoicing"]
            ),
            "lemonsqueezy": ServiceConfig(
                name="Lemon Squeezy",
                service_type=ServiceType.PAYMENT,
                api_key="",
                endpoint="https://api.lemonsqueezy.com",
                documentation_url="https://docs.lemonsqueezy.com",
                integration_complexity="simple",
                pricing_model="transaction_fee",
                features=["Digital Products", "Subscriptions", "Tax Handling", "Analytics"]
            ),
            
            # Analytics Services
            "google_analytics": ServiceConfig(
                name="Google Analytics 4",
                service_type=ServiceType.ANALYTICS,
                api_key="",
                endpoint="https://www.googletagmanager.com",
                documentation_url="https://developers.google.com/analytics",
                integration_complexity="medium",
                pricing_model="free",
                features=["Web Analytics", "App Analytics", "E-commerce", "Custom Events"]
            ),
            "mixpanel": ServiceConfig(
                name="Mixpanel",
                service_type=ServiceType.ANALYTICS,
                api_key="",
                endpoint="https://api.mixpanel.com",
                documentation_url="https://developer.mixpanel.com",
                integration_complexity="simple",
                pricing_model="freemium",
                features=["Event Tracking", "User Analytics", "Cohort Analysis", "A/B Testing"]
            ),
            "posthog": ServiceConfig(
                name="PostHog",
                service_type=ServiceType.ANALYTICS,
                api_key="",
                endpoint="https://app.posthog.com",
                documentation_url="https://posthog.com/docs",
                integration_complexity="simple",
                pricing_model="freemium",
                features=["Product Analytics", "Feature Flags", "Session Replay", "A/B Testing"]
            ),
            
            # Email Services
            "resend": ServiceConfig(
                name="Resend",
                service_type=ServiceType.EMAIL,
                api_key="",
                endpoint="https://api.resend.com",
                documentation_url="https://resend.com/docs",
                integration_complexity="simple",
                pricing_model="freemium",
                features=["Transactional Email", "Marketing Email", "Webhooks", "Analytics"]
            ),
            "sendgrid": ServiceConfig(
                name="SendGrid",
                service_type=ServiceType.EMAIL,
                api_key="",
                endpoint="https://api.sendgrid.com",
                documentation_url="https://docs.sendgrid.com",
                integration_complexity="medium",
                pricing_model="freemium",
                features=["Email API", "Marketing Campaigns", "Templates", "Analytics"]
            ),
            
            # Storage Services
            "supabase": ServiceConfig(
                name="Supabase",
                service_type=ServiceType.STORAGE,
                api_key="",
                endpoint="https://api.supabase.io",
                documentation_url="https://supabase.com/docs",
                integration_complexity="simple",
                pricing_model="freemium",
                features=["Database", "Storage", "Auth", "Real-time", "Edge Functions"]
            ),
            "aws_s3": ServiceConfig(
                name="AWS S3",
                service_type=ServiceType.STORAGE,
                api_key="",
                endpoint="https://s3.amazonaws.com",
                documentation_url="https://docs.aws.amazon.com/s3",
                integration_complexity="complex",
                pricing_model="pay_per_use",
                features=["Object Storage", "CDN", "Data Lake", "Backup", "Archive"]
            ),
            
            # Monitoring Services
            "sentry": ServiceConfig(
                name="Sentry",
                service_type=ServiceType.MONITORING,
                api_key="",
                endpoint="https://sentry.io/api",
                documentation_url="https://docs.sentry.io",
                integration_complexity="simple",
                pricing_model="freemium",
                features=["Error Monitoring", "Performance", "Release Health", "Alerts"]
            ),
            "datadog": ServiceConfig(
                name="Datadog",
                service_type=ServiceType.MONITORING,
                api_key="",
                endpoint="https://api.datadoghq.com",
                documentation_url="https://docs.datadoghq.com",
                integration_complexity="complex",
                pricing_model="subscription",
                features=["Infrastructure", "APM", "Logs", "Synthetics", "Security"]
            ),
        }
    
    def generate_integration_code(self, service_name: str, project_type: str = "nextjs") -> Dict[str, str]:
        """Generate integration code for a specific service"""
        
        if service_name not in self.services:
            raise ValueError(f"Service {service_name} not supported")
        
        service = self.services[service_name]
        
        self.console.print(f"🔌 Generating {service.name} integration for {project_type}")
        
        if service_name == "stripe":
            return self._generate_stripe_integration(project_type)
        elif service_name == "auth0":
            return self._generate_auth0_integration(project_type)
        elif service_name == "firebase_auth":
            return self._generate_firebase_auth_integration(project_type)
        elif service_name == "clerk":
            return self._generate_clerk_integration(project_type)
        elif service_name == "resend":
            return self._generate_resend_integration(project_type)
        elif service_name == "supabase":
            return self._generate_supabase_integration(project_type)
        elif service_name == "google_analytics":
            return self._generate_ga4_integration(project_type)
        elif service_name == "sentry":
            return self._generate_sentry_integration(project_type)
        else:
            return self._generate_generic_integration(service, project_type)
    
    def _generate_stripe_integration(self, project_type: str) -> Dict[str, str]:
        """Generate Stripe payment integration"""
        
        if project_type == "nextjs":
            return {
                "package.json": '''
{
  "dependencies": {
    "stripe": "^14.0.0",
    "@stripe/stripe-js": "^2.0.0"
  }
}''',
                "lib/stripe.ts": '''
import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
});

export const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);
''',
                "pages/api/create-payment-intent.ts": '''
import { NextApiRequest, NextApiResponse } from 'next';
import { stripe } from '../../lib/stripe';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    try {
      const { amount, currency = 'usd' } = req.body;
      
      const paymentIntent = await stripe.paymentIntents.create({
        amount: amount * 100, // Convert to cents
        currency,
        automatic_payment_methods: {
          enabled: true,
        },
      });
      
      res.status(200).json({ clientSecret: paymentIntent.client_secret });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end('Method Not Allowed');
  }
}
''',
                "components/CheckoutForm.tsx": '''
import { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import {
  Elements,
  CardElement,
  useStripe,
  useElements
} from '@stripe/react-stripe-js';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

function CheckoutForm({ amount }: { amount: number }) {
  const stripe = useStripe();
  const elements = useElements();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    if (!stripe || !elements) return;
    
    setLoading(true);
    
    // Create payment intent
    const response = await fetch('/api/create-payment-intent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount }),
    });
    
    const { clientSecret } = await response.json();
    
    // Confirm payment
    const result = await stripe.confirmCardPayment(clientSecret, {
      payment_method: {
        card: elements.getElement(CardElement)!,
      }
    });
    
    if (result.error) {
      console.error(result.error.message);
    } else {
      console.log('Payment succeeded!');
    }
    
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto p-6">
      <CardElement className="p-3 border rounded-md" />
      <button
        type="submit"
        disabled={!stripe || loading}
        className="w-full mt-4 bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? 'Processing...' : `Pay $${amount}`}
      </button>
    </form>
  );
}

export default function CheckoutPage() {
  return (
    <Elements stripe={stripePromise}>
      <CheckoutForm amount={99} />
    </Elements>
  );
}
''',
                ".env.example": '''
STRIPE_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
''',
                "README.md": '''
# Stripe Integration

## Setup
1. Get your API keys from https://dashboard.stripe.com/test/apikeys
2. Add them to your .env.local file
3. Test payments with card number: 4242 4242 4242 4242

## Features
- Payment processing
- Subscription management
- Webhook handling
- Customer portal
'''
            }
        
        return {}
    
    def _generate_auth0_integration(self, project_type: str) -> Dict[str, str]:
        """Generate Auth0 authentication integration"""
        
        if project_type == "nextjs":
            return {
                "package.json": '''
{
  "dependencies": {
    "@auth0/nextjs-auth0": "^3.0.0"
  }
}''',
                "pages/api/auth/[...auth0].ts": '''
import { handleAuth } from '@auth0/nextjs-auth0';

export default handleAuth();
''',
                "lib/auth0.ts": '''
import { initAuth0 } from '@auth0/nextjs-auth0';

export default initAuth0({
  domain: process.env.AUTH0_DOMAIN!,
  clientId: process.env.AUTH0_CLIENT_ID!,
  clientSecret: process.env.AUTH0_CLIENT_SECRET!,
  scope: 'openid profile email',
  redirectUri: process.env.AUTH0_REDIRECT_URI!,
  postLogoutRedirectUri: process.env.AUTH0_POST_LOGOUT_REDIRECT_URI!,
  session: {
    cookieSecret: process.env.AUTH0_COOKIE_SECRET!,
  },
});
''',
                "components/LoginButton.tsx": '''
import { useUser } from '@auth0/nextjs-auth0/client';

export default function LoginButton() {
  const { user, error, isLoading } = useUser();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>{error.message}</div>;

  if (user) {
    return (
      <div className="flex items-center space-x-4">
        <img src={user.picture} alt={user.name} className="w-8 h-8 rounded-full" />
        <span>{user.name}</span>
        <a href="/api/auth/logout" className="text-red-600 hover:underline">
          Logout
        </a>
      </div>
    );
  }

  return (
    <a href="/api/auth/login" className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
      Login
    </a>
  );
}
''',
                ".env.example": '''
AUTH0_DOMAIN=your-domain.auth0.com
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
AUTH0_COOKIE_SECRET=a-long-random-string
AUTH0_REDIRECT_URI=http://localhost:3000/api/auth/callback
AUTH0_POST_LOGOUT_REDIRECT_URI=http://localhost:3000
'''
            }
        
        return {}
    
    def _generate_resend_integration(self, project_type: str) -> Dict[str, str]:
        """Generate Resend email integration"""
        
        if project_type == "nextjs":
            return {
                "package.json": '''
{
  "dependencies": {
    "resend": "^2.0.0"
  }
}''',
                "lib/resend.ts": '''
import { Resend } from 'resend';

export const resend = new Resend(process.env.RESEND_API_KEY);
''',
                "pages/api/send-email.ts": '''
import { NextApiRequest, NextApiResponse } from 'next';
import { resend } from '../../lib/resend';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    try {
      const { to, subject, html } = req.body;
      
      const data = await resend.emails.send({
        from: 'noreply@yourdomain.com',
        to,
        subject,
        html,
      });
      
      res.status(200).json({ success: true, id: data.id });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end('Method Not Allowed');
  }
}
''',
                "components/ContactForm.tsx": '''
import { useState } from 'react';

export default function ContactForm() {
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [sending, setSending] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSending(true);

    try {
      const response = await fetch('/api/send-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          to: 'contact@yourdomain.com',
          subject: `Contact from ${formData.name}`,
          html: `
            <h2>New Contact Form Submission</h2>
            <p><strong>Name:</strong> ${formData.name}</p>
            <p><strong>Email:</strong> ${formData.email}</p>
            <p><strong>Message:</strong> ${formData.message}</p>
          `,
        }),
      });

      if (response.ok) {
        alert('Email sent successfully!');
        setFormData({ name: '', email: '', message: '' });
      }
    } catch (error) {
      alert('Failed to send email');
    }

    setSending(false);
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-lg mx-auto space-y-4">
      <input
        type="text"
        placeholder="Name"
        value={formData.name}
        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
        className="w-full p-3 border rounded-md"
        required
      />
      <input
        type="email"
        placeholder="Email"
        value={formData.email}
        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        className="w-full p-3 border rounded-md"
        required
      />
      <textarea
        placeholder="Message"
        value={formData.message}
        onChange={(e) => setFormData({ ...formData, message: e.target.value })}
        className="w-full p-3 border rounded-md h-32"
        required
      />
      <button
        type="submit"
        disabled={sending}
        className="w-full bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {sending ? 'Sending...' : 'Send Message'}
      </button>
    </form>
  );
}
''',
                ".env.example": '''
RESEND_API_KEY=re_...
'''
            }
        
        return {}
    
    def _generate_generic_integration(self, service: ServiceConfig, project_type: str) -> Dict[str, str]:
        """Generate generic integration template"""
        
        return {
            "README.md": f'''
# {service.name} Integration

## Overview
- **Service Type**: {service.service_type.value}
- **Complexity**: {service.integration_complexity}
- **Pricing**: {service.pricing_model}
- **Documentation**: {service.documentation_url}

## Features
{chr(10).join(f"- {feature}" for feature in service.features)}

## Setup
1. Sign up at {service.documentation_url}
2. Get your API key
3. Add to environment variables
4. Follow integration guide

## Environment Variables
```
{service.name.upper()}_API_KEY=your-api-key
{service.name.upper()}_ENDPOINT={service.endpoint}
```
''',
            ".env.example": f'''
{service.name.upper()}_API_KEY=your-api-key
{service.name.upper()}_ENDPOINT={service.endpoint}
'''
        }
    
    def get_recommended_services(self, project_type: str, budget: str = "startup") -> Dict[str, List[str]]:
        """Get recommended services for a project type and budget"""
        
        recommendations = {
            "saas": {
                "auth": ["clerk", "auth0", "firebase_auth"],
                "payment": ["stripe", "lemonsqueezy"],
                "analytics": ["google_analytics", "posthog", "mixpanel"],
                "email": ["resend", "sendgrid"],
                "database": ["supabase", "planetscale"],
                "monitoring": ["sentry", "datadog"]
            },
            "ecommerce": {
                "auth": ["auth0", "clerk"],
                "payment": ["stripe", "paypal"],
                "analytics": ["google_analytics", "mixpanel"],
                "email": ["sendgrid", "resend"],
                "storage": ["aws_s3", "supabase"],
                "monitoring": ["sentry"]
            },
            "marketplace": {
                "auth": ["auth0", "clerk"],
                "payment": ["stripe"],
                "analytics": ["mixpanel", "posthog"],
                "email": ["sendgrid"],
                "storage": ["aws_s3"],
                "monitoring": ["sentry", "datadog"]
            },
            "portfolio": {
                "analytics": ["google_analytics"],
                "email": ["resend"],
                "storage": ["supabase"],
                "monitoring": ["sentry"]
            }
        }
        
        # Filter by budget
        if budget == "startup":
            # Prefer free/freemium services
            budget_filter = ["freemium", "free", "pay_per_use"]
        elif budget == "business":
            budget_filter = ["freemium", "subscription", "transaction_fee"]
        else:  # enterprise
            budget_filter = ["subscription", "enterprise", "transaction_fee"]
        
        return recommendations.get(project_type, {})
    
    def generate_integration_guide(self, services: List[str], project_type: str) -> str:
        """Generate complete integration guide for multiple services"""
        
        guide = f"""
# API Integration Guide for {project_type.title()} Project

## Services Integration Plan

"""
        
        for service_name in services:
            if service_name in self.services:
                service = self.services[service_name]
                guide += f"""
### {service.name}
- **Type**: {service.service_type.value.title()}
- **Complexity**: {service.integration_complexity.title()}
- **Pricing**: {service.pricing_model.replace('_', ' ').title()}
- **Features**: {', '.join(service.features)}
- **Docs**: {service.documentation_url}

"""
        
        guide += """
## Integration Steps

1. **Setup Environment Variables**
   ```bash
   cp .env.example .env.local
   # Add your API keys
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Configure Each Service**
   - Follow individual service setup guides
   - Test in development environment
   - Deploy to production

4. **Testing**
   - Unit tests for API integrations
   - End-to-end testing
   - Load testing for production

## Best Practices

- Use environment variables for all API keys
- Implement proper error handling
- Add rate limiting and caching
- Monitor API usage and costs
- Set up alerts for failures
- Document all integrations

## Security Considerations

- Never expose API keys in client-side code
- Use HTTPS for all API calls
- Implement request validation
- Set up CORS properly
- Regular security audits

"""
        
        return guide

# Example usage
if __name__ == "__main__":
    manager = APIIntegrationManager()
    
    # Get recommendations for a SaaS project
    recommendations = manager.get_recommended_services("saas", "startup")
    console.print("🎯 Recommended services for SaaS startup:", recommendations)
    
    # Generate Stripe integration
    stripe_integration = manager.generate_integration_code("stripe", "nextjs")
    console.print("💳 Generated Stripe integration files")
    
    # Generate complete integration guide
    services = ["stripe", "auth0", "resend", "google_analytics"]
    guide = manager.generate_integration_guide(services, "saas")
    console.print("📋 Generated integration guide") 