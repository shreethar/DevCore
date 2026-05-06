# DevCore v0.1

A terminal-native coding assistant. Shell commands run directly. Prefix with `/` to talk to AI.

---

## Setup

```bash
# 1. Clone / download the devcore/ folder

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Anthropic API key
export OPENROUER_API_KEY=your_key_here

# 4. Run
python main.py
```

---

## Usage

```
devcore ~/projects/myapp ❯ ls
devcore ~/projects/myapp ❯ cd src
devcore ~/projects/myapp/src ❯ /what's in this folder and what does each file do
devcore ~/projects/myapp/src ❯ /which file handles authentication
devcore ~/projects/myapp/src ❯ git status
devcore ~/projects/myapp/src ❯ /clear      ← reset conversation history
devcore ~/projects/myapp/src ❯ exit
```

**Rule:** No `/` = shell command. `/` = Claude.

---

## Built-in commands

| Command     | What it does                        |
|-------------|-------------------------------------|
| `/clear`    | Reset the AI conversation history   |
| `/history`  | Show current conversation summary   |
| `exit`      | Quit DevCore                        |

---

## Roadmap

- **Phase 2** — Codebase indexer (dependency graph, smarter context selection)
- **Phase 3** — Code search (ripgrep integration)
- **Phase 4** — Edit engine (diff preview, apply changes)
- **Later** — `devcore` as a global CLI command