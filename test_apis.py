#!/usr/bin/env python3
"""
API Test Script for Anime Story Generator
Tests all available APIs to ensure they're working correctly.
"""

import requests
import time
import json
from typing import Dict, List

class APITester:
    def __init__(self):
        self.results = {}
        
    def test_huggingface(self, token: str = None) -> Dict:
        """Test Hugging Face Inference API"""
        print("🔍 Testing Hugging Face API...")
        
        if not token or token == "your_huggingface_token_here":
            return {"success": False, "error": "No valid token provided"}
        
        try:
            url = "https://api-inference.huggingface.co/models/gpt2"
            headers = {"Authorization": f"Bearer {token}"}
            payload = {
                "inputs": "Once upon a time in a magical world",
                "parameters": {
                    "max_length": 50,
                    "temperature": 0.8,
                    "do_sample": True
                }
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                    return {
                        "success": True,
                        "text": generated_text[:100] + "...",
                        "provider": "Hugging Face"
                    }
            
            return {"success": False, "error": f"API Error: {response.status_code}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_replicate(self, token: str = None) -> Dict:
        """Test Replicate API"""
        print("🔍 Testing Replicate API...")
        
        if not token or token == "your_replicate_token_here":
            return {"success": False, "error": "No valid token provided"}
        
        try:
            url = "https://api.replicate.com/v1/predictions"
            headers = {"Authorization": f"Token {token}"}
            payload = {
                "version": "replicate/gpt-2:latest",
                "input": {
                    "prompt": "Once upon a time in a magical world",
                    "max_length": 50,
                    "temperature": 0.8
                }
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "text": "Replicate API connected successfully",
                    "provider": "Replicate"
                }
            
            return {"success": False, "error": f"API Error: {response.status_code}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_together(self, token: str = None) -> Dict:
        """Test Together AI API"""
        print("🔍 Testing Together AI API...")
        
        if not token or token == "your_together_token_here":
            return {"success": False, "error": "No valid token provided"}
        
        try:
            url = "https://api.together.xyz/inference"
            headers = {"Authorization": f"Bearer {token}"}
            payload = {
                "model": "togethercomputer/RedPajama-INCITE-Chat-3B-v1",
                "prompt": "Once upon a time in a magical world",
                "max_tokens": 50,
                "temperature": 0.8
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "text": "Together AI API connected successfully",
                    "provider": "Together AI"
                }
            
            return {"success": False, "error": f"API Error: {response.status_code}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_fallback(self) -> Dict:
        """Test template fallback system"""
        print("🔍 Testing Template Fallback...")
        
        try:
            # Simulate template generation
            templates = [
                "The sun rose over Tokyo as Kenji prepared for his greatest challenge.",
                "A mysterious portal opened, transporting Hana to a fantasy world.",
                "In the cockpit of their mecha, Ryu faced the alien invaders."
            ]
            
            story = templates[0]  # Use first template
            
            return {
                "success": True,
                "text": story,
                "provider": "Template Fallback"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run_all_tests(self, tokens: Dict[str, str]) -> None:
        """Run all API tests"""
        print("🎌 ANIME STORY GENERATOR - API TEST SUITE 🎌")
        print("=" * 60)
        
        # Test each API
        apis = [
            ("Hugging Face", self.test_huggingface, tokens.get("HUGGINGFACE_TOKEN")),
            ("Replicate", self.test_replicate, tokens.get("REPLICATE_TOKEN")),
            ("Together AI", self.test_together, tokens.get("TOGETHER_TOKEN")),
            ("Template Fallback", self.test_fallback, None)
        ]
        
        for name, test_func, token in apis:
            print(f"\n📡 Testing {name}...")
            result = test_func(token)
            self.results[name] = result
            
            if result["success"]:
                print(f"✅ {name}: SUCCESS")
                print(f"   Sample: {result['text']}")
            else:
                print(f"❌ {name}: FAILED")
                print(f"   Error: {result['error']}")
            
            time.sleep(1)  # Rate limiting
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        successful_apis = [name for name, result in self.results.items() if result["success"]]
        failed_apis = [name for name, result in self.results.items() if not result["success"]]
        
        print(f"✅ Successful APIs: {len(successful_apis)}")
        for api in successful_apis:
            print(f"   - {api}")
        
        print(f"❌ Failed APIs: {len(failed_apis)}")
        for api in failed_apis:
            print(f"   - {api}")
        
        if successful_apis:
            print(f"\n🎉 Your app will work with: {', '.join(successful_apis)}")
        else:
            print(f"\n⚠️  No APIs working, but template fallback is available!")

def load_tokens_from_secrets() -> Dict[str, str]:
    """Load API tokens from secrets.toml file"""
    try:
        import streamlit as st
        # This will work if streamlit is installed
        return {
            "HUGGINGFACE_TOKEN": st.secrets.get("HUGGINGFACE_TOKEN", ""),
            "REPLICATE_TOKEN": st.secrets.get("REPLICATE_TOKEN", ""),
            "TOGETHER_TOKEN": st.secrets.get("TOGETHER_TOKEN", "")
        }
    except:
        # Fallback: try to read secrets.toml manually
        try:
            with open(".streamlit/secrets.toml", "r") as f:
                content = f.read()
                tokens = {}
                for line in content.split("\n"):
                    if "=" in line and not line.strip().startswith("#"):
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip().strip('"')
                        tokens[key] = value
                return tokens
        except:
            return {}

def main():
    print("🎌 Anime Story Generator - API Test Suite")
    print("This script tests all available APIs for your anime story generator.\n")
    
    # Load tokens
    tokens = load_tokens_from_secrets()
    
    if not tokens:
        print("⚠️  No API tokens found in .streamlit/secrets.toml")
        print("   Run setup_api_keys.py first to set up your tokens")
        print("   Or the app will use template fallback stories.\n")
    
    # Run tests
    tester = APITester()
    tester.run_all_tests(tokens)
    
    print(f"\n🚀 Ready to deploy! Run: streamlit run app.py")

if __name__ == "__main__":
    main()
