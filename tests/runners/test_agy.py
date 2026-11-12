"""Invocation of the Antigravity CLI for a task."""

import json
import subprocess
import unittest
from unittest import mock

from run_agent.instructions import HEADLESS
from run_agent.model import Effort, Task
from run_agent.runners.agy import Antigravity


def invoke(task):
    """Run the task; return the CLI's args."""
    with mock.patch("run_agent.runners.agy.run", return_value=subprocess.CompletedProcess([], 0, "")) as cli:
        Antigravity().run(task)
    (name, *args), kwargs = cli.call_args
    assert name == "agy"
    assert "input" not in kwargs  # agy doesn't read the prompt from stdin
    return args


class InvokeTest(unittest.TestCase):
    def test_run(self):
        self.assertEqual(invoke(Task("fix the tests")), [
            f"--print={HEADLESS}\n\nfix the tests",
            "--mode", "accept-edits",
            "--sandbox",
            "--settings", json.dumps({"permissions": {"allow": ["command(*)"]}}),
        ])

    def test_yolo(self):
        args = invoke(Task("fix the tests", yolo=True))

        self.assertEqual(args[1:], ["--dangerously-skip-permissions"])

    def test_model(self):
        args = invoke(Task("fix the tests", model="gemini-3-flash-medium"))

        self.assertEqual(args[-2:], ["--model", "gemini-3-flash-medium"])

    def test_effort(self):
        args = invoke(Task("fix the tests", effort=Effort.LOW))

        self.assertEqual(args[-2:], ["--effort", "low"])


if __name__ == "__main__":
    unittest.main()
