#!/usr/bin/env python3
"""
API Key Setup Helper for Anime Story Generator
This script helps you get free API keys for the anime story generator.
"""

import os
import webbrowser
from pathlib import Path

def create_secrets_file():
    """Create secrets.toml file with template"""
    streamlit_dir = Path(".streamlit")
    streamlit_dir.mkdir(exist_ok=True)
    
    secrets_file = streamlit_dir / "secrets.toml"
    template_file = streamlit_dir / "secrets.toml.template"
    
    if not secrets_file.exists() and template_file.exists():
        # Copy template to secrets.toml
        with open(template_file, 'r') as f:
            content = f.read()
        
        with open(secrets_file, 'w') as f:
            f.write(content)
        
        print(f"✅ Created {secrets_file}")
        print(f"📝 Edit this file to add your API keys")
    else:
        print(f"ℹ️  {secrets_file} already exists")

def open_api_links():
    """Open browser tabs for API key registration"""
    apis = {
        "Hugging Face": "https://huggingface.co/settings/tokens",
        "Replicate": "https://replicate.com/account/api-tokens", 
        "Together AI": "https://api.together.xyz/settings/api-keys"
    }
    
    print("🔑 Opening API registration pages...")
    for name, url in apis.items():
        print(f"📖 {name}: {url}")
        try:
            webbrowser.open(url)
        except:
            print(f"   Please manually open: {url}")

def show_instructions():
    """Show setup instructions"""
    print("""
🎌 ANIME STORY GENERATOR - API SETUP 🎌

This app works with FREE APIs! Here's how to get started:

📋 STEP 1: Get Free API Keys
   The script will open browser tabs for you to register:
   
   🔹 Hugging Face (1000 requests/month FREE)
   🔹 Replicate ($10 credits/month FREE)  
   🔹 Together AI ($25 credits FREE)

📝 STEP 2: Add Keys to Secrets File
   After getting your keys, edit: .streamlit/secrets.toml
   
   Replace the placeholder values:
   HUGGINGFACE_TOKEN = "hf_your_actual_token_here"
   REPLICATE_TOKEN = "r8_your_actual_token_here"
   TOGETHER_TOKEN = "your_actual_token_here"

🚀 STEP 3: Run the App
   streamlit run app.py

💡 TIP: The app works even without API keys!
   It will use template-based fallback stories.

🎯 Ready to start? Press Enter to open API registration pages...
""")

def main():
    print("🎌 Anime Story Generator - API Setup Helper")
    print("=" * 50)
    
    show_instructions()
    
    input("Press Enter to continue...")
    
    # Create secrets file
    create_secrets_file()
    
    # Open API registration pages
    open_api_links()
    
    print("""
✅ Setup Complete!

Next steps:
1. Register for API accounts (browser tabs opened)
2. Copy your API keys
3. Edit .streamlit/secrets.toml with your keys
4. Run: streamlit run app.py

🎌 Happy storytelling! 🚀
""")

if __name__ == "__main__":
    main()
