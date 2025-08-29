#!/usr/bin/env python3
"""Test script for the new theme loading system."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.theme_loader import ThemeLoader
from colorama import init

# Initialize colorama
init()

def test_theme_loader():
    """Test the theme loading functionality."""
    print("🧪 Testing Theme Loader System...")
    print("=" * 50)
    
    # Initialize theme loader
    loader = ThemeLoader()
    
    print("\n📊 Theme Loading Results:")
    print("-" * 30)
    
    # Get available themes
    themes = loader.get_available_themes()
    print(f"Total themes loaded: {len(themes)}")
    
    # Get themes by source
    themes_by_source = loader.get_themes_by_source()
    print(f"Default themes: {len(themes_by_source['default'])}")
    print(f"Custom themes: {len(themes_by_source['custom'])}")
    
    print("\n🎭 Available Themes:")
    print("-" * 30)
    for theme_name in sorted(themes):
        theme_data = loader.get_theme(theme_name)
        source = theme_data.get('_source', 'unknown')
        emoji = theme_data.get('emoji', '🎭')
        display_name = theme_data.get('display_name', theme_name)
        print(f"  {emoji} {theme_name} ({source}) - {display_name}")
    
    print("\n📁 Directory Structure:")
    print("-" * 30)
    print(f"Default themes dir: {loader.default_themes_dir}")
    print(f"Custom themes dir: {loader.custom_themes_dir}")
    print(f"Default dir exists: {loader.default_themes_dir.exists()}")
    print(f"Custom dir exists: {loader.custom_themes_dir.exists()}")
    
    # Test theme retrieval
    print("\n🔍 Testing Theme Retrieval:")
    print("-" * 30)
    test_theme = "medieval"
    theme_data = loader.get_theme(test_theme)
    if theme_data:
        print(f"✅ Successfully retrieved '{test_theme}' theme")
        print(f"   Vocabulary count: {len(theme_data.get('vocabulary', []))}")
        print(f"   Metaphors count: {len(theme_data.get('metaphors', []))}")
        print(f"   Source: {theme_data.get('_source', 'unknown')}")
    else:
        print(f"❌ Failed to retrieve '{test_theme}' theme")
    
    print("\n✅ Theme Loader Test Complete!")

if __name__ == "__main__":
    test_theme_loader()
