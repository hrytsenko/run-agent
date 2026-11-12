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

`<agent>` is `claude`, `codex` or `agy`. The agent's final answer goes to stdout and its progress to stderr. The exit code is the agent's.

### Run a task

```sh
run-agent <agent> --model <model> --effort <effort> "<prompt>"
```

`--model` and `--effort` are optional and default to the agent's own; `<effort>` is `low`, `medium`, `high`, `xhigh` or `max`.

The agent works in the current directory: it may edit files and run sandboxed commands there, and anything else that needs approval is denied.

### Run a task from a file

```sh
run-agent <agent> - < TASK.md
```

With `-`, the prompt comes from stdin. Keep a recurring task, or one too long to quote on the command line, in a file and run it whenever you need it.

### Run without restrictions

```sh
run-agent <agent> --yolo "<prompt>"
```

`--yolo` lifts every permission check and sandbox, so the agent can do anything your account can.

## Develop

```sh
uv run ruff check           # lint
uv run python -m unittest   # test
uv run python -m run_agent  # run
```
