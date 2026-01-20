from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
from dotenv import load_dotenv
import asyncio
from concurrent.futures import ThreadPoolExecutor
import numpy as np

load_dotenv()

class BertService:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.model_name = os.getenv("BERT_MODEL", "bert-base-uncased")
        self.executor = ThreadPoolExecutor(max_workers=1)
        
        # Intent categories for classification
        self.intents = [
            "greeting",
            "question",
            "command",
            "information",
            "conversation",
            "goodbye"
        ]
        self._load_model()
    
    def _load_model(self):
        """Load BERT model for intent classification"""
        print(f"Loading BERT model: {self.model_name}")
        try:
            # For intent classification, we'll use a simple approach
            # In production, you'd use a fine-tuned model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Use a sequence classification model
            # We'll create a simple classifier using BERT embeddings
            from transformers import AutoModel
            self.model = AutoModel.from_pretrained(self.model_name)
            self.model.eval()
            
            print("BERT model loaded successfully")
        except Exception as e:
            print(f"Error loading BERT model: {e}")
            raise
    
    def is_loaded(self):
        return self.model is not None and self.tokenizer is not None
    
    async def classify_intent(self, text: str) -> str:
        """
        Classify intent of the text using BERT embeddings
        """
        if not self.model or not self.tokenizer:
            raise Exception("BERT model not loaded")
        
        loop = asyncio.get_event_loop()
        intent = await loop.run_in_executor(
            self.executor,
            self._classify_intent_sync,
            text
        )
        return intent
    
    def _classify_intent_sync(self, text: str) -> str:
        """Synchronous intent classification"""
        try:
            # Tokenize input
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=128,
                padding=True
            )
            
            # Get BERT embeddings
            with torch.no_grad():
                outputs = self.model(**inputs)
                # Use [CLS] token embedding
                embeddings = outputs.last_hidden_state[:, 0, :].numpy()
            
            # Simple rule-based intent classification based on keywords
            # In production, use a fine-tuned classifier
            text_lower = text.lower()
            
            if any(word in text_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
                return "greeting"
            elif any(word in text_lower for word in ["what", "how", "why", "when", "where", "who", "?"]):
                return "question"
            elif any(word in text_lower for word in ["play", "stop", "open", "close", "turn on", "turn off", "set"]):
                return "command"
            elif any(word in text_lower for word in ["tell me", "explain", "describe", "information"]):
                return "information"
            elif any(word in text_lower for word in ["bye", "goodbye", "see you", "farewell"]):
                return "goodbye"
            else:
                return "conversation"
                
        except Exception as e:
            print(f"Intent classification error: {str(e)}")
            return "conversation"  # Default fallback


