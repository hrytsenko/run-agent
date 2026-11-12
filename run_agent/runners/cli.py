"""Helpers for invoking agent CLIs, shared by the runners."""

import shutil
import subprocess


def run(name, *args, input=None):
    """Run `<name> <args>` with input on stdin; return the CompletedProcess with stdout captured.

    Stderr passes through to the terminal, so the agent's progress and errors show while it works.
    Without input, stdin is closed so the CLI can't wait for it.
    """
    path = shutil.which(name)  # Windows: also finds .exe/.cmd shims, e.g. npm's codex.cmd
    if not path:
        raise RuntimeError(f"'{name}' not found")
    # Windows: args go straight to CreateProcess, so Git Bash can't rewrite them into paths.
    stdin = {"input": input} if input is not None else {"stdin": subprocess.DEVNULL}
    return subprocess.run(
        [path, *args],
        stdout=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", check=False, **stdin,
    )
