"""Codex runner."""

import json

from ..instructions import HEADLESS
from ..model import Outcome
from .cli import run


class Codex:
    def run(self, task):
        """Run the task with `codex exec`, the prompt on stdin and the headless instructions as developer instructions."""
        args = [
            "exec",
            "--config", f"developer_instructions={json.dumps(HEADLESS)}",
            "--skip-git-repo-check",
            "--ephemeral",
            "--color", "never",
        ]
        if task.yolo:
            args.append("--dangerously-bypass-approvals-and-sandbox")
        else:
            args += ["--sandbox", "workspace-write", "--config", 'approval_policy="never"']
        if task.model:
            args += ["--model", task.model]
        if task.effort:
            # Codex doesn't check the value: an unsupported one fails only when the API rejects it.
            args += ["--config", f"model_reasoning_effort={json.dumps(task.effort)}"]
        args.append("-")
        proc = run("codex", *args, input=task.prompt)
        return Outcome(proc.stdout, proc.returncode)
