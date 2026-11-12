"""Agent runners, one per agent CLI.

Each has a `NAME` and a `run(task)` that runs a `Task` headless and returns an `Outcome`.
`RUNNERS` maps each CLI name, as given on the command line, to its runner.
"""

from .agy import Antigravity
from .claude import Claude
from .codex import Codex

RUNNERS = {"claude": Claude(), "codex": Codex(), "agy": Antigravity()}

__all__ = ["RUNNERS"]
