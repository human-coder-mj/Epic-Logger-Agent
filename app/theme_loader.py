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
            self.themes_root = current_dir / "Themes"
            self.default_themes_dir = self.themes_root / "Default_Themes"
            self.custom_themes_dir = self.themes_root / "Custom_Themes"
        else:
            self.themes_root = Path(themes_dir)
            self.default_themes_dir = self.themes_root / "Default_Themes"
            self.custom_themes_dir = self.themes_root / "Custom_Themes"

        self.themes = {}
        self.load_themes()

    def load_themes(self) -> None:
        """Load all theme JSON files from Default_Themes and Custom_Themes directories."""
        themes_loaded = 0

        # Load default themes (always required)
        if self.default_themes_dir.exists():
            themes_loaded += self._load_themes_from_directory(self.default_themes_dir, "Default")
        else:
            print(f"{Fore.YELLOW}⚠️ Default themes directory not found: {self.default_themes_dir}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}💡 Creating Default_Themes directory...{Style.RESET_ALL}")
            self.default_themes_dir.mkdir(parents=True, exist_ok=True)

        # Load custom themes (optional)
        if self.custom_themes_dir.exists():
            themes_loaded += self._load_themes_from_directory(self.custom_themes_dir, "Custom")
        else:
            print(f"{Fore.CYAN}📁 Custom themes directory not found - creating: {self.custom_themes_dir}{Style.RESET_ALL}")
            self.custom_themes_dir.mkdir(parents=True, exist_ok=True)
            print(f"{Fore.GREEN}✅ Custom_Themes directory created. Add your custom themes here!{Style.RESET_ALL}")
        
        if themes_loaded == 0:
            print(f"{Fore.YELLOW}⚠️ No theme files found in any directory{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}🎭 Total themes loaded: {themes_loaded}{Style.RESET_ALL}")
    
    def _load_themes_from_directory(self, directory: Path, theme_type: str) -> int:
        """Load themes from a specific directory."""
        theme_files = list(directory.glob("*.json"))
        loaded_count = 0
        
        if not theme_files:
            print(f"{Fore.YELLOW}⚠️ No theme files found in {theme_type} themes: {directory}{Style.RESET_ALL}")
            return 0
        
        for theme_file in theme_files:
            try:
                with open(theme_file, 'r', encoding='utf-8') as f:
                    theme_data = json.load(f)

                # Validate theme structure
                if self._validate_theme(theme_data):
                    theme_name = theme_data.get("name", theme_file.stem.replace("_theme", ""))
                    
                    # Add theme type information
                    theme_data["_source"] = theme_type.lower()
                    theme_data["_file_path"] = str(theme_file)
                    
                    self.themes[theme_name] = theme_data
                    loaded_count += 1
                else:
                    print(f"{Fore.YELLOW}⚠️ Invalid theme format in {theme_file.name} ({theme_type}){Style.RESET_ALL}")

            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"{Fore.RED}⚠️ Failed to load {theme_type.lower()} theme {theme_file.name}: {e}{Style.RESET_ALL}")
        
        return loaded_count

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
    
    def get_themes_by_source(self) -> Dict[str, List[str]]:
        """Get themes organized by their source (default/custom)."""
        default_themes = []
        custom_themes = []
        
        for name, data in self.themes.items():
            source = data.get("_source", "unknown")
            if source == "default":
                default_themes.append(name)
            elif source == "custom":
                custom_themes.append(name)
        
        return {
            "default": sorted(default_themes),
            "custom": sorted(custom_themes)
        }
    
    def create_custom_theme_template(self, theme_name: str = "my_theme") -> bool:
        """Create a template JSON file in the Custom_Themes directory."""
        # Ensure Custom_Themes directory exists
        self.custom_themes_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = self.custom_themes_dir / f"{theme_name}_theme.json"
        return self.create_theme_template(str(output_path))

    def add_custom_theme(self, theme_file_path: str, permanent: bool = False) -> bool:
        """Add a custom theme from a JSON file.
        
        Args:
            theme_file_path: Path to the theme JSON file
            permanent: If True, copies the theme to Custom_Themes directory for persistence
        """
        try:
            with open(theme_file_path, 'r', encoding='utf-8') as f:
                theme_data = json.load(f)

            if self._validate_theme(theme_data):
                theme_name = theme_data.get("name", Path(theme_file_path).stem.replace("_theme", ""))

                # Add to memory
                self.themes[theme_name] = theme_data

                if permanent:
                    # Copy to Custom_Themes directory for persistence
                    destination_name = f"{theme_name}_theme.json"
                    destination_path = self.custom_themes_dir / destination_name

                    # Create Custom_Themes directory if it doesn't exist
                    self.custom_themes_dir.mkdir(parents=True, exist_ok=True)

                    # Copy the file
                    shutil.copy2(theme_file_path, destination_path)
                    print(f"{Fore.GREEN}✅ Added permanent custom theme: {theme_name} → {destination_path}{Style.RESET_ALL}")
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
