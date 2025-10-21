#!/usr/bin/env python3
"""
Anime Model Fine-Tuning Script
Fine-tune your own anime story generation model using anime datasets.
"""

import torch
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, 
    TrainingArguments, Trainer, DataCollatorForLanguageModeling
)
from datasets import Dataset
import json
import os
from typing import List, Dict
import argparse

class AnimeModelFineTuner:
    def __init__(self, base_model: str = "microsoft/DialoGPT-medium"):
        """
        Initialize the fine-tuner
        
        Args:
            base_model: Base model to fine-tune (recommended: DialoGPT, GPT-2, or Llama)
        """
        self.base_model = base_model
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        # Load tokenizer and model
        print(f"Loading {base_model}...")
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)
        self.model = AutoModelForCausalLM.from_pretrained(base_model)
        
        # Add padding token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Add special tokens for anime storytelling
        special_tokens = {
            'additional_special_tokens': [
                '[SCENE]', '[CHARACTER]', '[DIALOGUE]', '[ACTION]',
                '[SHONEN]', '[SHOJO]', '[ISEKAI]', '[MECHA]', 
                '[SLICE_OF_LIFE]', '[ROMANCE]', '[ACTION]'
            ]
        }
        self.tokenizer.add_special_tokens(special_tokens)
        self.model.resize_token_embeddings(len(self.tokenizer))
        
        print(f"Model loaded successfully!")
        print(f"Vocabulary size: {len(self.tokenizer)}")
        print(f"Model parameters: {self.model.num_parameters():,}")

    def create_anime_dataset(self, data_path: str = "data/anime_stories.json") -> Dataset:
        """Create anime story dataset"""
        
        # Create sample anime stories if data doesn't exist
        if not os.path.exists(data_path):
            print(f"Creating sample anime dataset at {data_path}")
            self._create_sample_dataset(data_path)
        
        # Load dataset
        with open(data_path, 'r', encoding='utf-8') as f:
            stories = json.load(f)
        
        # Format stories for training
        formatted_stories = []
        for story in stories:
            # Format: [GENRE] [SCENE] prompt -> generated story
            formatted_text = f"{story['genre']} [SCENE] {story['prompt']} {story['story']}"
            formatted_stories.append(formatted_text)
        
        # Create dataset
        dataset = Dataset.from_dict({"text": formatted_stories})
        
        print(f"Created dataset with {len(dataset)} stories")
        return dataset

    def _create_sample_dataset(self, data_path: str):
        """Create sample anime story dataset"""
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        
        sample_stories = [
            {
                "genre": "[SHONEN]",
                "prompt": "A young warrior discovers a legendary sword",
                "story": "Kenji's eyes widened as he pulled the ancient blade from its stone pedestal. The sword pulsed with golden energy, and he felt power coursing through his veins. 'This is it,' he whispered, 'the weapon that will help me protect everyone I care about.'"
            },
            {
                "genre": "[ISEKAI]",
                "prompt": "After dying in an accident, a programmer awakens in a fantasy world",
                "story": "Hana opened her eyes to find herself in a medieval fantasy world. A translucent status window appeared before her: 'Welcome, Hero. Level 1.' She examined her new abilities - [Magic], [Sword Mastery], and [Programming Knowledge]. 'I can use my coding skills here too!' she realized."
            },
            {
                "genre": "[MECHA]",
                "prompt": "Teenage pilots must defend Earth from alien invasion",
                "story": "The massive hangar doors opened, revealing Ryu's giant robot against the starlit sky. 'Neural synchronization at 95%,' the AI announced. Enemy signatures appeared on radar as alien ships approached Earth. 'This is it,' Ryu declared, 'time to show them what humanity is made of!'"
            },
            {
                "genre": "[ROMANCE]",
                "prompt": "Two rivals realize their feelings during the school festival",
                "story": "Cherry blossoms danced in the spring breeze as Sakura nervously approached her rival Takeshi. 'I... I have something to tell you,' she stammered, her heart pounding. Takeshi's usual confident expression softened. 'I think I know what you're going to say,' he whispered, taking her hand."
            },
            {
                "genre": "[SLICE_OF_LIFE]",
                "prompt": "Three friends start a band in their final year of high school",
                "story": "The music room echoed with the sound of their first practice. Yuki on guitar, Akira on drums, and Emi on bass. 'This is our last year together,' Yuki said, 'let's make it unforgettable.' They began playing their original song, 'Memories of Tomorrow,' filling the room with hope and friendship."
            },
            {
                "genre": "[ACTION]",
                "prompt": "A demon slayer faces their greatest challenge under the full moon",
                "story": "Under the blood-red moon, Tanjiro gripped his cursed blade tighter. The demon's eyes glowed crimson in the darkness ahead. 'Breath of Water, First Form!' he shouted, channeling his cursed energy. With perfect control, he unleashed his domain expansion, the very air crackling with supernatural power."
            }
        ]
        
        # Expand dataset by creating variations
        expanded_stories = []
        for story in sample_stories:
            expanded_stories.append(story)
            # Create variations with different character names
            variations = [
                {"Kenji": "Akira", "Hana": "Yuki", "Ryu": "Takeshi", "Sakura": "Emi", "Tanjiro": "Hiroto"},
                {"Kenji": "Daiki", "Hana": "Rei", "Ryu": "Shun", "Sakura": "Aoi", "Tanjiro": "Hayato"},
                {"Kenji": "Ryu", "Hana": "Misaki", "Ryu": "Kaito", "Sakura": "Miku", "Tanjiro": "Sora"}
            ]
            
            for variation in variations:
                new_story = story.copy()
                for old_name, new_name in variation.items():
                    new_story["story"] = new_story["story"].replace(old_name, new_name)
                expanded_stories.append(new_story)
        
        # Save dataset
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(expanded_stories, f, indent=2, ensure_ascii=False)
        
        print(f"Created {len(expanded_stories)} anime stories")

    def prepare_dataset_for_training(self, dataset: Dataset) -> Dataset:
        """Prepare dataset for training"""
        
        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                padding=True,
                max_length=512,
                return_tensors="pt"
            )
        
        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=dataset.column_names
        )
        
        return tokenized_dataset

    def fine_tune(self, 
                  dataset: Dataset,
                  output_dir: str = "./anime_model",
                  num_epochs: int = 3,
                  batch_size: int = 4,
                  learning_rate: float = 5e-5):
        """Fine-tune the model"""
        
        print("Preparing dataset for training...")
        tokenized_dataset = self.prepare_dataset_for_training(dataset)
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            warmup_steps=100,
            learning_rate=learning_rate,
            logging_steps=50,
            logging_dir=f"{output_dir}/logs",
            save_steps=500,
            save_total_limit=2,
            evaluation_strategy="no",
            report_to="none",
            dataloader_drop_last=True,
        )
        
        # Initialize trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=tokenized_dataset,
        )
        
        print("Starting fine-tuning...")
        print(f"Training for {num_epochs} epochs with batch size {batch_size}")
        print(f"Learning rate: {learning_rate}")
        
        # Train
        trainer.train()
        
        # Save model
        print(f"Saving fine-tuned model to {output_dir}")
        trainer.save_model()
        self.tokenizer.save_pretrained(output_dir)
        
        print("Fine-tuning complete!")
        return output_dir

    def test_model(self, model_path: str, prompt: str, genre: str = "[SHONEN]"):
        """Test the fine-tuned model"""
        
        # Load fine-tuned model
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(model_path)
        
        # Prepare input
        full_prompt = f"{genre} [SCENE] {prompt}"
        input_ids = tokenizer.encode(full_prompt, return_tensors='pt')
        
        # Generate
        with torch.no_grad():
            output = model.generate(
                input_ids,
                max_length=input_ids.shape[1] + 100,
                temperature=0.8,
                top_p=0.95,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                no_repeat_ngram_size=3
            )
        
        # Decode
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        
        print("=" * 60)
        print("FINE-TUNED MODEL TEST")
        print("=" * 60)
        print(f"Prompt: {full_prompt}")
        print(f"Generated: {generated_text}")
        print("=" * 60)
        
        return generated_text

def main():
    parser = argparse.ArgumentParser(description="Fine-tune anime story generation model")
    parser.add_argument("--base_model", default="microsoft/DialoGPT-medium", 
                       help="Base model to fine-tune")
    parser.add_argument("--data_path", default="data/anime_stories.json",
                       help="Path to anime stories dataset")
    parser.add_argument("--output_dir", default="./anime_model",
                       help="Output directory for fine-tuned model")
    parser.add_argument("--epochs", type=int, default=3,
                       help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=4,
                       help="Training batch size")
    parser.add_argument("--learning_rate", type=float, default=5e-5,
                       help="Learning rate")
    parser.add_argument("--test_only", action="store_true",
                       help="Only test existing model")
    
    args = parser.parse_args()
    
    if args.test_only:
        # Test existing model
        fine_tuner = AnimeModelFineTuner(args.base_model)
        fine_tuner.test_model(args.output_dir, 
                            "A young warrior discovers a legendary sword",
                            "[SHONEN]")
    else:
        # Fine-tune model
        fine_tuner = AnimeModelFineTuner(args.base_model)
        
        # Create dataset
        dataset = fine_tuner.create_anime_dataset(args.data_path)
        
        # Fine-tune
        model_path = fine_tuner.fine_tune(
            dataset=dataset,
            output_dir=args.output_dir,
            num_epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.learning_rate
        )
        
        # Test the model
        print("\nTesting fine-tuned model...")
        fine_tuner.test_model(model_path, 
                            "A young warrior discovers a legendary sword",
                            "[SHONEN]")

if __name__ == "__main__":
    main()
