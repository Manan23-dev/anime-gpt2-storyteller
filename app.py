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

# Custom CSS for anime theme
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0a0e27, #1a1f3a, #2a0845);
        color: white;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27, #1a1f3a, #2a0845);
    }
    
    .story-container {
        background: rgba(255, 107, 107, 0.1);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #ff6b6b;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: rgba(0, 0, 0, 0.3);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .genre-card {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.3), rgba(78, 205, 196, 0.3));
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .genre-card:hover {
        border-color: #ff6b6b;
        transform: scale(1.02);
    }
    
    .genre-card.selected {
        background: linear-gradient(45deg, rgba(255, 107, 107, 0.8), rgba(255, 142, 83, 0.8));
        border-color: #ff6b6b;
    }
</style>
""", unsafe_allow_html=True)

class AnimeStoryGenerator:
    def __init__(self):
        # Initialize with default tokens - will be updated when secrets are available
        self.api_configs = {
            "huggingface": {
                "url": "https://api-inference.huggingface.co/models/gpt2",
                "headers": {"Authorization": "Bearer hf_demo"},
                "free": True
            },
            "replicate": {
                "url": "https://api.replicate.com/v1/predictions",
                "headers": {"Authorization": "Token demo"},
                "free": True
            },
            "together": {
                "url": "https://api.together.xyz/inference",
                "headers": {"Authorization": "Bearer demo"},
                "free": True
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
            hf_token = st.secrets.get('HUGGINGFACE_TOKEN', 'hf_demo')
            replicate_token = st.secrets.get('REPLICATE_TOKEN', 'demo')
            together_token = st.secrets.get('TOGETHER_TOKEN', 'demo')
            
            # Only update if tokens are not default values
            if hf_token != 'hf_demo':
                self.api_configs["huggingface"]["headers"]["Authorization"] = f"Bearer {hf_token}"
            if replicate_token != 'demo':
                self.api_configs["replicate"]["headers"]["Authorization"] = f"Token {replicate_token}"
            if together_token != 'demo':
                self.api_configs["together"]["headers"]["Authorization"] = f"Bearer {together_token}"
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
                    "max_length": max_length,
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

    def generate_fallback_story(self, prompt: str, genre: str) -> str:
        """Generate a fallback story using templates when APIs fail"""
        templates = {
            "shonen": [
                "The sun rose over Tokyo as {protagonist} prepared for their greatest challenge. '{dialogue}' they shouted, gripping their weapon tightly. With unwavering determination, they faced the trials ahead, knowing that true strength comes from protecting those you care about.",
                "In the hidden village, {protagonist} trained relentlessly under the moonlight. Master {mentor} watched from the shadows, knowing that the final test approached. '{dialogue}' the master whispered. The legendary technique would soon be needed.",
                "The tournament arena erupted in cheers as {protagonist} stepped forward. Their rival stood across the battlefield, eyes blazing with competitive fire. '{dialogue}' they declared, raising their weapon high."
            ],
            "isekai": [
                "The summoning circle pulsed with otherworldly light beneath {protagonist}'s feet. When the glow faded, they stood in a vast meadow under twin moons. '{dialogue}' they whispered, realizing their ordinary life had ended.",
                "After the accident, {protagonist} expected darkness. Instead, they awakened in a fantasy world as the legendary {class}. '{dialogue}' they said, examining their new abilities.",
                "The goddess smiled as she explained the situation to {protagonist}. '{dialogue}' she said, offering them incredible cheat abilities."
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

    def generate_story(self, prompt: str, genre: str, max_length: int = 200) -> Dict:
        """Generate story with multiple API fallbacks"""
        genre_info = self.genres.get(genre, self.genres["shonen"])
        full_prompt = f"{genre_info['prompt_prefix']} {prompt}"
        
        # Try APIs in order of preference
        apis_to_try = [
            ("huggingface", self.generate_with_huggingface),
            ("replicate", self.generate_with_replicate),
        ]
        
        for api_name, api_func in apis_to_try:
            try:
                result = api_func(full_prompt, max_length)
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
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 4rem; background: linear-gradient(45deg, #ff6b6b, #ffd93d, #6bcf7f, #4ecdc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem;">🎌 ANIME STORY GENERATOR 🎌</h1>
        <p style="font-size: 1.3rem; opacity: 0.9;">Generate Epic Anime Stories with AI Power</p>
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
        max_length = st.slider("Max Length", 50, 500, 200)
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
    
    # Main content area
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
        
        # Genre selection
        st.markdown("### 🎭 Choose Your Genre")
        
        # Create genre selection
        selected_genre = st.radio(
            "Select Genre:",
            options=list(generator.genres.keys()),
            format_func=lambda x: generator.genres[x]["name"],
            horizontal=False
        )
        
        # Display genre description
        genre_info = generator.genres[selected_genre]
        st.markdown(f"**{genre_info['name']}**: {genre_info['description']}")
        
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
                        # Display story
                        st.markdown("### 📖 Generated Story")
                        st.markdown(f"""
                        <div class="story-container">
                            <p style="line-height: 1.8; font-size: 1.1rem;">{result['text']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display metrics
                        word_count = len(result['text'].split())
                        token_count = int(word_count * 1.3)
                        tokens_per_sec = int(token_count / generation_time) if generation_time > 0 else 0
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("📊 Tokens", token_count)
                        with col2:
                            st.metric("⏱️ Time", f"{generation_time:.2f}s")
                        with col3:
                            st.metric("🚀 Speed", f"{tokens_per_sec} tok/s")
                        with col4:
                            st.metric("🤖 Provider", result['provider'])
                        
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
        
        # Quick genre buttons
        st.markdown("### 🎨 Quick Genre Selection")
        for genre_key, genre_info in generator.genres.items():
            if st.button(genre_info["name"], key=f"genre_{genre_key}", use_container_width=True):
                st.session_state.selected_genre = genre_key
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; opacity: 0.7;">
        <p>🎌 Made with ❤️ for anime storytelling enthusiasts</p>
        <p>🚀 Powered by free AI APIs • 🌟 Open source on GitHub</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
