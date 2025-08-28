"""
Epic Changelog Agent
A theatrical changelog generator that transforms mundane updates into epic narratives.
"""

import os
import sys
from typing import Optional
import click
from dotenv import load_dotenv
from colorama import init, Fore, Style
from .epic_log_generator import EpicChangelogAgent


# Initialize colorama for Windows terminal colors
init()

# Load environment variables
load_dotenv()

def print_epic_banner():
    """Print the epic banner."""
    banner = f"""{Fore.YELLOW}╔════════════════════════════════════════════════════════════╗
║  ⚔️ EPIC LOGGER AGENT (Powered by AI) ⚔️                     ║
║  Transforming mundane updates into legendary tales...      ║
╚════════════════════════════════════════════════════════════╝
    {Style.RESET_ALL}
"""
    print(banner)

def print_available_themes(agent):
    """Display available themes to the user."""
    print(f"\n{Fore.CYAN}🎭 Available Themes:{Style.RESET_ALL}")
    
    themes_by_source = agent.get_themes_by_source()
    
    # Show default themes
    if themes_by_source["default"]:
        print(f"\n  {Fore.GREEN}📦 Default Themes:{Style.RESET_ALL}")
        for theme_name in themes_by_source["default"]:
            theme_data = agent.theme_loader.get_theme(theme_name)
            emoji = theme_data.get("emoji", "🎭")
            display_name = theme_data.get("display_name", theme_name)
            description = theme_data.get("description", "")
            print(f"    {emoji} {Fore.YELLOW}{theme_name}{Style.RESET_ALL}: {description}")
    
    # Show custom themes
    if themes_by_source["custom"]:
        print(f"\n  {Fore.CYAN}🎨 Custom Themes:{Style.RESET_ALL}")
        for theme_name in themes_by_source["custom"]:
            theme_data = agent.theme_loader.get_theme(theme_name)
            emoji = theme_data.get("emoji", "🎭")
            display_name = theme_data.get("display_name", theme_name)
            description = theme_data.get("description", "")
            print(f"    {emoji} {Fore.YELLOW}{theme_name}{Style.RESET_ALL}: {description}")
    
    print()

def get_dynamic_theme_choices(agent):
    """Get theme choices dynamically from loaded themes."""
    return agent.get_available_themes()


@click.command()
@click.argument('text', required=False)
@click.option('--drama-level', '-d', default=int(os.getenv('DEFAULT_DRAMA_LEVEL', '7')),
              type=click.IntRange(1, 10), help='Drama level from 1 (mild) to 10 (maximum)')
@click.option('--theme', '-t', default=os.getenv('DEFAULT_THEME', 'medieval'),
              help='Choose your epic theme (use --list-themes to see available options)')
@click.option('--model', '-m', default=os.getenv('DEFAULT_MODEL'),
              help='Google Generative AI model to use')
@click.option('--file', '-f', 'input_file', help='Process a file with multiple changelog entries')
@click.option('--output', '-o', help='Save epic changelogs to file')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode')
@click.option('--list-themes', is_flag=True, help='List all available themes and exit')
@click.option('--create-theme', help='Create a custom theme template with given name')
@click.option('--add-theme', help='Add a custom theme from JSON file path')
def main(text: Optional[str], drama_level: int, theme: str, model: str, input_file: Optional[str],
         output: Optional[str], interactive: bool, list_themes: bool, create_theme: Optional[str], 
         add_theme: Optional[str]):
    """Transform boring changelogs into EPIC narratives! ⚔️"""

    print_epic_banner()

    try:
        agent = EpicChangelogAgent(model=model)
    except ValueError as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}Please set your Google API key in the .env file or GOOGLE_API_KEY environment variable.{Style.RESET_ALL}")
        sys.exit(1)

    # Handle theme management commands
    if list_themes:
        print_available_themes(agent)
        return
    
    if create_theme:
        success = agent.create_custom_theme_template(create_theme)
        if success:
            click.echo(f"{Fore.GREEN}✅ Custom theme template created: {create_theme}_theme.json{Style.RESET_ALL}")
            click.echo(f"{Fore.CYAN}📝 Edit the template in Themes/Custom_Themes/ directory{Style.RESET_ALL}")
        return
    
    if add_theme:
        success = agent.add_custom_theme(add_theme, permanent=True)
        if success:
            click.echo(f"{Fore.GREEN}✅ Custom theme added successfully!{Style.RESET_ALL}")
        return

    # Validate theme
    available_themes = agent.get_available_themes()
    if theme not in available_themes:
        click.echo(f"{Fore.YELLOW}⚠️ Theme '{theme}' not found. Available themes:{Style.RESET_ALL}")
        for available_theme in available_themes:
            theme_data = agent.theme_loader.get_theme(available_theme)
            emoji = theme_data.get("emoji", "🎭")
            print(f"  {emoji} {available_theme}")
        click.echo(f"{Fore.CYAN}Using default theme 'medieval'{Style.RESET_ALL}")
        theme = "medieval"

    results = []
    
    if interactive:
        click.echo(f"{Fore.CYAN}🎭 Interactive Epic Changelog Mode{Style.RESET_ALL}")
        click.echo(f"Theme: {theme} | Drama Level: {drama_level}")
        click.echo("Enter changelog entries (empty line to finish):\n")

        while True:
            entry = input(f"{Fore.GREEN}> {Style.RESET_ALL}")
            if not entry.strip():
                break

            epic_version = agent.generate_epic_changelog(entry, drama_level, theme)
            click.echo(f"{Fore.BLUE}Epic: {Style.RESET_ALL}{epic_version}\n")
            results.append(f"Original: {entry}\nEpic: {epic_version}\n")

    elif input_file:
        click.echo(f"{Fore.CYAN}📜 Processing sacred scroll: {input_file}{Style.RESET_ALL}")
        results = agent.process_changelog_file(input_file, drama_level, theme)
        for result in results:
            click.echo(result)

    elif text:
        epic_version = agent.generate_epic_changelog(text, drama_level, theme)
        click.echo(f"{Fore.GREEN}Original:{Style.RESET_ALL} {text}")
        click.echo(f"{Fore.BLUE}Epic:{Style.RESET_ALL} {epic_version}")
        results.append(f"Original: {text}\nEpic: {epic_version}\n")

    else:
        # Show example
        example_text = "Fixed minor bug in login form"
        epic_version = agent.generate_epic_changelog(example_text, drama_level, theme)
        click.echo(f"{Fore.CYAN}🎭 Example Transformation:{Style.RESET_ALL}")
        click.echo(f"{Fore.GREEN}Original:{Style.RESET_ALL} {example_text}")
        click.echo(f"{Fore.BLUE}Epic:{Style.RESET_ALL} {epic_version}")
        click.echo(f"\n{Fore.YELLOW}Use --help to see all options, or provide text to transform!{Style.RESET_ALL}")

    # Save to output file if specified
    if output and results:
        try:
            with open(output, 'w', encoding='utf-8') as f:
                f.write("# Epic Changelog Transformations\n\n")
                f.write(f"Theme: {theme} | Drama Level: {drama_level}\n\n")
                for result in results:
                    f.write(result + "\n")
            click.echo(f"{Fore.GREEN}✨ Epic transformations saved to: {output}{Style.RESET_ALL}")
        except Exception as e:
            click.echo(f"{Fore.RED}Failed to save epic chronicles: {e}{Style.RESET_ALL}")


if __name__ == '__main__':
    main()
