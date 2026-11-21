# Agent guidelines

## Workflow

1. Write code for the Python version in `requires-python`, using its features.
2. Check that the code passes `uv run pre-commit run --all-files` and `uv run python -m unittest`.
3. When a change touches the package, bump the minor version in `run_agent/__init__.py`. Bump once per commit: if the version already differs from the last commit, leave it.

## Decisions

### Shared model

`model.py` holds the types that the app and runners share. It describes a task and its outcome, not how a runner invokes its agent.

### Independent runners

Runners must be independent. When different agents take a prompt or report an outcome the same way, treat it as a coincidence and don't share code between their runners. Generic helpers for running a CLI, as in `runners/cli.py`, are fine to share. Taking the same steps, check then run, is a convenience, not an obligation: a runner may change its steps.

### The user's prompt, plus headless instructions

A run passes the user's prompt to the agent as the task. It keeps the agent's own system instructions and doesn't ask for structured output. `instructions.py` holds generic instructions that tell the agent it runs headless and must complete the work without asking for approvals; each runner delivers them through whatever channel its CLI offers, such as an appended system prompt or a preamble to the prompt.

### Workspace-scoped permissions by default

By default, a run lets the agent edit files and run sandboxed commands in the working directory, and has whatever else would need approval denied rather than waited on. Each runner picks its CLI's closest mode, and a mode must end the run instead of blocking on a prompt. `yolo` lifts every check and sandbox, and only through each CLI's own bypass flag. When a CLI reports a denied run as a success, its runner turns the outcome into a failure.

## Testing

A `test-<agent>.yml` workflow per agent covers the real run: it installs the agent's latest CLI and gives `run-agent` a task with the default permissions. The task runs a script that writes the hash of a random nonce, and the workflow checks it, so the agent must run a command in the workspace: it can't produce the token by itself. The prompt names the exact command, so a failure points at the run, such as an approval, the sandbox or the headless instructions, not at the agent's guesswork.
