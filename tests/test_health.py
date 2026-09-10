"""Hermetic unit tests for WorkstationHealthScorer."""

from pathlib import Path
import unittest

from core.health import WorkstationHealthScorer
from core.inspector import RepoStatus


class TestHealth(unittest.TestCase):

    def test_all_clean_scores_100(self):
        statuses = [
            RepoStatus(name="r1", path=Path("/tmp/1"), vcs_type="git", is_dirty=False, unpushed_count=0),
            RepoStatus(name="r2", path=Path("/tmp/2"), vcs_type="git", is_dirty=False, unpushed_count=0),
        ]
        report = WorkstationHealthScorer.score(statuses)
        self.assertEqual(report.score, 100)
        self.assertEqual(report.grade, "EXCELLENT")
        self.assertEqual(report.dirty_repos, 0)

    def test_dirty_and_unpushed_deductions(self):
        statuses = [
            RepoStatus(name="r1", path=Path("/tmp/1"), vcs_type="git", is_dirty=True, dirty_count=3, unpushed_count=2),
        ]
        report = WorkstationHealthScorer.score(statuses)
        self.assertLess(report.score, 100)
        self.assertEqual(report.dirty_repos, 1)
        self.assertGreater(len(report.recommendations), 0)


if __name__ == "__main__":
    unittest.main()
