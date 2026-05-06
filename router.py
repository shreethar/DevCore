from shell import run_command
from llm import ask


def route(user_input: str, history: list) -> None:
    """
    Single routing decision:
      - Starts with /  →  send to Claude (strip the slash first)
      - Anything else  →  run as shell command
    """
    stripped = user_input.strip()

    if not stripped:
        return

    if stripped.startswith("/"):
        prompt = stripped[1:].strip()
        if not prompt:
            print("devcore: empty prompt — type /your question here")
            return
        ask(prompt, history)
    else:
        run_command(stripped)