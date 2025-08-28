"""
Epic Changelog Agent
A theatrical changelog generator that transforms mundane updates into epic narratives.
"""

import os
from typing import List, Optional, Dict
from dotenv import load_dotenv
from colorama import Fore, Style
from google import genai
from google.genai import types
from .theme_loader import ThemeLoader

# Load environment variables
load_dotenv()

class EpicChangelogAgent:
    """Module for epic changelogs generation."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, custom_themes_dir: Optional[str] = None):
        """Initialize the agent with Google API key and load themes."""
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model = model or os.getenv("DEFAULT_MODEL")
        
        # Load themes from JSON files using ThemeLoader
        try:
            self.theme_loader = ThemeLoader(custom_themes_dir)
            print(f"{Fore.GREEN}✅ Loaded {len(self.theme_loader.get_available_themes())} themes{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}⚠️ Failed to load themes: {e}{Style.RESET_ALL}")
            raise
        
        # API setup
        self.use_api = True
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
                print(f"{Fore.GREEN}🤗 Using Google Generative AI{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️ API setup failed: {e}{Style.RESET_ALL}")
                self.use_api = False
        else:
            self.use_api = False

        if not self.use_api:
            raise ValueError("GOOGLE_API_KEY is required. Set GOOGLE_API_KEY in environment or .env file")

    def get_available_themes(self) -> List[str]:
        """Get list of available theme names."""
        return self.theme_loader.get_available_themes()
    
    def get_theme_descriptions(self) -> Dict[str, str]:
        """Get theme descriptions for help display."""
        return self.theme_loader.get_theme_info()
    
    def get_themes_by_source(self) -> Dict[str, List[str]]:
        """Get themes organized by source (default/custom)."""
        return self.theme_loader.get_themes_by_source()
    
    def add_custom_theme(self, theme_file_path: str, permanent: bool = False) -> bool:
        """Add a custom theme from JSON file."""
        return self.theme_loader.add_custom_theme(theme_file_path, permanent)

    def create_custom_theme_template(self, theme_name: str = "my_theme") -> bool:
        """Create a template for a new custom theme."""
        return self.theme_loader.create_custom_theme_template(theme_name)
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
        
        # Get theme data from ThemeLoader
        theme_data = self.theme_loader.get_theme(theme.lower())
        if not theme_data:
            print(f"{Fore.YELLOW}⚠️ Theme '{theme}' not found, using 'medieval'{Style.RESET_ALL}")
            theme_data = self.theme_loader.get_theme("medieval")
            theme = "medieval"

        theme_vocabulary = ", ".join(theme_data["vocabulary"][:8])
        theme_metaphors = ", ".join(theme_data["metaphors"][:6])
        drama_instructions = self._get_drama_instructions(drama_level)

        system_message = f"""You are a creative storyteller specializing in {theme_data["tone"]} narratives.

Transform software changes into epic {theme} stories using this vocabulary: {theme_vocabulary}
Include metaphors like: {theme_metaphors}
{drama_instructions}

Keep responses to 7-10 words with an appropriate emoji. Be direct and dramatic."""

        try:
            if self.use_api:
                response = self.client.models.generate_content(
                    model=self.model,
                    config=types.GenerateContentConfig(
                        system_instruction=system_message,
                    ),
                    contents=f"Transform this software change into an epic {theme} tale: '{original_text}'"
                )
                
                content = response.text.strip()

                # Add theme-specific emoji if not present
                theme_emoji = theme_data.get("emoji", "🎭")
                if not any(emoji in content for emoji in ['⚔️', '🏰', '🐉', '🚀', '💥', '⚡', '🎭', '🤖', '🏴‍☠️', '🤠']):
                    content = f"{theme_emoji} {content}"

                return content
            else:
                return "😢 Epic transformation unavailable - please check your setup"

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