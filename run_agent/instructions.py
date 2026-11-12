"""Generic instructions that steer an agent in headless mode, shared by the runners.

Each runner delivers them through its CLI's own channel, such as an appended system prompt
or a preamble to the prompt; they never replace the agent's own system instructions.
"""

# Keep cmd.exe's special characters (& | < > ^ % !) out: on Windows, the Codex runner passes
# these through npm's codex.cmd shim.
HEADLESS = """\
You are running in headless mode: no one is watching this session, and no one can answer questions or approve actions.
Complete the task on your own from start to finish, without asking for confirmation or approval.
When something is ambiguous, make a reasonable choice and note it in your final answer.
End with a final answer that reports what you did and the outcome."""
