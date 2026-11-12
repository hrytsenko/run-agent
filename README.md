# run-agent

Execute a task via a locally installed agent CLI in headless mode: Claude Code, Codex or Antigravity.

The prompt goes to the agent as its task, with instructions that it runs headless and must finish without asking for approvals; the agent keeps its own system prompt. Each CLI must be installed and logged in.

## Install

With [uv](https://docs.astral.sh/uv/):

```sh
uv tool install git+https://github.com/hrytsenko/run-agent  # install
uv tool upgrade run-agent                                   # update
uv tool uninstall run-agent                                 # remove
```

## Run

```sh
run-agent <agent> "<prompt>"                 # run the prompt
run-agent <agent> - < prompt.md              # read the prompt from stdin
run-agent <agent> --model <model> "<prompt>" # pick a model
run-agent <agent> --effort high "<prompt>"   # pick a reasoning effort
run-agent <agent> --yolo "<prompt>"          # skip every permission check and sandbox
run-agent --version
```

`<agent>` is `claude`, `codex` or `agy`. The agent's final answer goes to stdout and its progress to stderr. The exit code is the agent's.

## Permissions

The agent works in the current directory: it may edit files and run sandboxed commands there, and anything else that needs approval is denied. `--yolo` lifts every check and sandbox, so the agent can do anything your account can.

## Develop

```sh
uv run ruff check           # lint
uv run python -m unittest   # test
uv run python -m run_agent  # run
```
