"""Hermetic unit tests for LoopTracker."""

from pathlib import Path
import tempfile
import unittest

from core.loop_tracker import LoopTracker


class TestLoopTracker(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp_dir.name)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_non_loop_project(self):
        self.assertFalse(LoopTracker.is_loop_project(self.root))
        self.assertIsNone(LoopTracker.parse_project(self.root))

    def test_parse_loop_project(self):
        (self.root / "AGENT_LOG.md").write_text(
            "# Log\n\n## [Run 001] — 2026-09-08 Initial\n- Action 1\n\n## [Run 002] — 2026-09-09 Second\n- Action 2\n"
        )
        (self.root / "ROADMAP.md").write_text(
            "- **Active Phase**: Phase 1\n\n- [x] **Task 1.1**: Done\n- [ ] **Task 1.2**: Todo\n"
        )
        self.assertTrue(LoopTracker.is_loop_project(self.root))
        proj = LoopTracker.parse_project(self.root)
        self.assertIsNotNone(proj)
        self.assertEqual(proj.total_runs, 2)
        self.assertEqual(proj.latest_run_num, 2)
        self.assertEqual(proj.total_tasks, 2)
        self.assertEqual(proj.completed_tasks, 1)
        self.assertEqual(proj.completion_pct, 50.0)
        self.assertTrue(proj.is_active)


if __name__ == "__main__":
    unittest.main()
