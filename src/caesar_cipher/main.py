from pathlib import Path
from typing import Annotated
import shlex

import typer
from click.testing import CliRunner
from typer.main import get_command

from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

from caesar_cipher.analyzer import FrequencyAnalyzer
from caesar_cipher.cipher import CaesarCipher
from caesar_cipher.utils import write_output, read_input, validate_key



app = typer.Typer(
    name = "caesar-cipher",
    help = "A Caesar cipher encryption, decryption and cracking utility.",
    invoke_without_command = True,
    no_args_is_help = False,
)

console = Console()

BANNER = r"""
   ██████╗ █████╗ ███████╗███████╗ █████╗ ██████╗
  ██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗
  ██║     ███████║█████╗  ███████╗███████║██████╔╝
  ██║     ██╔══██║██╔══╝  ╚════██║██╔══██║██╔══██╗
  ╚██████╗██║  ██║███████╗███████║██║  ██║██║  ██║
   ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
"""

def show_banner() -> None:
    console.print(
        Align.center(
            Text(BANNER, style="bold cyan")
        )
    )

    console.print(
        Panel(
            "[bold]Caesar Cipher CLI[/bold]\n"
            "Encryption, decryption and frequency-analysis cracking utility.\n\n"
            "[dim]Type --help to see available commands.[/dim]",
            title="[bold cyan]Welcome[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

def interactive_mode() -> None:
    show_banner()

    console.print(
        Panel(
            "You are now in [bold cyan]Caesar Mode[/bold cyan].\n"
            "Run commands without typing 'caesar'.\n"
            "Use [bold]Ctrl+Q[/bold] to leave Caesar Mode.",
            title="[bold cyan]Welcome[/bold cyan]",
            border_style="cyan",
        )
    )

    session = PromptSession()
    kb = KeyBindings()

    @kb.add("c-q")
    def exit_caesar(event) -> None:
        event.app.exit()

    while True:
        console.print(
            "[bold cyan]╭─ Command ──────────────────────────────────────────────╮[/bold cyan]"
        )

        try:
            command = session.prompt(
                "╰─> ",
                key_bindings=kb,
            )

            if command is None:
                break
                
            if not command.strip():
                continue

            run_interactive_command(command)

        except KeyboardInterrupt:
            continue

        except EOFError:
            break

    console.print("\n[dim]Leaving Caesar Mode...[/dim]")

def run_interactive_command(command: str) -> None:
    try:
        parts = shlex.split(command)

        if not parts:
            return

        if parts[0].lower() in {"exit", "quit"}:
            raise typer.Exit()

        if parts[0].lower() in {"help", "--help", "-h"}:
            parts.append("--help")

        runner = CliRunner()
        typer_app = get_command(app)

        result = runner.invoke(typer_app, parts)

        if result.output:
            console.print(
                Text.from_ansi(result.output),
                end="")

        if result.exception and not isinstance(result.exception, typer.Exit):
            console.print(
                f"[red]Error:[/red] {result.exception}"
            )

    except ValueError as e:
        console.print(f"[red]Invalid command:[/red] {e}")

@app.command()
def encrypt(
    text: Annotated[str | None, typer.Argument(
                                                help = "Text to encrypt (or use --input-file or stdin)"
                                                )] = None,
    key: Annotated[int, typer.Option(
                                    "--key",
                                    "-k",
                                    help = "Shift key (0-25)"
                                    )] = 3,
    input_file: Annotated[Path | None, typer.Option(
                                                    "--input-file",
                                                    "-i",
                                                    help = "Input file path"
                                                    )] = None,
    output_file: Annotated[Path | None, typer.Option("--output-file", "-o", help = "Output file path")] = None,
    quiet: Annotated[bool, typer.Option("--quiet", "-q", help = "Suppress all output")] = False,
) -> None:

    try:
        validate_key(key)
        plaintext = read_input(text, input_file)
        cipher = CaesarCipher(key = key)
        encrypted = cipher.encrypt(plaintext)

        if not quiet and not output_file: console.print(f"[bold cyan]Encrypted:[/bold cyan] {encrypted}")
        else: write_output(encrypted, output_file, quiet)

    except (ValueError, OSError) as e:
        console.print(f'[red]Error:[/red] {e}')
        raise typer.Exit(code=1) from None

@app.command()
def decrypt(
    text: Annotated[
        str | None,
        typer.Argument(help = "Text to decrypt (or use --input-file or stdin)")
    ] = None,

    key: Annotated[
        int,
        typer.Option("--key", "-k", help = "Shift key (0-25)")
    ] = 3,

    input_file: Annotated[
        Path | None,
        typer.Option("--input-file", "-i", help = "Input file path")
    ] = None,

    output_file: Annotated[
        Path | None,
        typer.Option("--output-file", "-o", help = "Output file path")
    ] = None,

    quiet: Annotated[
        bool, typer.Option("--quiet", "-q", help = "Suppress all output")
    ] = False,
) -> None:

    try:
        validate_key(key)
        plaintext = read_input(text, input_file)
        cipher = CaesarCipher(key = key)
        decrypted = cipher.decrypt(plaintext)

        if not quiet and not output_file: console.print(f"[bold cyan]Decrypted:[/bold cyan] {decrypted}")
        else: write_output(decrypted, output_file, quiet)

    except (ValueError, OSError) as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1) from None
        
@app.command()
def crack(
    text: Annotated[
        str | None,
        typer.Argument(help = "Text to crack (or use --input-file or stdin)")
    ] = None,
    input_file: Annotated[
        Path | None,
        typer.Option("--input-file", "-i", help = "Input file path")
    ] = None,
    top: Annotated[
        int,
        typer.Option("--top", "-t", help = "Show top N candidates")
    ] = 5,
    show_all: Annotated[
        bool,
        typer.Option("--all", "-a", help = "Show all 26 possible shifts")
    ] = False
) -> None:
    try:
        ciphertext = read_input(text, input_file)
        candidates = CaesarCipher.crack(ciphertext)
        analyzer = FrequencyAnalyzer()
        ranked = analyzer.rank_candidates(candidates)

        table = Table(title = "Caesar Cipher Brute Force Results")
        table.add_column("Rank", justify = "right")
        table.add_column("Shift", justify = "right")
        table.add_column("Score", justify = "right")
        table.add_column("Decrypted Text", style = "green")

        display_count = len(ranked) if show_all else min(top, len(ranked))

        for rank, (shift, text_result, score) in enumerate(ranked[:display_count], 1):
            table.add_row(
                str(rank),
                str(shift),
                f"{score}",
                text_result[: 80]
            )

        console.print(table)
        console.print(
            f"\n[bold]Best match (Shift {ranked[0][0]}):[/bold] {ranked[0][1]}" 
        )

    except (ValueError, OSError) as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1) from None

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        interactive_mode()

if __name__ == "__main__":
    app()

