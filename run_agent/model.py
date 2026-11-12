"""The model shared by the app and runners: a task and its outcome."""

from dataclasses import dataclass
from enum import StrEnum


class Effort(StrEnum):
    """How hard the model reasons: the levels every agent supports."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    XHIGH = "xhigh"
    MAX = "max"


@dataclass
class Task:
    """What to run."""

    prompt: str  # the user's task, passed verbatim
    model: str | None = None  # None = the agent's default
    effort: Effort | None = None  # None = the agent's default
    yolo: bool = False  # True = no permission checks or sandbox; else scoped to the working directory


@dataclass
class Outcome:
    """What the run of a task returned."""

    output: str  # the agent's final answer, as printed
    code: int  # the run's exit code: the CLI's, unless its runner detects a failure the CLI doesn't report
