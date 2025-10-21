# 🚀 Anime GPT-2 Storyteller - Deployment Guide

## 📋 Overview

This guide will help you deploy your anime story generator with **real AI models** using **free APIs**. The app includes multiple fallback options to ensure it always works, even without API keys.

## 🎯 Deployment Options

### Option 1: Streamlit Cloud (Recommended - FREE)

**Pros:**
- ✅ Completely free hosting
- ✅ Automatic deployments from GitHub
- ✅ Built-in secrets management
- ✅ Global CDN
- ✅ No server maintenance

**Steps:**

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Streamlit app with free AI APIs"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `anime-gpt2-storyteller-1`
   - Main file path: `app.py`
   - Click "Deploy!"

3. **Add API Keys (Optional)**
   - In Streamlit Cloud dashboard, go to "Settings" → "Secrets"
   - Add your API keys:
   ```toml
   HUGGINGFACE_TOKEN = "hf_your_token_here"
   REPLICATE_TOKEN = "r8_your_token_here"
   TOGETHER_TOKEN = "your_together_token_here"
   ```

### Option 2: Hugging Face Spaces (FREE)

**Pros:**
- ✅ Free hosting with GPU
- ✅ Built-in model integration
- ✅ Easy sharing

**Steps:**

1. **Create Hugging Face Space**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose "Streamlit" SDK
   - Name: `anime-story-generator`

2. **Upload Files**
   - Upload `app.py`, `requirements.txt`, and `.streamlit/config.toml`
   - Add your API keys in Space settings

3. **Deploy**
   - Hugging Face will automatically build and deploy your app

### Option 3: Railway (FREE Tier)

**Pros:**
- ✅ Free tier available
- ✅ Easy GitHub integration
- ✅ Automatic deployments

**Steps:**

1. **Connect GitHub**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"

2. **Configure**
   - Select your repository
   - Railway will auto-detect it's a Streamlit app
   - Add environment variables for API keys

## 🔑 Free API Setup

### 1. Hugging Face Inference API (FREE)

**Get Started:**
1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Create a new token
3. Copy the token

**Free Tier:**
- ✅ 1000 requests/month
- ✅ Access to GPT-2, GPT-Neo, and other models
- ✅ No credit card required

**Usage in App:**
```python
# Already integrated in app.py
result = generator.generate_with_huggingface(prompt, max_length)
```

### 2. Replicate API (FREE)

**Get Started:**
1. Go to [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens)
2. Create a new token
3. Copy the token

**Free Tier:**
- ✅ $10 free credits monthly
- ✅ Access to open-source models
- ✅ Fast inference

### 3. Together AI (FREE)

**Get Started:**
1. Go to [api.together.xyz/settings/api-keys](https://api.together.xyz/settings/api-keys)
2. Create a new API key
3. Copy the key

**Free Tier:**
- ✅ $25 free credits
- ✅ Access to Llama, Mistral, and other models
- ✅ High-quality generation

## 🛠️ Local Development

### Prerequisites
- Python 3.8+
- Git

### Setup
```bash
# Clone repository
git clone https://github.com/yourusername/anime-gpt2-storyteller-1.git
cd anime-gpt2-storyteller-1

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up secrets (optional)
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your API keys

# Run locally
streamlit run app.py
```

## 🎨 Customization

### Adding New Genres
Edit `app.py` and add to the `genres` dictionary:

```python
self.genres = {
    # ... existing genres ...
    "new_genre": {
        "name": "🌟 NEW GENRE",
        "description": "Description of your genre",
        "prompt_prefix": "[NEW_GENRE] [SCENE]"
    }
}
```

### Adding New APIs
Add a new method to the `AnimeStoryGenerator` class:

```python
def generate_with_new_api(self, prompt: str) -> Dict:
    """Generate story using your new API"""
    try:
        # Your API integration code here
        return {"success": True, "text": generated_text, "provider": "New API"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### Styling
The app uses custom CSS in the Streamlit app. Modify the `st.markdown()` section with custom styles.

## 🚀 Advanced Features

### 1. Model Fine-tuning
Use your existing `train.py` to fine-tune models and upload them to Hugging Face:

```bash
# Train your model
python train.py

# Upload to Hugging Face Hub
huggingface-cli login
python -c "
from transformers import GPT2LMHeadModel, GPT2Tokenizer
model = GPT2LMHeadModel.from_pretrained('./models')
tokenizer = GPT2Tokenizer.from_pretrained('./models')
model.push_to_hub('yourusername/anime-gpt2-storyteller')
tokenizer.push_to_hub('yourusername/anime-gpt2-storyteller')
"
```

### 2. Database Integration
Add story saving functionality:

```python
import sqlite3

def save_story(story, genre, prompt):
    conn = sqlite3.connect('stories.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY,
            prompt TEXT,
            genre TEXT,
            story TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('INSERT INTO stories (prompt, genre, story) VALUES (?, ?, ?)', 
                   (prompt, genre, story))
    conn.commit()
    conn.close()
```

### 3. User Authentication
Add user accounts with Streamlit-Authenticator:

```bash
pip install streamlit-authenticator
```

## 📊 Monitoring & Analytics

### 1. Usage Tracking
Add analytics to track usage:

```python
import streamlit as st

def track_usage(action, genre=None):
    # Log usage to file or database
    with open('usage.log', 'a') as f:
        f.write(f"{time.time()},{action},{genre}\n")

# Use in your app
track_usage('story_generated', selected_genre)
```

### 2. Performance Monitoring
Monitor API response times and success rates:

```python
def log_performance(provider, success, response_time):
    # Log performance metrics
    pass
```

## 🔧 Troubleshooting

### Common Issues

1. **API Rate Limits**
   - Solution: The app has multiple fallbacks
   - Add more API providers in the `generate_story` method

2. **Streamlit Deployment Issues**
   - Check `requirements.txt` has all dependencies
   - Ensure `app.py` is in the root directory
   - Verify secrets are properly configured

3. **Model Loading Errors**
   - The app uses APIs instead of local models
   - If APIs fail, template fallback is used

### Debug Mode
Run with debug information:

```bash
streamlit run app.py --logger.level debug
```

## 🎯 Next Steps

1. **Deploy your app** using one of the options above
2. **Get API keys** for better performance
3. **Customize** the genres and templates
4. **Share** your deployed app with others
5. **Monitor** usage and performance

## 📞 Support

- **GitHub Issues**: [Create an issue](https://github.com/yourusername/anime-gpt2-storyteller-1/issues)
- **Streamlit Community**: [Discord](https://discord.gg/streamlit)
- **Documentation**: [Streamlit Docs](https://docs.streamlit.io)

---

**🎌 Happy storytelling! Your anime story generator is ready to deploy! 🚀**
