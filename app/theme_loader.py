"""Theme loading utility for Epic Changelog Agent."""

import json
import shutil
from typing import Dict, List, Optional
from pathlib import Path
from colorama import Fore, Style

class ThemeLoader:
    """Loads and manages themes from JSON files."""

    def __init__(self, themes_dir: Optional[str] = None):
        """Initialize the theme loader."""
        if themes_dir is None:
            # Default to Themes directory relative to project root
            current_dir = Path(__file__).parent.parent
            self.themes_dir = current_dir / "Themes"
        else:
            self.themes_dir = Path(themes_dir)

        self.themes = {}
        self.load_themes()

    def load_themes(self) -> None:
        """Load all theme JSON files from the themes directory."""
        if not self.themes_dir.exists():
            print(f"{Fore.YELLOW}⚠️ Themes directory not found: {self.themes_dir}{Style.RESET_ALL}")
            return

        theme_files = list(self.themes_dir.glob("*_theme.json"))
        if not theme_files:
            print(f"{Fore.YELLOW}⚠️ No theme files found in: {self.themes_dir}{Style.RESET_ALL}")
            return

        for theme_file in theme_files:
            try:
                with open(theme_file, 'r', encoding='utf-8') as f:
                    theme_data = json.load(f)

                # Validate theme structure
                if self._validate_theme(theme_data):
                    theme_name = theme_data.get("name", theme_file.stem.replace("_theme", ""))
                    self.themes[theme_name] = theme_data
                    print(f"{Fore.GREEN}✅ Loaded theme: {theme_name}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}⚠️ Invalid theme format in {theme_file.name}{Style.RESET_ALL}")

            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"{Fore.RED}⚠️ Failed to load theme {theme_file.name}: {e}{Style.RESET_ALL}")

    def _validate_theme(self, theme_data: Dict) -> bool:
        """Validate that a theme has required fields."""
        required_fields = ["vocabulary", "metaphors", "tone"]
        return all(field in theme_data for field in required_fields)

    def get_theme(self, theme_name: str) -> Optional[Dict]:
        """Get a specific theme by name."""
        return self.themes.get(theme_name.lower())

    def get_available_themes(self) -> List[str]:
        """Get list of available theme names."""
        return list(self.themes.keys())

    def get_theme_info(self) -> Dict[str, str]:
        """Get theme names and descriptions."""
        return {
            name: data.get("description", f"{data.get('display_name', name)} theme")
            for name, data in self.themes.items()
        }

    def add_custom_theme(self, theme_file_path: str, permanent: bool = False) -> bool:
        """Add a custom theme from a JSON file.
        
        Args:
            theme_file_path: Path to the theme JSON file
            permanent: If True, copies the theme to Themes directory for persistence
        """
        try:
            with open(theme_file_path, 'r', encoding='utf-8') as f:
                theme_data = json.load(f)

            if self._validate_theme(theme_data):
                theme_name = theme_data.get("name", Path(theme_file_path).stem.replace("_theme", ""))

                # Add to memory
                self.themes[theme_name] = theme_data

                if permanent:
                    # Copy to Themes directory for persistence
                    destination_name = f"{theme_name}_theme.json"
                    destination_path = self.themes_dir / destination_name

                    # Create Themes directory if it doesn't exist
                    self.themes_dir.mkdir(exist_ok=True)

                    # Copy the file
                    shutil.copy2(theme_file_path, destination_path)
                    print(f"{Fore.GREEN}✅ Added permanent theme: {theme_name} → {destination_path}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}✅ Added temporary theme: {theme_name} (session only){Style.RESET_ALL}")

                return True
            else:
                print(f"{Fore.YELLOW}⚠️ Invalid theme format in {theme_file_path}{Style.RESET_ALL}")
                return False
    
        except Exception as e:
            print(f"{Fore.RED}⚠️ Failed to add custom theme: {e}{Style.RESET_ALL}")
            return False

    def create_theme_template(self, output_path: str) -> bool:
        """Create a template JSON file for new themes."""
        template = {
            "name": "my_theme",
            "display_name": "My Custom Theme",
            "vocabulary": [
                "word1", "word2", "word3", "word4", "word5", 
                "word6", "word7", "word8", "word9", "word10"
            ],
            "metaphors": [
                "metaphor1", "metaphor2", "metaphor3", "metaphor4", 
                "metaphor5", "metaphor6", "metaphor7", "metaphor8"
            ],
            "tone": "describe your theme's tone here",
            "emoji": "🎭",
            "description": "Describe what this theme does"
        }

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=4)
            print(f"{Fore.GREEN}✅ Theme template created: {output_path}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}⚠️ Failed to create template: {e}{Style.RESET_ALL}")
            return False
