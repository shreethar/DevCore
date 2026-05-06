import os
import sys

from rich.console import Console
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML

from shell import get_cwd
from router import route

console = Console()

HISTORY_FILE = os.path.expanduser("~/.devcore_history")


def get_prompt_text() -> HTML:
    """Build the prompt string shown on each line."""
    cwd = get_cwd()

    # Replace home directory with ~ for brevity
    home = os.path.expanduser("~")
    if cwd.startswith(home):
        cwd = "~" + cwd[len(home):]

    return HTML(f"<cyan><b>devcore</b></cyan> <gray>{cwd}</gray> <cyan>❯</cyan> ")


def print_banner() -> None:
    console.print()
    console.print("[bold cyan]  DevCore[/bold cyan] [dim]v0.1[/dim]")
    console.print("[dim]  Shell commands run directly. Prefix with [/dim][bold]/[/bold][dim] to talk to AI.[/dim]")
    console.print("[dim]  /clear to reset conversation · exit to quit[/dim]")
    console.print()


def main() -> None:
    print_banner()

    session = PromptSession(
        history=FileHistory(HISTORY_FILE),
        style=Style.from_dict({
            "": "#ffffff",
        }),
        mouse_support=False,
    )

    history = []  # Claude conversation history — persists across turns in a session

    while True:
        try:
            user_input = session.prompt(get_prompt_text())
        except KeyboardInterrupt:
            # Ctrl+C clears the current line, doesn't exit
            print()
            continue
        except EOFError:
            # Ctrl+D exits cleanly
            console.print("\n[dim]Goodbye.[/dim]\n")
            sys.exit(0)

        cmd = user_input.strip()

        # --- Built-in commands ---
        if cmd in ("exit", "quit"):
            console.print("[dim]Goodbye.[/dim]\n")
            sys.exit(0)

        if cmd == "/clear":
            history.clear()
            console.print("[dim]Conversation cleared.[/dim]")
            continue

        if cmd == "/history":
            if not history:
                console.print("[dim]No conversation history yet.[/dim]")
            else:
                for i, msg in enumerate(history):
                    role = "You" if msg["role"] == "user" else "DevCore"
                    # Trim long messages for display
                    content = msg["content"][:120] + "..." if len(msg["content"]) > 120 else msg["content"]
                    console.print(f"[dim]{i+1}. [{role}] {content}[/dim]")
            continue

        # --- Route everything else ---
        route(cmd, history)


if __name__ == "__main__":
    main()