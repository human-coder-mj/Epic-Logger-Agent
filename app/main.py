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
from epic_log_generator import EpicChangelogAgent


# Initialize colorama for Windows terminal colors
init()

# Load environment variables
load_dotenv()

def print_epic_banner():
    """Print the epic banner."""
    banner = f"""{Fore.YELLOW}╔══════════════════════════════════════════════════════════════╗
║  ⚔️  EPIC CHANGELOG AGENT (Powered by Hugging Face) ⚔️         ║
║  Transforming mundane updates into legendary tales...        ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


@click.command()
@click.argument('text', required=False)
@click.option('--drama-level', '-d', default=int(os.getenv('DEFAULT_DRAMA_LEVEL', '7')),
              type=click.IntRange(1, 10), help='Drama level from 1 (mild) to 10 (maximum)')
@click.option('--theme', '-t', default=os.getenv('DEFAULT_THEME', 'medieval'),
              type=click.Choice(['medieval', 'space', 'superhero', 'mythology']),
              help='Choose your epic theme')
@click.option('--model', '-m', default=os.getenv('DEFAULT_MODEL'),
              help='Hugging Face model to use')
@click.option('--file', '-f', 'input_file', help='Process a file with multiple changelog entries')
@click.option('--output', '-o', help='Save epic changelogs to file')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode')
def main(text: Optional[str], drama_level: int, theme: str, model: str, input_file: Optional[str],
         output: Optional[str], interactive: bool):
    """Transform boring changelogs into EPIC narratives! ⚔️"""

    print_epic_banner()

    try:
        agent = EpicChangelogAgent(model=model)
    except ValueError as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}Please set your Hugging Face API key in the .env file or HUGGINGFACE_API_KEY environment variable.{Style.RESET_ALL}")
        sys.exit(1)

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
