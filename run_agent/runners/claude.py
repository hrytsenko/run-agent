"""Claude Code runner."""

from ..instructions import HEADLESS
from ..model import Outcome
from .cli import run


class Claude:
    def run(self, task):
        """Run the task with `claude --print`"""
        args = [
            "--print",
            "--append-system-prompt", HEADLESS,
            "--no-session-persistence",
            "--permission-prompts", "none",
        ]
        if task.yolo:
            args.append("--dangerously-skip-permissions")
        else:
            args += ["--permission-mode", "auto"]
        if task.model:
            args += ["--model", task.model]
        if task.effort:
            args += ["--effort", task.effort]
        proc = run("claude", *args, input=task.prompt)
        return Outcome(proc.stdout, proc.returncode)
