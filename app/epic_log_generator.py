"""
Epic Changelog Agent
A theatrical changelog generator that transforms mundane updates into epic narratives.
"""

import os
from typing import List, Optional
from dotenv import load_dotenv
from colorama import init, Fore, Style
from google import genai
from google.genai import types

init()

# Load environment variables
load_dotenv()

class EpicChangelogAgent:
    """Module for epic changelogs generation."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize the agent with Hugging Face API key."""
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model = model or os.getenv("DEFAULT_MODEL")

        # Try different approaches for text generation
        self.use_api = True
        self.local_pipeline = None

        if self.api_key:
            try:
                self.client = genai.Client(
                    api_key=self.api_key
                )
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️ API setup failed: {e}{Style.RESET_ALL}")
                self.use_api = False
        else:
            self.use_api = False

        # Fallback to local transformers if API fails
        if not self.use_api:
            raise ValueError("GOOGLE_API_Key is required. Set GOOGLE_API_Key  in environment or .env file")

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
    def _get_drama_instructions(self, drama_level: int) -> str:
        """Generate drama-specific instructions based on level."""
        if drama_level <= 3:
            return "Use subtle epic language with moderate excitement."
        elif drama_level <= 6:
            return "Use dramatic language with strong action words and vivid imagery."
        elif drama_level <= 8:
            return "Use highly dramatic language with intense action, multiple adjectives, and epic stakes."
        else:
            return "Use MAXIMUM DRAMA with over-the-top language, legendary consequences, and world-shaking events!"
    
    def generate_epic_changelog(self, original_text: str, drama_level: int = 7, theme: str = "medieval") -> str:
        """Transform a boring changelog entry into an epic narrative."""

        if theme not in self.themes:
            theme = "medieval"

        theme_data = self.themes[theme]

        theme_vocabulary = ", ".join(theme_data["vocabulary"][:8])  # Use first 8 words
        theme_metaphors = ", ".join(theme_data["metaphors"][:6])   # Use first 6 metaphors

        # Adjust drama based on drama_level
        drama_instructions = self._get_drama_instructions(drama_level)

        system_message = f"""You are a creative storyteller specializing in {theme_data["tone"]} narratives.

        Transform software changes into epic {theme} stories using this vocabulary: {theme_vocabulary}
        Include metaphors like: {theme_metaphors}
        {drama_instructions}

        Keep responses to 7-10 words with an appropriate emoji. Be direct and dramatic."""


        try:
            if self.use_api:

                max_tokens = min(200, 100 + (drama_level * 10))
                temperature = min(1.0, 0.5 + (drama_level * 0.05))


                response = self.client.models.generate_content(
                    model=self.model,
                    config=types.GenerateContentConfig(
                        system_instruction=system_message,
                        max_output_tokens=max_tokens,
                        temperature=temperature,
                        ),
                    contents=f"Transform this software change into an epic {theme} tale: '{original_text}'"
                )
                
                result = response.text
                content = result.strip()

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