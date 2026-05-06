import os
from shell import get_cwd

# Folders that add noise and should be skipped
IGNORED_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    "dist", "build", ".next", ".cache", ".idea", ".vscode",
    "coverage", ".mypy_cache", ".pytest_cache",
}

IGNORED_FILES = {
    ".DS_Store", "Thumbs.db", ".env",
}


def _build_tree(path: str, prefix: str = "", depth: int = 0, max_depth: int = 3) -> str:
    """Recursively build a tree string for a directory."""
    if depth >= max_depth:
        return f"{prefix}...\n"

    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return f"{prefix}[permission denied]\n"

    # Filter noise
    entries = [
        e for e in entries
        if e not in IGNORED_FILES
        and not (os.path.isdir(os.path.join(path, e)) and e in IGNORED_DIRS)
    ]

    tree = ""
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        child_prefix = prefix + ("    " if is_last else "│   ")
        full_path = os.path.join(path, entry)

        if os.path.isdir(full_path):
            tree += f"{prefix}{connector}{entry}/\n"
            tree += _build_tree(full_path, child_prefix, depth + 1, max_depth)
        else:
            # Show line count for text files, size for binaries
            meta = _file_meta(full_path)
            tree += f"{prefix}{connector}{entry}{meta}\n"

    return tree


def _file_meta(path: str) -> str:
    """Return a short metadata string for a file."""
    try:
        size = os.path.getsize(path)
        # Try reading as text to get line count
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = sum(1 for _ in f)
        return f"  [{lines} lines]"
    except Exception:
        return ""


def build_context() -> str:
    """
    Build the context string that gets injected into Claude's system prompt.
    Includes cwd and a file tree. No file contents — that comes later in Phase 2.
    """
    cwd = get_cwd()
    tree = _build_tree(cwd)

    context = f"## Current working directory\n{cwd}\n\n"
    context += f"## File structure\n```\n{tree}```\n"

    return context