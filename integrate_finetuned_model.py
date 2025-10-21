#!/usr/bin/env python3
"""
Fine-tuned Model Integration
Add your custom fine-tuned anime model to the Streamlit app.
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import streamlit as st
from typing import Dict

class FineTunedAnimeGenerator:
    def __init__(self, model_path: str = "./anime_model"):
        """
        Initialize fine-tuned model generator
        
        Args:
            model_path: Path to your fine-tuned model
        """
        self.model_path = model_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load model and tokenizer
        try:
            print(f"Loading fine-tuned model from {model_path}...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForCausalLM.from_pretrained(model_path)
            self.model.to(self.device)
            self.model.eval()
            
            print(f"Fine-tuned model loaded successfully!")
            print(f"Device: {self.device}")
            print(f"Model parameters: {self.model.num_parameters():,}")
            
            self.is_loaded = True
            
        except Exception as e:
            print(f"Failed to load fine-tuned model: {e}")
            print("Falling back to template generation...")
            self.is_loaded = False

    def generate_story(self, prompt: str, genre: str, max_length: int = 200) -> Dict:
        """Generate story using fine-tuned model"""
        
        if not self.is_loaded:
            return {
                "success": False,
                "error": "Fine-tuned model not loaded",
                "provider": "Fine-tuned Model"
            }
        
        try:
            # Prepare prompt with genre
            genre_prefix = {
                "shonen": "[SHONEN]",
                "isekai": "[ISEKAI]", 
                "mecha": "[MECHA]",
                "romance": "[ROMANCE]",
                "slice": "[SLICE_OF_LIFE]",
                "action": "[ACTION]"
            }.get(genre, "[SHONEN]")
            
            full_prompt = f"{genre_prefix} [SCENE] {prompt}"
            
            # Tokenize
            input_ids = self.tokenizer.encode(full_prompt, return_tensors='pt').to(self.device)
            
            # Generate
            with torch.no_grad():
                output = self.model.generate(
                    input_ids,
                    max_length=input_ids.shape[1] + max_length,
                    temperature=0.8,
                    top_p=0.95,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=3,
                    num_return_sequences=1
                )
            
            # Decode
            generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
            
            # Extract only the generated part (remove input prompt)
            if full_prompt in generated_text:
                generated_text = generated_text.split(full_prompt, 1)[1].strip()
            
            return {
                "success": True,
                "text": generated_text,
                "provider": "Fine-tuned Anime Model"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": "Fine-tuned Model"
            }

def add_finetuned_to_app():
    """Add fine-tuned model option to the main app"""
    
    # This function shows how to integrate the fine-tuned model
    # into your existing app.py
    
    integration_code = '''
# Add this to your AnimeStoryGenerator class in app.py:

def __init__(self):
    # ... existing code ...
    
    # Add fine-tuned model
    self.finetuned_generator = None
    try:
        self.finetuned_generator = FineTunedAnimeGenerator("./anime_model")
    except:
        print("Fine-tuned model not available")

def generate_story(self, prompt: str, genre: str, max_length: int = 200) -> Dict:
    """Generate story with fine-tuned model as first priority"""
    
    # Try fine-tuned model first
    if self.finetuned_generator and self.finetuned_generator.is_loaded:
        result = self.finetuned_generator.generate_story(prompt, genre, max_length)
        if result["success"]:
            return result
    
    # Fall back to other APIs
    # ... existing API fallback code ...
'''
    
    print("Integration code for app.py:")
    print(integration_code)

def main():
    print("🎌 Fine-tuned Anime Model Integration 🎌")
    print("=" * 50)
    
    # Test if fine-tuned model exists
    import os
    model_path = "./anime_model"
    
    if os.path.exists(model_path):
        print(f"✅ Fine-tuned model found at {model_path}")
        
        # Test the model
        generator = FineTunedAnimeGenerator(model_path)
        
        if generator.is_loaded:
            print("✅ Model loaded successfully!")
            
            # Test generation
            result = generator.generate_story(
                "A young warrior discovers a legendary sword",
                "shonen"
            )
            
            if result["success"]:
                print("✅ Story generation successful!")
                print(f"Generated: {result['text'][:100]}...")
            else:
                print(f"❌ Generation failed: {result['error']}")
        else:
            print("❌ Model failed to load")
    else:
        print(f"❌ Fine-tuned model not found at {model_path}")
        print("Run fine_tune_anime_model.py first to create your model")
    
    print("\n" + "=" * 50)
    print("To integrate into your app:")
    add_finetuned_to_app()

if __name__ == "__main__":
    main()
