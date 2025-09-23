import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config
from transformers import TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from datasets import load_dataset
import os

class AnimeGPT2Trainer:
    def __init__(self, model_name='gpt2-medium', output_dir='./models'):
        self.model_name = model_name
        self.output_dir = output_dir
        self.device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
        
        print(f"Using device: {self.device}")
        
        # Initialize tokenizer and model
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Custom configuration for ~200M parameters
        config = GPT2Config.from_pretrained(model_name)
        config.n_layer = 24  # Adjust layers
        config.n_head = 16
        config.n_embd = 1024
        
        self.model = GPT2LMHeadModel.from_pretrained(model_name, config=config)
        self.model.to(self.device)
        
        # Add special tokens for anime storytelling
        special_tokens = {
            'additional_special_tokens': [
                '[SCENE]', '[CHARACTER]', '[DIALOGUE]', '[ACTION]',
                '[SHONEN]', '[SHOJO]', '[ISEKAI]', '[MECHA]', '[SLICE_OF_LIFE]'
            ]
        }
        self.tokenizer.add_special_tokens(special_tokens)
        self.model.resize_token_embeddings(len(self.tokenizer))
        
    def prepare_dataset(self, data_path='data/anime_stories.txt'):
        """Prepare dataset for training"""
        if not os.path.exists(data_path):
            print(f"Data file not found at {data_path}")
            print("Creating sample dataset...")
            self._create_sample_data(data_path)
        
        dataset = TextDataset(
            tokenizer=self.tokenizer,
            file_path=data_path,
            block_size=128
        )
        
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        return dataset, data_collator
    
    def _create_sample_data(self, data_path):
        """Create sample anime story data"""
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        
        sample_stories = [
            "[SHONEN] [SCENE] The sun rose over Tokyo as Kenji prepared for his entrance exam. [CHARACTER] Kenji, a determined 15-year-old with spiky black hair, grabbed his bag. [DIALOGUE] 'Today's the day I prove everyone wrong!' he shouted.",
            "[ISEKAI] [SCENE] A blinding light engulfed Hana as she walked home from school. [ACTION] She opened her eyes to find herself in a medieval fantasy world. [CHARACTER] A mysterious elf appeared before her.",
            "[SLICE_OF_LIFE] [SCENE] The cherry blossoms danced in the spring breeze. [CHARACTER] Yuki sat on the park bench, sketching the scenery. [DIALOGUE] 'This moment is perfect,' she whispered."
        ]
        
        with open(data_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(sample_stories * 100))  # Repeat for more data
        
        print(f"Sample data created at {data_path}")
    
    def train(self, epochs=3, batch_size=4, learning_rate=5e-5):
        """Train the model"""
        dataset, data_collator = self.prepare_dataset()
        
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            overwrite_output_dir=True,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            save_steps=500,
            save_total_limit=2,
            learning_rate=learning_rate,
            warmup_steps=100,
            logging_steps=50,
            logging_dir='./logs',
            report_to='none'
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=dataset
        )
        
        print("Starting training...")
        trainer.train()
        
        # Save model
        self.model.save_pretrained(self.output_dir)
        self.tokenizer.save_pretrained(self.output_dir)
        print(f"Model saved to {self.output_dir}")

if __name__ == "__main__":
    trainer = AnimeGPT2Trainer()
    trainer.train(epochs=3, batch_size=2)
    print("Training complete!")