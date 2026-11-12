"""Antigravity runner."""

import json

from ..instructions import HEADLESS
from ..model import Outcome
from .cli import run

# Sandboxed commands are allowed, as Codex's workspace-write sandbox allows them; without the rule,
# headless mode auto-denies them.
WORKSPACE_SETTINGS = {"permissions": {"allow": ["command(*)"]}}


class Antigravity:
    NAME = "Antigravity"

    def run(self, task):
        """Run the task with `agy --print`"""
        # agy has no system-prompt channel and doesn't read the prompt from stdin.
        args = [f"--print={HEADLESS}\n\n{task.prompt}"]
        if task.yolo:
            args.append("--dangerously-skip-permissions")
        else:
            args += ["--mode", "accept-edits", "--sandbox", "--settings", json.dumps(WORKSPACE_SETTINGS)]
        if task.model:
            args += ["--model", task.model]
        if task.effort:
            args += ["--effort", task.effort]
        proc = run("agy", *args)
        # When a tool is auto-denied, agy explains on stderr, prints nothing and still exits 0.
        code = proc.returncode or (0 if proc.stdout.strip() else 1)
        return Outcome(proc.stdout, code)
