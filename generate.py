import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import time

class AnimeStoryGenerator:
    def __init__(self, model_path='./models'):
        self.device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
        
        print(f"Loading model from {model_path}...")
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        self.model = GPT2LMHeadModel.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()
        
        print(f"Model loaded on {self.device}")
    
    def generate_story(self, prompt, genre='[SHONEN]', max_length=300, 
                      temperature=0.8, top_k=50, top_p=0.95):
        """Generate an anime story"""
        
        # Add genre tag to prompt
        full_prompt = f"{genre} [SCENE] {prompt}"
        
        print(f"\nPrompt: {full_prompt}\n")
        print("Generating story...\n")
        
        # Tokenize
        input_ids = self.tokenizer.encode(full_prompt, return_tensors='pt').to(self.device)
        
        # Measure inference time
        start_time = time.time()
        
        # Generate
        with torch.no_grad():
            output = self.model.generate(
                input_ids,
                max_length=max_length,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p,
                do_sample=True,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
                no_repeat_ngram_size=3
            )
        
        end_time = time.time()
        
        # Decode
        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=False)
        
        # Calculate stats
        num_tokens = len(output[0])
        inference_time = end_time - start_time
        tokens_per_sec = num_tokens / inference_time
        
        # Calculate perplexity (simplified)
        with torch.no_grad():
            outputs = self.model(output, labels=output)
            perplexity = torch.exp(outputs.loss).item()
        
        print("=" * 60)
        print("GENERATED STORY:")
        print("=" * 60)
        print(generated_text)
        print("\n" + "=" * 60)
        print("PERFORMANCE METRICS:")
        print("=" * 60)
        print(f"Tokens generated: {num_tokens}")
        print(f"Inference time: {inference_time:.2f} seconds")
        print(f"Speed: {tokens_per_sec:.0f} tokens/sec")
        print(f"Perplexity: {perplexity:.2f}")
        print("=" * 60)
        
        return generated_text

def main():
    # Initialize generator
    generator = AnimeStoryGenerator()
    
    # Example prompts for different genres
    prompts = [
        {
            'genre': '[SHONEN]',
            'prompt': 'A young warrior discovers a legendary sword'
        },
        {
            'genre': '[ISEKAI]',
            'prompt': 'After dying in an accident, a programmer awakens in a fantasy world'
        },
        {
            'genre': '[SLICE_OF_LIFE]',
            'prompt': 'The first day of high school brings unexpected friendships'
        },
        {
            'genre': '[MECHA]',
            'prompt': 'Humanity\'s last hope lies in giant robots'
        }
    ]
    
    # Interactive mode
    print("\n🎬 Anime Story Generator 🎬")
    print("\nAvailable genres: [SHONEN], [SHOJO], [ISEKAI], [MECHA], [SLICE_OF_LIFE]")
    print("\nType 'quit' to exit\n")
    
    while True:
        user_input = input("\nEnter your story prompt (or press Enter for examples): ").strip()
        
        if user_input.lower() == 'quit':
            break
        
        if not user_input:
            # Use example prompts
            print("\nGenerating example stories...\n")
            for example in prompts[:2]:  # Generate 2 examples
                generator.generate_story(
                    prompt=example['prompt'],
                    genre=example['genre'],
                    max_length=200
                )
        else:
            # Get genre
            genre = input("Enter genre (default: [SHONEN]): ").strip() or '[SHONEN]'
            generator.generate_story(prompt=user_input, genre=genre)

if __name__ == "__main__":
    main()