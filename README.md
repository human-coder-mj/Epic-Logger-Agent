# Epic Logger Agent 🏰⚔️

An LLM-powered changelog writer that transforms mundane software updates into epic, theatrical narratives.

## Features

- 🎭 Transforms boring changelog entries into dramatic tales
- ⚡ Powered by Hugging Face open-source models
- 🎨 Multiple theatrical styles and themes
- 📝 CLI interface for easy integration
- 🔧 Configurable drama levels
- 📦 Easy pip-style installation

## Installation

### Option 1: Install as Package (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd Epic-Logger-Agent

# Install the package
pip install -e .
```

### Option 2: Manual Installation
```bash
# Clone this repository
git clone <repository-url>
cd Epic-Logger-Agent

# Install dependencies
pip install -r requirements.txt
```

## Setup

Set up your Hugging Face API key:
```bash
# Create .env file with your API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

## Usage

### CLI Commands (After Package Installation)

The package provides three convenient commands:

```bash
# Primary command
epiclog "Fixed minor bug in login form"

# Alternative alias
changelog "Fixed minor bug in login form"
```

### Command Options

```bash
# Choose drama level (1-10)
epiclog "Added new feature" --drama-level 8

# Select theme
epiclog "Updated dependencies" --theme space

# Interactive mode
epiclog --interactive

# Process file with multiple entries
epiclog --file changelog_input.txt

# Save output to file
epiclog "Fixed bug" --output epic_changes.txt
```

### Example Output
- **Input:** "Fixed minor bug in login form"
- **Output:** "🗡️ Vanquished a lurking menace that had corrupted the sacred login flow, restoring peace to the realm of user authentication!"

### Manual Usage (Without Package Installation)
```bash
# With default drama level(7) and default theme(medieval)
python -m app.main "Fixed minor bug in login form"

# Choose drama level (1-10)
python -m app.main "Added new feature" --drama-level 8

# Select theme
python -m app.main "Updated dependencies" --theme space

# Interactive mode
python -m app.main --interactive

# Process file with multiple entries
python -m app.main --file changelog_input.txt

# Save output to file
python -m app.main --output epic_changes.txt
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
GOOGLE_API_KEY=your_google_api_key_here
DEFAULT_DRAMA_LEVEL=7
DEFAULT_THEME=medieval
DEFAULT_MODEL=gemini-2.5-flash
```

## Development

Run tests:
```bash
python -m pytest tests/
```
