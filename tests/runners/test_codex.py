"""Invocation of the Codex CLI for a task."""

import json
import subprocess
import tomllib
import unittest
from unittest import mock

from run_agent.instructions import HEADLESS
from run_agent.model import Effort, Task
from run_agent.runners.codex import Codex


def invoke(task):
    """Run the task; return the CLI's args and its stdin."""
    with mock.patch("run_agent.runners.codex.run", return_value=subprocess.CompletedProcess([], 0, "")) as cli:
        Codex().run(task)
    (name, *args), kwargs = cli.call_args
    assert name == "codex"
    return args, kwargs["input"]


class InvokeTest(unittest.TestCase):
    def test_run(self):
        self.assertEqual(invoke(Task("say hello")), ([
            "exec",
            "--config", f"developer_instructions={json.dumps(HEADLESS)}",
            "--skip-git-repo-check",
            "--ephemeral",
            "--color", "never",
            "--sandbox", "workspace-write",
            "--config", 'approval_policy="never"',
            "-",
        ], "say hello"))

    def test_instructions(self):
        args, _ = invoke(Task("say hello"))
        config = args[args.index("--config") + 1]

        self.assertNotIn("\n", config)
        self.assertEqual(tomllib.loads(config), {"developer_instructions": HEADLESS})

    def test_yolo(self):
        args, _ = invoke(Task("say hello", yolo=True))

        self.assertIn("--dangerously-bypass-approvals-and-sandbox", args)
        self.assertNotIn("--sandbox", args)
        self.assertNotIn('approval_policy="never"', args)

    def test_model(self):
        args, _ = invoke(Task("say hello", model="gpt-5-luna"))

        self.assertEqual(args[-3:], ["--model", "gpt-5-luna", "-"])

    def test_effort(self):
        args, _ = invoke(Task("say hello", effort=Effort.XHIGH))

        self.assertEqual(args[-3:], ["--config", 'model_reasoning_effort="xhigh"', "-"])


if __name__ == "__main__":
    unittest.main()
