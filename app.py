import streamlit as st
import requests
import json
import time
import random
from typing import Dict, List, Optional

# Page configuration
st.set_page_config(
    page_title="🎌 Anime Story Generator AI",
    page_icon="🎌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS inspired by GitHub pages
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        font-family: 'Poppins', sans-serif;
        background: #0a0e27;
        color: white;
        overflow-x: hidden;
    }
    
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    
    /* Animated background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, #0a0e27, #1a1f3a, #2a0845);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        opacity: 0.9;
        z-index: -1;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating particles */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 20%, rgba(255, 107, 107, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(78, 205, 196, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 60%, rgba(255, 217, 61, 0.2) 0%, transparent 50%);
        animation: particleFloat 20s ease-in-out infinite;
        z-index: -1;
    }
    
    @keyframes particleFloat {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        position: relative;
        z-index: 10;
        background: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        border-radius: 0 0 30px 30px;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(45deg, #ff6b6b, #ffd93d, #6bcf7f, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        animation: glow 2s ease-in-out infinite alternate;
        text-shadow: 0 0 30px rgba(255, 107, 107, 0.5);
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 20px #ff6b6b); }
        to { filter: drop-shadow(0 0 40px #4ecdc4); }
    }
    
    .main-header p {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    
    /* Main content container */
    .main-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(15px);
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        z-index: 10;
    }
    
    /* Story form styling */
    .story-form {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid rgba(255, 107, 107, 0.3);
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }
    
    .story-form:hover {
        border-color: #ff6b6b;
        box-shadow: 0 0 30px rgba(255, 107, 107, 0.3);
    }
    
    /* Genre tablets with background images */
    .genre-tablets {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .genre-tablet {
        position: relative;
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.3), rgba(78, 205, 196, 0.3));
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        color: white;
        cursor: pointer;
        transition: all 0.4s ease;
        text-align: center;
        font-weight: 600;
        overflow: hidden;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        backdrop-filter: blur(10px);
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    
    /* Individual genre backgrounds */
    .genre-tablet[data-genre="shonen"] {
        background-image: 
            linear-gradient(rgba(255, 107, 107, 0.5), rgba(255, 107, 107, 0.7)),
            url('https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop');
    }
    
    .genre-tablet[data-genre="action"] {
        background-image: 
            linear-gradient(rgba(139, 0, 139, 0.5), rgba(75, 0, 130, 0.7)),
            url('https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop');
    }
    
    .genre-tablet[data-genre="isekai"] {
        background-image: 
            linear-gradient(rgba(0, 191, 255, 0.5), rgba(50, 205, 50, 0.7)),
            url('https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop');
    }
    
    .genre-tablet[data-genre="mecha"] {
        background-image: 
            linear-gradient(rgba(70, 130, 180, 0.5), rgba(0, 191, 255, 0.7)),
            url('https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop');
    }
    
    .genre-tablet[data-genre="romance"] {
        background-image: 
            linear-gradient(rgba(255, 182, 193, 0.5), rgba(255, 105, 180, 0.7)),
            url('https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop');
    }
    
    .genre-tablet[data-genre="slice"] {
        background-image: 
            linear-gradient(rgba(210, 180, 140, 0.5), rgba(139, 90, 43, 0.7)),
            url('https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop');
    }
    
    .genre-tablet:hover {
        border-color: #ff6b6b;
        transform: scale(1.05) translateY(-8px);
        box-shadow: 0 25px 50px rgba(255, 107, 107, 0.5);
    }
    
    .genre-tablet.selected {
        background: linear-gradient(45deg, rgba(255, 107, 107, 0.8), rgba(255, 142, 83, 0.8));
        border-color: #ff6b6b;
        box-shadow: 0 20px 60px rgba(255, 107, 107, 0.6);
        transform: scale(1.02);
    }
    
    .genre-tablet-text {
        position: relative;
        z-index: 2;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        font-size: 1.1rem;
        font-weight: 700;
    }
    
    /* Button styling for genre tablets */
    .stButton > button {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.3), rgba(78, 205, 196, 0.3));
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        color: white;
        font-weight: 700;
        font-size: 1rem;
        padding: 1.5rem;
        min-height: 120px;
        transition: all 0.4s ease;
        backdrop-filter: blur(10px);
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        border-color: #ff6b6b;
        transform: scale(1.05) translateY(-5px);
        box-shadow: 0 20px 40px rgba(255, 107, 107, 0.4);
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Specific button backgrounds */
    .stButton > button[data-testid*="genre_shonen"] {
        background-image: 
            linear-gradient(rgba(255, 107, 107, 0.6), rgba(255, 107, 107, 0.8)),
            url('https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop');
        background-size: cover;
        background-position: center;
    }
    
    .stButton > button[data-testid*="genre_action"] {
        background-image: 
            linear-gradient(rgba(139, 0, 139, 0.6), rgba(75, 0, 130, 0.8)),
            url('https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop');
        background-size: cover;
        background-position: center;
    }
    
    .stButton > button[data-testid*="genre_isekai"] {
        background-image: 
            linear-gradient(rgba(0, 191, 255, 0.6), rgba(50, 205, 50, 0.8)),
            url('https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop');
        background-size: cover;
        background-position: center;
    }
    
    .stButton > button[data-testid*="genre_mecha"] {
        background-image: 
            linear-gradient(rgba(70, 130, 180, 0.6), rgba(0, 191, 255, 0.8)),
            url('https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop');
        background-size: cover;
        background-position: center;
    }
    
    .stButton > button[data-testid*="genre_romance"] {
        background-image: 
            linear-gradient(rgba(255, 182, 193, 0.6), rgba(255, 105, 180, 0.8)),
            url('https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop');
        background-size: cover;
        background-position: center;
    }
    
    .stButton > button[data-testid*="genre_slice"] {
        background-image: 
            linear-gradient(rgba(210, 180, 140, 0.6), rgba(139, 90, 43, 0.8)),
            url('https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop');
        background-size: cover;
        background-position: center;
    }
    
    /* Generate button */
    .generate-btn {
        background: linear-gradient(45deg, #ff6b6b, #ff8e53);
        border: none;
        border-radius: 50px;
        padding: 1.5rem 3rem;
        font-size: 1.3rem;
        font-weight: 700;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 15px 35px rgba(255, 107, 107, 0.4);
        width: 100%;
        margin-top: 2rem;
    }
    
    .generate-btn:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(255, 107, 107, 0.6);
    }
    
    .generate-btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
    }
    
    /* Story output */
    .story-output {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.15), rgba(78, 205, 196, 0.15));
        padding: 2rem;
        border-radius: 20px;
        border-left: 5px solid #ff6b6b;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
        min-height: 200px;
        animation: fadeInUp 0.5s ease;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .story-text {
        line-height: 1.8;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    /* Metrics */
    .metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
    }
    
    .metric-card {
        background: rgba(0, 0, 0, 0.3);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(45deg, #ff6b6b, #ffd93d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.8;
        margin-top: 0.5rem;
    }
    
    /* Loading animation */
    .loading {
        text-align: center;
        padding: 2rem;
        font-size: 1.2rem;
    }
    
    .spinner {
        width: 50px;
        height: 50px;
        border: 5px solid rgba(255, 107, 107, 0.2);
        border-top: 5px solid #ff6b6b;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Input styling */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 107, 107, 0.3);
        border-radius: 15px;
        color: white;
        font-size: 1rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #ff6b6b;
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.3);
    }
    
    /* Slider styling */
    .stSlider .stSlider {
        background: rgba(255, 107, 107, 0.3);
    }
    
    /* Radio button styling */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 2.5rem; }
        .genre-selector { grid-template-columns: 1fr; }
        .genre-card {
            min-height: 180px;
            padding: 1.5rem 1rem;
        }
        .genre-icon { font-size: 2.5rem; }
        .genre-name { font-size: 1.1rem; }
        .genre-desc { font-size: 0.85rem; }
    }
</style>
""", unsafe_allow_html=True)

class AnimeStoryGenerator:
    def __init__(self):
        # Initialize with default tokens - will be updated when secrets are available
        self.api_configs = {
            # Free APIs
            "huggingface": {
                "url": "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
                "headers": {"Authorization": "Bearer hf_demo"},
                "free": True,
                "model": "DialoGPT"
            },
            "huggingface_llama": {
                "url": "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf",
                "headers": {"Authorization": "Bearer hf_demo"},
                "free": True,
                "model": "Llama-2"
            },
            "replicate": {
                "url": "https://api.replicate.com/v1/predictions",
                "headers": {"Authorization": "Token demo"},
                "free": True,
                "model": "GPT-2"
            },
            "together": {
                "url": "https://api.together.xyz/inference",
                "headers": {"Authorization": "Bearer demo"},
                "free": True,
                "model": "Llama-3"
            },
            # Premium APIs (better quality)
            "openai": {
                "url": "https://api.openai.com/v1/chat/completions",
                "headers": {"Authorization": "Bearer demo"},
                "free": False,
                "model": "GPT-4o-mini"
            },
            "anthropic": {
                "url": "https://api.anthropic.com/v1/messages",
                "headers": {"Authorization": "Bearer demo"},
                "free": False,
                "model": "Claude-3.5-Sonnet"
            }
        }
        
        # Try to update with real tokens if available
        self._update_api_tokens()
        
        self.genres = {
            "shonen": {
                "name": "⚔️ SHONEN HEROES",
                "description": "Epic battles and heroic adventures",
                "prompt_prefix": "[SHONEN] [SCENE]"
            },
            "isekai": {
                "name": "🌍 ISEKAI WORLDS", 
                "description": "Transported to magical realms",
                "prompt_prefix": "[ISEKAI] [SCENE]"
            },
            "mecha": {
                "name": "🤖 MECHA PILOTS",
                "description": "Giant robots defending humanity",
                "prompt_prefix": "[MECHA] [SCENE]"
            },
            "romance": {
                "name": "💕 SHOJO ROMANCE",
                "description": "Heartwarming love stories",
                "prompt_prefix": "[ROMANCE] [SCENE]"
            },
            "slice": {
                "name": "☕ SLICE OF LIFE",
                "description": "Everyday adventures and moments",
                "prompt_prefix": "[SLICE_OF_LIFE] [SCENE]"
            },
            "action": {
                "name": "🔥 DEMON SLAYERS",
                "description": "Intense supernatural combat",
                "prompt_prefix": "[ACTION] [SCENE]"
            }
        }

    def _update_api_tokens(self):
        """Update API tokens from secrets if available"""
        try:
            # Free APIs
            hf_token = st.secrets.get('HUGGINGFACE_TOKEN', 'hf_demo')
            replicate_token = st.secrets.get('REPLICATE_TOKEN', 'demo')
            together_token = st.secrets.get('TOGETHER_TOKEN', 'demo')
            
            # Premium APIs
            openai_token = st.secrets.get('OPENAI_API_KEY', 'demo')
            anthropic_token = st.secrets.get('ANTHROPIC_API_KEY', 'demo')
            
            # Update free API tokens
            if hf_token != 'hf_demo':
                self.api_configs["huggingface"]["headers"]["Authorization"] = f"Bearer {hf_token}"
                self.api_configs["huggingface_llama"]["headers"]["Authorization"] = f"Bearer {hf_token}"
            if replicate_token != 'demo':
                self.api_configs["replicate"]["headers"]["Authorization"] = f"Token {replicate_token}"
            if together_token != 'demo':
                self.api_configs["together"]["headers"]["Authorization"] = f"Bearer {together_token}"
            
            # Update premium API tokens
            if openai_token != 'demo':
                self.api_configs["openai"]["headers"]["Authorization"] = f"Bearer {openai_token}"
            if anthropic_token != 'demo':
                self.api_configs["anthropic"]["headers"]["Authorization"] = f"Bearer {anthropic_token}"
                
        except:
            # Secrets not available, use default tokens
            pass

    def generate_with_huggingface(self, prompt: str, max_length: int = 200) -> Dict:
        """Generate story using Hugging Face Inference API"""
        try:
            # Check if using demo token
            if "hf_demo" in self.api_configs["huggingface"]["headers"]["Authorization"]:
                return {"success": False, "error": "Demo token - get real token from huggingface.co/settings/tokens"}
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": max_length + 200,
                    "temperature": 0.8,
                    "top_p": 0.95,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                self.api_configs["huggingface"]["url"],
                headers=self.api_configs["huggingface"]["headers"],
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return {
                        "success": True,
                        "text": result[0].get("generated_text", ""),
                        "provider": "Hugging Face"
                    }
            
            return {"success": False, "error": f"API Error: {response.status_code}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_with_replicate(self, prompt: str) -> Dict:
        """Generate story using Replicate API"""
        try:
            # Check if using demo token
            if "demo" in self.api_configs["replicate"]["headers"]["Authorization"]:
                return {"success": False, "error": "Demo token - get real token from replicate.com/account/api-tokens"}
            
            payload = {
                "version": "replicate/gpt-2:latest",
                "input": {
                    "prompt": prompt,
                    "max_length": 200,
                    "temperature": 0.8
                }
            }
            
            response = requests.post(
                self.api_configs["replicate"]["url"],
                headers=self.api_configs["replicate"]["headers"],
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "text": result.get("output", ""),
                    "provider": "Replicate"
                }
            
            return {"success": False, "error": f"API Error: {response.status_code}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_with_openai(self, prompt: str, genre: str) -> Dict:
        """Generate story using OpenAI GPT-4o-mini"""
        try:
            if "demo" in self.api_configs["openai"]["headers"]["Authorization"]:
                return {"success": False, "error": "Demo token - get real token from platform.openai.com/api-keys"}
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system", 
                        "content": f"You are an expert anime storyteller specializing in {genre} genre. Create engaging, authentic anime stories with proper pacing, character development, and genre-appropriate elements."
                    },
                    {
                        "role": "user", 
                        "content": f"Write an anime {genre} story based on this prompt: {prompt}. Make it engaging and authentic to the genre."
                    }
                ],
                "max_tokens": 800,
                "temperature": 0.8
            }
            
            response = requests.post(
                self.api_configs["openai"]["url"],
                headers=self.api_configs["openai"]["headers"],
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "text": result["choices"][0]["message"]["content"],
                    "provider": "OpenAI GPT-4o-mini"
                }
            
            return {"success": False, "error": f"API Error: {response.status_code}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_with_claude(self, prompt: str, genre: str) -> Dict:
        """Generate story using Anthropic Claude"""
        try:
            if "demo" in self.api_configs["anthropic"]["headers"]["Authorization"]:
                return {"success": False, "error": "Demo token - get real token from console.anthropic.com"}
            
            payload = {
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 800,
                "messages": [
                    {
                        "role": "user", 
                        "content": f"Write an engaging anime {genre} story based on this prompt: {prompt}. Make it authentic to the genre with proper pacing and character development."
                    }
                ]
            }
            
            response = requests.post(
                self.api_configs["anthropic"]["url"],
                headers=self.api_configs["anthropic"]["headers"],
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "text": result["content"][0]["text"],
                    "provider": "Claude-3.5-Sonnet"
                }
            
            return {"success": False, "error": f"API Error: {response.status_code}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_with_llama(self, prompt: str, genre: str) -> Dict:
        """Generate story using Llama-2 via Hugging Face"""
        try:
            if "hf_demo" in self.api_configs["huggingface_llama"]["headers"]["Authorization"]:
                return {"success": False, "error": "Demo token - get real token from huggingface.co/settings/tokens"}
            
            payload = {
                "inputs": f"<s>[INST] Write an anime {genre} story based on: {prompt} [/INST]",
                "parameters": {
                    "max_length": 500,
                    "temperature": 0.8,
                    "top_p": 0.95,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                self.api_configs["huggingface_llama"]["url"],
                headers=self.api_configs["huggingface_llama"]["headers"],
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return {
                        "success": True,
                        "text": result[0].get("generated_text", ""),
                        "provider": "Llama-2"
                    }
            
            return {"success": False, "error": f"API Error: {response.status_code}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_fallback_story(self, prompt: str, genre: str) -> str:
        """Generate a fallback story using templates when APIs fail"""
        templates = {
            "shonen": [
                "The sun rose over Tokyo as {protagonist} prepared for their greatest challenge. The city stretched endlessly before them, filled with both danger and opportunity. '{dialogue}' they shouted, gripping their weapon tightly. With unwavering determination, they faced the trials ahead, knowing that true strength comes from protecting those you care about. The journey would test not just their physical abilities, but their resolve and the bonds they had forged with their friends. Every step forward was a step toward becoming the hero they were destined to be. The wind carried whispers of ancient legends, stories of warriors who had walked this same path centuries ago, each one leaving behind a legacy of courage and sacrifice.",
                "In the hidden village, {protagonist} trained relentlessly under the moonlight. Master {mentor} watched from the shadows, knowing that the final test approached. '{dialogue}' the master whispered. The legendary technique would soon be needed. Years of preparation had led to this moment, where ancient wisdom would be passed down to the next generation. The technique wasn't just about power—it was about understanding the responsibility that came with great strength and using it to protect the innocent. The training had been grueling, pushing {protagonist} beyond their limits, but each drop of sweat and every moment of pain had been worth it for this chance to carry on the village's sacred tradition.",
                "The tournament arena erupted in cheers as {protagonist} stepped forward. Their rival stood across the battlefield, eyes blazing with competitive fire. '{dialogue}' they declared, raising their weapon high. This wasn't just about winning—it was about proving that dreams and friendship could overcome any obstacle. The crowd held their breath as the two warriors prepared for the ultimate showdown, each carrying the hopes and dreams of everyone who believed in them. The arena had witnessed countless battles, but this one felt different. It was more than a competition; it was a testament to the power of determination and the unbreakable bonds of friendship that had brought them this far."
            ],
            "isekai": [
                "The summoning circle pulsed with otherworldly light beneath {protagonist}'s feet. When the glow faded, they stood in a vast meadow under twin moons. '{dialogue}' they whispered, realizing their ordinary life had ended. The air itself felt different here, charged with magical energy that made their skin tingle. Strange creatures roamed the landscape, and in the distance, they could see towering castles and floating islands that defied the laws of physics. This was no ordinary fantasy world—it was a realm where magic was as common as breathing, and where their modern knowledge would be both a blessing and a curse. The goddess had chosen them for a reason, and now they would discover what destiny had in store.",
                "After the accident, {protagonist} expected darkness. Instead, they awakened in a fantasy world as the legendary {class}. '{dialogue}' they said, examining their new abilities. The transformation had been complete—their body felt stronger, more agile, and their mind buzzed with knowledge of spells and combat techniques that had never existed in their previous life. The world around them was breathtaking, filled with magical creatures, ancient ruins, and mysteries waiting to be solved. But with great power came great responsibility, and they would soon learn that being the chosen one meant facing challenges that would test not just their new abilities, but their very soul.",
                "The goddess smiled as she explained the situation to {protagonist}. '{dialogue}' she said, offering them incredible cheat abilities. The divine power coursed through their veins, granting them abilities that would make them nearly invincible in this world. But power alone wasn't enough—they would need wisdom, courage, and the strength to make difficult choices. The goddess had seen something special in them, something that made them worthy of this second chance at life. Now it was up to them to prove that her faith had been well-placed, and to use their incredible gifts to make this world a better place for everyone."
            ],
            "mecha": [
                "The massive hangar doors opened, revealing {protagonist}'s giant robot against the starlit sky. '{dialogue}' they declared through the communication system. Earth's last line of defense stood ready.",
                "Neural synchronization at 95% and climbing. {protagonist} felt their consciousness merge with their mecha's AI. '{dialogue}' they said, as enemy signatures appeared on radar.",
                "In the cockpit of their inherited mecha, {protagonist} discovered their mysterious past. '{dialogue}' the AI companion explained."
            ],
            "romance": [
                "Cherry blossoms danced in the spring breeze as {protagonist} nervously approached their crush. '{dialogue}' they stammered, their heart pounding.",
                "The rain started falling as {protagonist} waited under the school gate. When {love_interest} appeared with an umbrella, they shared a moment of perfect silence.",
                "The rivalry between {protagonist} and {love_interest} had defined their entire school career. But during the cultural festival, something shifted."
            ],
            "slice": [
                "The morning sun filtered through the classroom windows as {protagonist} settled into their routine. '{dialogue}' their friend said, offering to share lunch.",
                "After school, the literature club gathered in their usual spot. {protagonist} watched their friends discuss the latest novel, feeling grateful.",
                "The small town had its own gentle rhythm, and {protagonist} was finally learning to appreciate it. '{dialogue}' the elderly shopkeeper said with a knowing smile."
            ],
            "action": [
                "Under the blood-red moon, {protagonist} gripped their cursed blade tighter. The demon's eyes glowed crimson in the darkness ahead. '{dialogue}' they breathed.",
                "The ancient curse mark pulsed on {protagonist}'s arm as supernatural power coursed through their veins. '{dialogue}' they growled, facing the horde of cursed spirits.",
                "The school bell chimed midnight as {protagonist} leaped across rooftops, pursuing their target. '{dialogue}' they muttered, preparing their special attack."
            ]
        }
        
        protagonist_names = ["Kenji", "Akira", "Yuki", "Hana", "Takeshi", "Misaki", "Ryu", "Sakura"]
        dialogue_options = [
            "I won't give up, no matter what!",
            "This is just the beginning of our story!",
            "I'll protect everyone I care about!",
            "My dreams are worth fighting for!",
            "Today, everything changes!",
            "I believe in the power of friendship!"
        ]
        
        template = random.choice(templates.get(genre, templates["shonen"]))
        protagonist = random.choice(protagonist_names)
        dialogue = random.choice(dialogue_options)
        
        story = template.replace("{protagonist}", protagonist)
        story = story.replace("{dialogue}", dialogue)
        story = story.replace("{mentor}", random.choice(protagonist_names))
        story = story.replace("{love_interest}", random.choice(protagonist_names))
        story = story.replace("{class}", random.choice(["Sword Master", "Mage", "Paladin", "Assassin"]))
        
        return f"Based on your idea: \"{prompt}\"\n\n{story}"

    def generate_story(self, prompt: str, genre: str, max_length: int = 500) -> Dict:
        """Generate story with multiple API fallbacks - upgraded models"""
        genre_info = self.genres.get(genre, self.genres["shonen"])
        
        # Try APIs in order of quality (best first)
        apis_to_try = [
            ("openai", lambda p, g: self.generate_with_openai(prompt, genre)),
            ("claude", lambda p, g: self.generate_with_claude(prompt, genre)),
            ("llama", lambda p, g: self.generate_with_llama(prompt, genre)),
            ("huggingface", lambda p, g: self.generate_with_huggingface(f"{genre_info['prompt_prefix']} {prompt}", max_length)),
            ("replicate", lambda p, g: self.generate_with_replicate(f"{genre_info['prompt_prefix']} {prompt}")),
        ]
        
        for api_name, api_func in apis_to_try:
            try:
                result = api_func(prompt, genre)
                if result["success"]:
                    return result
            except Exception as e:
                st.warning(f"API {api_name} failed: {str(e)}")
                continue
        
        # Fallback to template-based generation
        fallback_story = self.generate_fallback_story(prompt, genre)
        return {
            "success": True,
            "text": fallback_story,
            "provider": "Template Fallback"
        }

def main():
    # Initialize generator
    generator = AnimeStoryGenerator()
    
    # Beautiful Header
    st.markdown("""
    <div class="main-header">
        <h1>🎌 ANIME STORY GENERATOR 🎌</h1>
        <p>Generate Epic Anime Stories with AI Power</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # API Status
        st.markdown("#### 🔌 API Status")
        st.info("Using free APIs: Hugging Face, Replicate")
        
        # Generation Settings
        st.markdown("#### 🎛️ Generation Settings")
        max_length = st.slider("Max Length", 100, 1000, 500)
        temperature = st.slider("Creativity", 0.1, 1.0, 0.8)
        
        # About section
        st.markdown("#### 📖 About")
        st.markdown("""
        This app uses multiple free AI APIs to generate anime stories:
        
        - **Hugging Face**: GPT-2 and other models
        - **Replicate**: Open-source model hosting
        - **Template Fallback**: When APIs are unavailable
        
        All APIs are free to use!
        """)
    
    # Main content area with beautiful layout
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Story form section
    st.markdown('<div class="story-form">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Story prompt input
        st.markdown("### 📝 Your Story Idea")
        prompt = st.text_area(
            "Enter your anime story prompt:",
            value="A young warrior discovers a legendary sword hidden in an ancient temple",
            height=100,
            help="Describe the beginning of your anime story"
        )
        
        # Genre selection with beautiful tablets
        st.markdown("### 🎭 Choose Your Genre")
        
        # Create genre tablets with background images
        genre_tablets = st.columns(3)
        
        genre_options = list(generator.genres.keys())
        
        # First row of tablets
        with genre_tablets[0]:
            if st.button("⚔️ SHONEN HEROES", key="genre_shonen", use_container_width=True):
                st.session_state.selected_genre = "shonen"
                st.rerun()
        
        with genre_tablets[1]:
            if st.button("🔥 DEMON SLAYERS", key="genre_action", use_container_width=True):
                st.session_state.selected_genre = "action"
                st.rerun()
        
        with genre_tablets[2]:
            if st.button("🌍 ISEKAI WORLDS", key="genre_isekai", use_container_width=True):
                st.session_state.selected_genre = "isekai"
                st.rerun()
        
        # Second row of tablets
        genre_tablets2 = st.columns(3)
        
        with genre_tablets2[0]:
            if st.button("🤖 MECHA PILOTS", key="genre_mecha", use_container_width=True):
                st.session_state.selected_genre = "mecha"
                st.rerun()
        
        with genre_tablets2[1]:
            if st.button("💕 SHOJO ROMANCE", key="genre_romance", use_container_width=True):
                st.session_state.selected_genre = "romance"
                st.rerun()
        
        with genre_tablets2[2]:
            if st.button("☕ SLICE OF LIFE", key="genre_slice", use_container_width=True):
                st.session_state.selected_genre = "slice"
                st.rerun()
        
        # Get selected genre
        selected_genre = st.session_state.get('selected_genre', 'shonen')
        
        # Display selected genre with visual indicator
        genre_info = generator.genres[selected_genre]
        
        # Show selected genre with beautiful styling
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(255, 107, 107, 0.2), rgba(78, 205, 196, 0.2)); 
                    padding: 1rem; border-radius: 15px; border-left: 5px solid #ff6b6b; 
                    margin: 1rem 0; backdrop-filter: blur(10px);">
            <h4 style="color: #ffd93d; margin: 0; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);">
                {genre_info['name']}
            </h4>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);">
                {genre_info['description']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate button
        if st.button("🚀 GENERATE EPIC STORY", type="primary", use_container_width=True):
            if prompt.strip():
                with st.spinner("✨ AI is crafting your anime masterpiece..."):
                    start_time = time.time()
                    
                    # Generate story
                    result = generator.generate_story(prompt, selected_genre, max_length)
                    
                    end_time = time.time()
                    generation_time = end_time - start_time
                    
                    if result["success"]:
                        # Display story with beautiful styling
                        st.markdown("### 📖 Generated Story")
                        st.markdown(f"""
                        <div class="story-output">
                            <div class="story-text">{result['text']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display metrics with beautiful styling
                        word_count = len(result['text'].split())
                        token_count = int(word_count * 1.3)
                        tokens_per_sec = int(token_count / generation_time) if generation_time > 0 else 0
                        
                        st.markdown(f"""
                        <div class="metrics">
                            <div class="metric-card">
                                <div class="metric-value">{token_count}</div>
                                <div class="metric-label">📊 Tokens</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">{generation_time:.2f}s</div>
                                <div class="metric-label">⏱️ Time</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">{tokens_per_sec}</div>
                                <div class="metric-label">🚀 Tokens/sec</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">{result['provider'][:10]}...</div>
                                <div class="metric-label">🤖 Provider</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Success message
                        st.success(f"✅ Story generated successfully using {result['provider']}!")
                        
                    else:
                        st.error(f"❌ Generation failed: {result['error']}")
            else:
                st.warning("⚠️ Please enter a story prompt!")
    
    with col2:
        # Example prompts
        st.markdown("### 💡 Example Prompts")
        
        example_prompts = [
            "A young pirate sets sail to find the legendary One Piece",
            "A demon slayer faces their greatest challenge under the full moon",
            "After dying in an accident, a programmer awakens in a fantasy RPG world",
            "Teenage pilots must defend Earth from alien invasion",
            "Two rivals realize their feelings during the school festival",
            "Three friends start a band in their final year of high school"
        ]
        
        for i, example in enumerate(example_prompts):
            if st.button(f"📝 {example}", key=f"example_{i}", use_container_width=True):
                st.session_state.example_prompt = example
                st.rerun()
        
        # Quick genre selection info
        st.markdown("### 🎨 Genre Selection")
        st.info("Use the beautiful genre tablets in the main area to select your preferred anime genre!")
    
    # Close HTML containers
    st.markdown('</div>', unsafe_allow_html=True)  # Close story-form
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-content
    
    # Beautiful Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; opacity: 0.7;">
        <p style="font-size: 1.1rem; margin-bottom: 1rem;">🎌 Made with ❤️ for anime storytelling enthusiasts</p>
        <p style="font-size: 0.9rem;">🚀 Powered by free AI APIs • 🌟 Open source on GitHub</p>
        <p style="font-size: 0.8rem; margin-top: 1rem;">✨ Generate epic stories with GPT-4, Claude, Llama, and more!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
