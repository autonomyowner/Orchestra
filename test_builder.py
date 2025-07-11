#!/usr/bin/env python3
"""
Test script for the Ultimate Website Builder
"""

import asyncio
from ultimate_website_builder import UltimateWebsiteBuilder

async def test_builder():
    """Test the basic functionality of the Ultimate Website Builder"""
    
    print("🧪 Testing Ultimate Website Builder...")
    
    # Initialize builder
    builder = UltimateWebsiteBuilder()
    
    # Test initialization
    print("✅ Builder initialized successfully")
    
    # Test design system
    design_system = builder.design_system
    colors = design_system.get_color_system()
    print(f"✅ Design system working - Primary color: {colors['primary']}")
    
    # Test component library
    components = builder.component_library.get_components_for_industry("restaurant")
    print(f"✅ Component library working - Restaurant components: {len(components)}")
    
    # Test template system
    template = builder.template_system.get_industry_template("portfolio")
    print(f"✅ Template system working - Portfolio template: {template['name']}")
    
    print("\n🎉 All systems working correctly!")
    print("Ready to run: python ultimate_website_builder.py")

if __name__ == "__main__":
    asyncio.run(test_builder())