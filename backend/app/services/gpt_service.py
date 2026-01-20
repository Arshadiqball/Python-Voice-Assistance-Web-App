import os
from dotenv import load_dotenv
from openai import OpenAI
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import asyncio
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

class GPTService:
    def __init__(self):
        self.openai_client = None
        self.local_model = None
        self.tokenizer = None
        self.use_openai = False
        self.executor = ThreadPoolExecutor(max_workers=1)
        self._initialize()
    
    def _initialize(self):
        """Initialize GPT service - try OpenAI first, fallback to local model"""
        api_key = os.getenv("OPENAI_API_KEY")
        
        if api_key and api_key != "your_openai_api_key_here":
            try:
                self.openai_client = OpenAI(api_key=api_key)
                self.use_openai = True
                print("Using OpenAI API for GPT")
            except Exception as e:
                print(f"Error initializing OpenAI: {e}, falling back to local model")
                self._load_local_model()
        else:
            print("No OpenAI API key found, using local model")
            self._load_local_model()
    
    def _load_local_model(self):
        """Load local GPT model as fallback"""
        try:
            print("Loading local GPT model (gpt2)...")
            model_name = "gpt2"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.local_model = AutoModelForCausalLM.from_pretrained(model_name)
            self.local_model.eval()
            print("Local GPT model loaded successfully")
        except Exception as e:
            print(f"Error loading local GPT model: {e}")
            # Use a simple fallback
            self.local_model = None
    
    def is_ready(self):
        return self.openai_client is not None or self.local_model is not None
    
    async def generate_response(self, user_input: str, intent: str) -> str:
        """
        Generate response using GPT based on user input and intent
        """
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            self.executor,
            self._generate_response_sync,
            user_input,
            intent
        )
        return response
    
    def _generate_response_sync(self, user_input: str, intent: str) -> str:
        """Synchronous response generation"""
        try:
            # Create context-aware prompt
            system_prompt = f"You are a helpful voice assistant. The user's intent is: {intent}."
            prompt = f"{system_prompt}\nUser: {user_input}\nAssistant:"
            
            if self.use_openai and self.openai_client:
                # Use OpenAI API
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"You are a helpful voice assistant. The user's intent is: {intent}."},
                        {"role": "user", "content": user_input}
                    ],
                    max_tokens=150,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            
            elif self.local_model and self.tokenizer:
                # Use local GPT model
                inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
                
                with torch.no_grad():
                    outputs = self.local_model.generate(
                        inputs,
                        max_length=inputs.shape[1] + 100,
                        num_return_sequences=1,
                        temperature=0.7,
                        do_sample=True,
                        pad_token_id=self.tokenizer.eos_token_id
                    )
                
                generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                # Extract only the assistant's response
                if "Assistant:" in generated_text:
                    response = generated_text.split("Assistant:")[-1].strip()
                else:
                    response = generated_text[len(prompt):].strip()
                
                # Clean up response
                response = response.split("\n")[0].strip()
                return response if response else "I understand. How can I help you?"
            
            else:
                # Fallback response
                return self._get_fallback_response(intent, user_input)
                
        except Exception as e:
            print(f"Response generation error: {str(e)}")
            return self._get_fallback_response(intent, user_input)
    
    def _get_fallback_response(self, intent: str, user_input: str) -> str:
        """Fallback responses based on intent"""
        responses = {
            "greeting": "Hello! How can I assist you today?",
            "question": "That's an interesting question. Let me help you with that.",
            "command": "I understand you want me to do something. Could you provide more details?",
            "information": "I'd be happy to provide information about that topic.",
            "conversation": "I'm here to help. What would you like to know?",
            "goodbye": "Goodbye! Have a great day!"
        }
        return responses.get(intent, "I'm here to help. How can I assist you?")


