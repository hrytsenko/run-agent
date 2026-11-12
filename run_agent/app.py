"""Run a prompt through the Claude Code, Codex or Antigravity (agy) CLI in headless mode.

The agent gets the prompt as its task, with instructions to complete the work without asking for approvals.
It works in the current directory: it may edit files and run sandboxed commands there, and whatever
else would need approval is denied, unless --yolo lifts every check.
The agent's final answer goes to stdout and its progress to stderr; the exit code is the agent's.

Usage:
    run-agent <agent> "<prompt>"                  # run the prompt
    run-agent <agent> - < prompt.md               # read the prompt from stdin
    run-agent <agent> --model <model> "<prompt>"  # pick a model; else the agent's default
    run-agent <agent> --effort high "<prompt>"    # pick a reasoning effort; else the agent's default
"""

import argparse
import sys

from . import __version__
from .model import Effort, Task
from .runners import RUNNERS


def main():
    parser = argparse.ArgumentParser(prog="run-agent", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("agent", choices=RUNNERS, help="the agent to run")
    parser.add_argument("prompt", help="the prompt, or - to read it from stdin")
    parser.add_argument("--model", help="the model to use")
    parser.add_argument("--effort", type=Effort, choices=list(Effort), help="the reasoning effort")
    parser.add_argument("--yolo", action="store_true", help="skip every permission check and sandbox")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args()

    # Windows consoles may default to a legacy codepage that can't print the agent's output.
    sys.stdout.reconfigure(encoding="utf-8")

    prompt = sys.stdin.read() if args.prompt == "-" else args.prompt
    if not prompt.strip():
        parser.error("the prompt is empty")
    task = Task(prompt, model=args.model, effort=args.effort, yolo=args.yolo)

    try:
        outcome = RUNNERS[args.agent].run(task)
    except (RuntimeError, OSError) as e:
        parser.exit(1, f"{parser.prog}: {e}\n")
    except KeyboardInterrupt:
        parser.exit(130)

    sys.stdout.write(outcome.output)
    sys.stdout.flush()
    sys.exit(outcome.code)
