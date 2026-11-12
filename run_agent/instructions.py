"""Generic instructions that steer an agent in headless mode, shared by the runners."""

# Keep as plain text without special characters (& | < > ^ % ! "): on Windows, they pass through cmd.exe via npm's codex.cmd.
HEADLESS = """\
You are running in headless mode: no one is watching this session, and no one can answer questions or approve actions.
Complete the task on your own from start to finish, without asking for confirmation or approval.
When something is ambiguous, make a reasonable choice and note it in your final answer.
End with a final answer that reports what you did and the outcome."""
