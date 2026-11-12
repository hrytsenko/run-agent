"""The app's command line: the task it builds, the output it prints and its exit code."""

import contextlib
import io
import sys
import unittest
from unittest import mock

from run_agent import __version__, app
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
    """Run the app with args, `claude` as runner and stdin; return its exit code, stdout and stderr."""
    # The app reconfigures stdout, which StringIO can't do.
    stdout, stderr = io.TextIOWrapper(io.BytesIO(), encoding="utf-8", newline=""), io.StringIO()
    with (
        mock.patch.object(sys, "argv", ["run-agent", *args]),
        mock.patch.object(sys, "stdin", io.StringIO(stdin)),
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
    def test_version(self):
        code, stdout, _ = run("--version")

        self.assertEqual((code, stdout), (0, f"run-agent {__version__}\n"))

    def test_prints_output_and_exits_with_code(self):
        runner = Runner(Outcome("Done ✓\n", 3))

        self.assertEqual(run("claude", "fix the tests", runner=runner), (3, "Done ✓\n", ""))
        self.assertEqual(runner.task, Task("fix the tests"))

    def test_options(self):
        runner = Runner(Outcome("", 0))
        run("claude", "--model", "haiku", "--effort", "max", "--yolo", "fix the tests", runner=runner)

        self.assertEqual(runner.task, Task("fix the tests", model="haiku", effort=Effort.MAX, yolo=True))

    def test_unsupported_effort(self):
        runner = Runner(Outcome("", 0))
        code, _, stderr = run("claude", "--effort", "minimal", "fix the tests", runner=runner)

        self.assertEqual(code, 2)
        self.assertIn("invalid Effort value: 'minimal'", stderr)
        self.assertIsNone(runner.task)

    def test_prompt_from_stdin(self):
        runner = Runner(Outcome("", 0))
        run("claude", "-", runner=runner, stdin="fix the tests\n")

        self.assertEqual(runner.task, Task("fix the tests\n"))

    def test_empty_prompt(self):
        runner = Runner(Outcome("", 0))
        code, _, stderr = run("claude", "-", runner=runner, stdin="  \n")

        self.assertEqual(code, 2)
        self.assertIn("the prompt is empty", stderr)
        self.assertIsNone(runner.task)

    def test_agent_not_found(self):
        code, stdout, stderr = run("claude", "fix the tests", runner=Runner(error=RuntimeError("'claude' not found")))

        self.assertEqual((code, stdout, stderr), (1, "", "run-agent: 'claude' not found\n"))


if __name__ == "__main__":
    unittest.main()
