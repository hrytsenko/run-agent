"""Invocation of the Claude Code CLI for a task."""

import subprocess
import unittest
from unittest import mock

from run_agent.instructions import HEADLESS
from run_agent.model import Effort, Task
from run_agent.runners.claude import Claude


def invoke(task):
    """Run the task; return the CLI's args and its stdin."""
    with mock.patch("run_agent.runners.claude.run", return_value=subprocess.CompletedProcess([], 0, "")) as cli:
        Claude().run(task)
    (name, *args), kwargs = cli.call_args
    assert name == "claude"
    return args, kwargs["input"]


class InvokeTest(unittest.TestCase):
    def test_run(self):
        self.assertEqual(invoke(Task("fix the tests")), ([
            "--print",
            "--append-system-prompt", HEADLESS,
            "--no-session-persistence",
            "--permission-prompts", "none",
            "--permission-mode", "auto",
        ], "fix the tests"))

    def test_yolo(self):
        args, _ = invoke(Task("fix the tests", yolo=True))

        self.assertIn("--dangerously-skip-permissions", args)
        self.assertNotIn("--permission-mode", args)

    def test_model(self):
        args, _ = invoke(Task("fix the tests", model="haiku"))

        self.assertEqual(args[-2:], ["--model", "haiku"])

    def test_effort(self):
        args, _ = invoke(Task("fix the tests", effort=Effort.HIGH))

        self.assertEqual(args[-2:], ["--effort", "high"])


if __name__ == "__main__":
    unittest.main()
