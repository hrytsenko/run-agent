"""Invocation of the app."""

import contextlib
import io
import sys
import unittest
from unittest import mock

from run_agent import app
from run_agent.model import Effort, Outcome, Task


class Runner:
    """A runner that records its task and returns a fixed outcome, or raises an error."""

    def __init__(self, outcome=None, error=None):
        self.outcome, self.error, self.task = outcome, error, None

    def run(self, task):
        self.task = task
        if self.error:
            raise self.error
        return self.outcome


def run(*args, runner=None, stdin=""):
    """Run the app with args. Return its exit code, stdout and stderr."""
    stdout, stderr = io.TextIOWrapper(io.BytesIO(), encoding="utf-8", newline=""), io.StringIO()
    with (
        mock.patch.object(sys, "argv", ["run-agent", *args]),
        mock.patch.object(sys, "stdin", io.TextIOWrapper(io.BytesIO(stdin.encode()), encoding="utf-8")),
        mock.patch.dict("run_agent.app.RUNNERS", {"claude": runner}),
        contextlib.redirect_stdout(stdout),
        contextlib.redirect_stderr(stderr),
    ):
        try:
            app.main()
        except SystemExit as e:
            code = e.code
    stdout.flush()
    return code, stdout.buffer.getvalue().decode("utf-8"), stderr.getvalue()


class AppTest(unittest.TestCase):
    def test_regular_run(self):
        runner = Runner(Outcome("Done ✓\n", 3))

        self.assertEqual(run("claude", "say hello", runner=runner), (3, "Done ✓\n", ""))
        self.assertEqual(runner.task, Task("say hello"))

    def test_prompt_from_stdin(self):
        runner = Runner(Outcome("", 0))
        run("claude", "-", runner=runner, stdin="say hello\n")

        self.assertEqual(runner.task, Task("say hello\n"))

    def test_options(self):
        runner = Runner(Outcome("", 0))
        run("claude", "--model", "haiku", "--effort", "max", "--yolo", "say hello", runner=runner)

        self.assertEqual(runner.task, Task("say hello", model="haiku", effort=Effort.MAX, yolo=True))

    def test_empty_prompt(self):
        runner = Runner(Outcome("", 0))
        code, _, stderr = run("claude", "-", runner=runner, stdin="  \n")

        self.assertEqual(code, 2)
        self.assertIn("the prompt is empty", stderr)
        self.assertIsNone(runner.task)

    def test_unsupported_effort(self):
        runner = Runner(Outcome("", 0))
        code, _, stderr = run("claude", "--effort", "minimal", "say hello", runner=runner)

        self.assertEqual(code, 2)
        self.assertIn("invalid Effort value: 'minimal'", stderr)
        self.assertIsNone(runner.task)

    def test_agent_not_found(self):
        code, stdout, stderr = run("claude", "say hello", runner=Runner(error=RuntimeError("'claude' not found")))

        self.assertEqual((code, stdout, stderr), (1, "", "run-agent: 'claude' not found\n"))


if __name__ == "__main__":
    unittest.main()
