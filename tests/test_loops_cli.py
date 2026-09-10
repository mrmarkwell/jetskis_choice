"""Hermetic unit tests for Keel Loops CLI."""

from pathlib import Path
import unittest

from cli.loops import format_loops_table
from core.loop_tracker import LoopProject


class TestLoopsCLI(unittest.TestCase):

    def test_format_loops_table(self):
        projects = [
            LoopProject(name="bible", path=Path("/tmp/b"), total_runs=75, completed_tasks=70, total_tasks=84, active_phase="Phase 3", is_active=True),
            LoopProject(name="autoloop", path=Path("/tmp/a"), total_runs=5, completed_tasks=5, total_tasks=5, active_phase="Phase 0", is_active=False),
        ]
        out = format_loops_table(projects)
        self.assertIn("bible", out)
        self.assertIn("83.3%", out)
        self.assertIn("70/84", out)
        self.assertIn("autoloop", out)
        self.assertIn("100.0%", out)

    def test_empty_loops_table(self):
        out = format_loops_table([])
        self.assertIn("No autonomous Ralph/Autoloop projects discovered", out)


if __name__ == "__main__":
    unittest.main()
