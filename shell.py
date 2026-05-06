import os
import subprocess

# Track cwd ourselves — subprocess can't affect the parent process's cwd
_cwd = os.getcwd()


def get_cwd() -> str:
    return _cwd


def run_command(command: str) -> None:
    global _cwd
    parts = command.strip().split()

    if not parts:
        return

    # --- Handle `cd` manually ---
    # subprocess runs in a child process, so `cd` there won't affect us.
    # We manage the directory ourselves with os.chdir().
    if parts[0] == "cd":
        if len(parts) == 1:
            target = os.path.expanduser("~")
        elif parts[1] == "-":
            # cd - goes back to previous dir (simplified: just home for now)
            target = os.path.expanduser("~")
        else:
            target = parts[1]

        # Resolve relative or absolute path
        if os.path.isabs(target):
            new_path = os.path.normpath(target)
        else:
            new_path = os.path.normpath(os.path.join(_cwd, target))

        if os.path.isdir(new_path):
            _cwd = new_path
            os.chdir(_cwd)
        else:
            print(f"devcore: cd: {target}: No such file or directory")
        return

    # --- Run everything else ---
    try:
        subprocess.run(
            command,
            shell=True,
            cwd=_cwd,
        )
    except KeyboardInterrupt:
        # Let user Ctrl+C a running command without killing DevCore
        print()
    except Exception as e:
        print(f"devcore: error running command: {e}")