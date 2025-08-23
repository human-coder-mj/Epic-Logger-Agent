"""
Epic Changelog Agent
A theatrical changelog generator that transforms mundane updates into epic narratives.
"""

import os
from typing import List, Optional
from dotenv import load_dotenv
from colorama import init, Fore, Style
from huggingface_hub import InferenceClient
import requests
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

init()

# Load environment variables
load_dotenv()

class EpicChangelogAgent:
    """Module for epic changelogs generation."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize the agent with Hugging Face API key."""
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        self.model = model or os.getenv("DEFAULT_MODEL")

        # Try different approaches for text generation
        self.use_api = True
        self.local_pipeline = None

        if self.api_key:
            try:
                self.client = InferenceClient(
                    provider="fireworks-ai",
                    token=self.api_key
                )
                print(f"{Fore.CYAN}🤗 Using Hugging Face Inference API{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️ API setup failed: {e}{Style.RESET_ALL}")
                self.use_api = False
        else:
            self.use_api = False

        # Fallback to local transformers if API fails
        if not self.use_api:
            if TRANSFORMERS_AVAILABLE:
                try:
                    print(f"{Fore.CYAN}🤗 Using local Hugging Face Transformers{Style.RESET_ALL}")
                    self.local_pipeline = pipeline(
                        "text-generation", 
                        model="gpt2",  # Use a simple model that works offline
                        max_length=200,
                        do_sample=True,
                        temperature=0.8
                    )
                except Exception as e:
                    print(f"{Fore.YELLOW}⚠️ Local transformers setup failed: {e}{Style.RESET_ALL}")
                    raise ValueError("Neither Hugging Face API nor local transformers are available. Please install transformers or set HUGGINGFACE_API_KEY.") from e
            else:
                raise ValueError("Hugging Face API key is required or install transformers library. Set HUGGINGFACE_API_KEY in environment or .env file, or install transformers.")

        # Dramatic themes and their characteristics
        self.themes = {
            "medieval": {
                "vocabulary": ["vanquished", "forged", "conquered", "wielded", "summoned", "banished", "realm", "sacred", "legendary", "ancient"],
                "metaphors": ["dragon", "knight", "sword", "castle", "quest", "prophecy", "dark magic", "holy grail", "enchanted"],
                "tone": "epic fantasy adventure"
            },
            "space": {
                "vocabulary": ["obliterated", "engineered", "navigated", "transmitted", "launched", "terraformed", "galaxy", "cosmic", "stellar", "quantum"],
                "metaphors": ["starship", "alien threat", "black hole", "wormhole", "space station", "nebula", "asteroid belt", "hyperdrive"],
                "tone": "galactic space opera"
            },
            "superhero": {
                "vocabulary": ["defeated", "empowered", "protected", "rescued", "unleashed", "transformed", "city", "ultimate", "mighty", "heroic"],
                "metaphors": ["villain", "superpower", "secret identity", "fortress", "energy beam", "time rift", "dimensional portal", "crime wave"],
                "tone": "superhero comic book adventure"
            },
            "mythology": {
                "vocabulary": ["decreed", "blessed", "cursed", "awakened", "ordained", "proclaimed", "divine", "immortal", "eternal", "mystical"],
                "metaphors": ["god", "titan", "oracle", "temple", "lightning bolt", "golden fleece", "underworld", "pantheon"],
                "tone": "mythological epic"
            }
        }
    
    def generate_epic_changelog(self, original_text: str, drama_level: int = 7, theme: str = "medieval") -> str:
        """Transform a boring changelog entry into an epic narrative."""
        
        if theme not in self.themes:
            theme = "medieval"
        
        theme_data = self.themes[theme]
        
        try:
            if self.use_api:
                # Use Hugging Face Inference API with SmolLM3-3B via chat completions
                messages = [
                    {"role": "system", "content": f"You are a creative storyteller. Transform software changes into brief epic {theme} stories. Keep responses to 1-2 sentences with an emoji. Be direct and dramatic."},
                    {"role": "user", "content": f"Transform: '{original_text}'"}
                ]
                
                # Use the chat completions endpoint for SmolLM3
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": self.model,
                    "provider" : "fireworks-ai",
                    "messages": messages,
                    "max_tokens": 150,
                    "temperature": 0.8,
                    "stop": ["<think>"]
                }
                
                response = requests.post(
                    f"https://api-inference.huggingface.co/models/{self.model}/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content'].strip()
                    
                    # Clean up any incomplete responses
                    if content.startswith('<think>'):
                        content = content.split('</think>')[-1].strip()
                    
                    # Remove any remaining thinking patterns
                    content = content.replace('<think>', '').replace('</think>', '')

                    
                    # Add emoji if not present
                    if not any(emoji in content for emoji in ['⚔️', '🏰', '🐉', '🚀', '💥', '⚡', '🎭']):
                        emoji_map = {
                            'medieval': '⚔️',
                            'space': '🚀', 
                            'superhero': '💥',
                            'mythology': '⚡'
                        }
                        content = f"{emoji_map.get(theme, '🎭')} {content}"
                    
                    return content
                else:
                    return f"⚠️ API Error: {response.status_code} - {response.text[:100]}"
            
            elif self.local_pipeline:
                # Use local transformers pipeline
                simple_prompt = f"Transform: {original_text} -> Epic {theme}:"
                response = self.local_pipeline(simple_prompt, max_length=150, num_return_sequences=1)
                return response[0]['generated_text'].replace(simple_prompt, '').strip()
            
            else:
                return "🎭 Epic transformation unavailable - please check your setup"
            
        except Exception as e:
            return f"⚠️ Failed to summon the epic transformation: {str(e)}"
    
    def process_changelog_file(self, filename: str, drama_level: int = 7, theme: str = "medieval") -> List[str]:
        """Process a file containing multiple changelog entries."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            
            results = []
            for line in lines:
                epic_version = self.generate_epic_changelog(line, drama_level, theme)
                results.append(f"Original: {line}\nEpic: {epic_version}\n")
            
            return results
            
        except FileNotFoundError:
            return [f"⚠️ The sacred scroll '{filename}' could not be found in this realm!"]
        except Exception as e:
            return [f"⚠️ An unexpected curse befell the file processing: {str(e)}"]