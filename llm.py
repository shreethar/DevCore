import openai
from rich.console import Console

from config import API_KEY, MODEL, SYSTEM_PROMPT
from context import build_context

console = Console()

# Lazy-init the client so missing API key only errors when you actually use /
_client = None


def _get_client() -> openai.OpenAI:
    global _client
    if _client is None:
        if not API_KEY:
            console.print(
                "\n[bold red]Error:[/bold red] OPENROUTER_API_KEY environment variable is not set.\n"
                "Run: [bold]export OPENROUTER_API_KEY=your_key_here[/bold]\n"
            )
            raise SystemExit(1)
        _client = openai.OpenAI(api_key=API_KEY, base_url="https://openrouter.ai/api/v1")
    return _client


def ask(prompt: str, history: list) -> None:
    """
    Send a prompt to Qwen with fresh context injected into the system prompt.
    Streams the response token by token.
    Updates history in place.
    """
    client = _get_client()

    # Fresh context on every call — captures any cd changes
    context = build_context()
    system_with_context = f"{SYSTEM_PROMPT}\n\n{context}"

    # Append user message to history
    history.append({"role": "user", "content": prompt})

    console.print("\n[bold cyan]◆ DevCore[/bold cyan] ", end="")

    response_text = ""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=history,
            stream=True,
            extra_body={"reasoning": {"enabled": False}}
        )

        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)

    except openai.APIConnectionError:
        console.print("\n[red]Connection error — are you online?[/red]")
        history.pop()  # Don't store failed exchange
        return
    except openai.RateLimitError:
        console.print("\n[red]Rate limit hit — slow down a bit.[/red]")
        history.pop()
        return
    except openai.APIStatusError as e:
        console.print(f"\n[red]API error {e.status_code}:[/red] {e.message}")
        history.pop()
        return

    print("\n")  # Clean newline after streamed response

    # Store the clean response (no context bloat in history)
    history.append({"role": "assistant", "content": response_text})