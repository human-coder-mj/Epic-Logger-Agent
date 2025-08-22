# Epic Changelog Agent 🏰⚔️

An LLM-powered changelog writer that transforms mundane software updates into epic, theatrical narratives.

## Features

- 🎭 Transforms boring changelog entries into dramatic tales
- ⚡ Powered by Hugging Face open-source models
- 🎨 Multiple theatrical styles and themes
- 📝 CLI interface for easy integration
- 🔧 Configurable drama levels

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Hugging Face API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your HUGGINGFACE_API_KEY
   ```

## Usage

### Basic Usage
```bash
python epic_changelog.py "Fixed minor bug in login form"
```

### Output Example
**Input:** "Fixed minor bug in login form"
**Output:** "🗡️ Vanquished a lurking menace that had corrupted the sacred login flow, restoring peace to the realm of user authentication!"

### Advanced Usage
```bash
# Choose drama level (1-10)
python epic_changelog.py "Added new feature" --drama-level 8

# Select theme
python epic_changelog.py "Updated dependencies" --theme medieval

# Choose different Hugging Face model
python epic_changelog.py "Updated docs" --model "microsoft/DialoGPT-large"

# Process multiple entries
python epic_changelog.py --file changelog_input.txt
```

## Drama Levels
- **1-3**: Mildly dramatic
- **4-6**: Moderately epic
- **7-8**: Highly theatrical
- **9-10**: Maximum drama overload

## Themes
- `medieval`: Knights, dragons, and quests
- `space`: Cosmic battles and galactic adventures
- `superhero`: Powers, villains, and heroic deeds
- `mythology`: Gods, legends, and ancient prophecies

## Configuration

Create a `.env` file with:
```
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
DEFAULT_DRAMA_LEVEL=7
DEFAULT_THEME=medieval
DEFAULT_MODEL=microsoft/DialoGPT-medium
```

## Recommended Models

- **microsoft/DialoGPT-medium**: Good balance of quality and speed
- **microsoft/DialoGPT-large**: Higher quality responses
- **facebook/blenderbot-400M-distill**: Fast and lightweight
- **microsoft/DialoGPT-small**: Fastest option

## Development

Run tests:
```bash
python -m pytest tests/
```

## License

MIT License - Transform your boring changelogs into epic tales!
