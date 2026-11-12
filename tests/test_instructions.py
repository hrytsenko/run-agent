"""The headless instructions shared by the runners."""

import unittest

from run_agent.instructions import HEADLESS


class InstructionsTest(unittest.TestCase):
    def test_safe_for_cmd(self):
        # On Windows, the Codex runner passes them through npm's codex.cmd shim, so cmd.exe sees them.
        self.assertFalse(set(HEADLESS) & set('&|<>^%!"'))


if __name__ == "__main__":
    unittest.main()
