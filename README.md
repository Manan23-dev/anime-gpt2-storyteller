# 🎌 Anime Storytelling with GPT-2

[![Live Demo](https://img.shields.io/badge/🚀_Try_Demo-Live_Now-ff6b6b?style=for-the-badge)](https://manan23-dev.github.io/anime-gpt2-storyteller/)
[![GitHub](https://img.shields.io/badge/📂_Source-GitHub-4ecdc4?style=for-the-badge)](https://github.com/Manan23-dev/anime-gpt2-storyteller)

A PyTorch-based GPT-2 model with 200M parameters fine-tuned for generating anime narratives. **[Try the live demo!]([https://manan23-dev.github.io/anime-gpt2-storyteller/](https://manan23-dev-4a2r3ablbpih72jjz46tkb.streamlit.app/)**

## 🚀 Features

- **Custom embeddings** for anime genres (Shonen, Isekai, Slice of Life, Mecha, Shojo)
- **150+ tokens/sec** inference speed on Apple Silicon
- **Perplexity score of ~15** for coherent storytelling
- **Interactive web demo** with anime character backgrounds
- **Dynamic plot progression** and character development

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Manan23-dev/anime-gpt2-storyteller.git
cd anime-gpt2-storyteller

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🎯 Quick Start

### 🚀 Deploy with Real AI (Recommended)

```bash
# 1. Set up API keys (optional - app works without them!)
python setup_api_keys.py

# 2. Test your APIs
python test_apis.py

# 3. Run the web app locally
streamlit run app.py

# 4. Deploy to Streamlit Cloud (FREE!)
# - Push to GitHub
# - Go to share.streamlit.io
# - Deploy your app!
```

### 🎓 Train Your Own Model

```bash
# Train your model
python train.py

# Generate stories locally
python generate.py
```

## 🤖 Want Better Models? Here's What You Can Use

**GPT-2 is from 2019 - here are modern alternatives:**

### **🔥 Upgrade Options**

| Model | Quality | Speed | Cost | Setup Difficulty |
|-------|---------|-------|------|------------------|
| **GPT-4o Mini** | ⭐⭐⭐⭐⭐ | Fast | $0.001/story | Easy |
| **Claude 3.5 Sonnet** | ⭐⭐⭐⭐⭐ | Fast | $0.003/story | Easy |
| **Llama 3.1 8B** | ⭐⭐⭐⭐ | Fast | **FREE** | Medium |
| **Mistral 7B** | ⭐⭐⭐⭐ | Fast | **FREE** | Medium |

### **🆓 Free Options (Recommended)**

**Llama 3.1 via Hugging Face:**
```python
from transformers import pipeline

# Free, no API key needed
generator = pipeline('text-generation', 
                    model='meta-llama/Meta-Llama-3.1-8B-Instruct')

story = generator(f"Write an anime story: {prompt}", 
                 max_length=200, temperature=0.8)
```

**Local Llama with Ollama:**
```bash
# Install Ollama (runs models locally)
curl -fsSL https://ollama.ai/install.sh | sh

# Download Llama 3.1
ollama pull llama3.1

# Generate stories locally (completely free!)
ollama run llama3.1 "Write a shonen anime story about..."
```

### **💎 Premium Options (Best Quality)**

**OpenAI GPT-4o Mini:**
```javascript
// Best quality for $5 = 5000+ stories
const response = await fetch('https://api.openai.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: "gpt-4o-mini",
    messages: [{"role": "user", "content": `Generate anime ${genre} story: ${prompt}`}]
  })
});
```

## 🚀 Deployment Options

### **⚡ Streamlit Cloud (FREE - Recommended)**

**Perfect for:**
- ✅ Real AI story generation
- ✅ Free hosting forever
- ✅ Automatic deployments
- ✅ Global CDN
- ✅ No server maintenance

**Deploy in 3 steps:**
```bash
# 1. Push to GitHub
git add .
git commit -m "Add Streamlit app"
git push origin main

# 2. Go to share.streamlit.io
# 3. Connect GitHub repo and deploy!
```

**Add API keys for better performance:**
- Hugging Face: 1000 requests/month FREE
- Replicate: $10 credits/month FREE
- Together AI: $25 credits FREE

### **🌐 Hugging Face Spaces (FREE)**

**Perfect for:**
- ✅ GPU acceleration
- ✅ Built-in model integration
- ✅ Easy sharing

**Deploy:**
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Create new Space with Streamlit SDK
3. Upload your files
4. Auto-deploy!

### **☁️ Railway (FREE Tier)**

**Perfect for:**
- ✅ GitHub integration
- ✅ Automatic deployments
- ✅ Custom domains

**Deploy:**
1. Go to [railway.app](https://railway.app)
2. Connect GitHub repo
3. Auto-deploy!

### **📱 Local Development**

```bash
# Run locally with real AI
streamlit run app.py

# Test APIs
python test_apis.py

# Set up API keys
python setup_api_keys.py
```

## 💡 Cool Use Cases & Applications

### **🎓 Educational**
- **Creative Writing Aid**: Help students learn storytelling
- **Language Learning**: Generate stories in different languages
- **Literature Analysis**: Study anime narrative structures

### **🎮 Entertainment**
- **Interactive Fiction**: User-driven story branches  
- **RPG Game Content**: Generate NPC backstories & quests
- **Social Media**: Viral anime story generator bot

### **💼 Commercial**
- **Content Creation**: Anime YouTube channel scripts
- **Marketing**: Anime-themed product descriptions
- **App Integration**: Add storytelling to anime apps

### **🛠️ Technical**
- **AI Research**: Study creative text generation
- **Fine-tuning Practice**: Learn model customization
- **Portfolio Project**: Showcase ML skills to employers

## 🎨 Demo Features

The live demo includes:
- **6 anime genres** with custom backgrounds
- **Luffy** background for Shonen stories
- **Jujutsu Kaisen** theme for action stories
- **Interactive UI** with animations
- **Mobile responsive** design

## 📊 Performance

- **Model Size**: 200M parameters (optimized from GPT-2 Medium)
- **Speed**: 150+ tokens/sec on M1 Mac
- **Quality**: ~15 perplexity score
- **Genres**: 6 specialized categories
- **Device Support**: CPU, CUDA, Apple Silicon (MPS)

## 🤝 Contributing

Found a bug? Want to add a feature? PRs welcome!

1. Fork it
2. Create your feature branch
3. Commit your changes  
4. Push to the branch
5. Open a Pull Request

## 📝 License

MIT License - feel free to use this in your own projects!

---

<div align="center">

**⭐ If this helped you, please star the repo! ⭐**

[**🚀 Try Live Demo**](https://manan23-dev.github.io/anime-gpt2-storyteller/) • [**📚 Documentation**](https://github.com/Manan23-dev/anime-gpt2-storyteller) • [**🐛 Report Issues**](https://github.com/Manan23-dev/anime-gpt2-storyteller/issues)

*Made with ❤️ by [Manan Patel](https://github.com/Manan23-dev)*

</div>
