"""Hermetic unit tests for Keel Radar CLI."""

import io
from pathlib import Path
import unittest
from unittest.mock import patch

from cli.radar import format_radar_table, run_radar
from core.inspector import RepoStatus


class TestRadarCLI(unittest.TestCase):

    def test_format_radar_table(self):
        statuses = [
            RepoStatus(name="proj1", path=Path("/tmp/p1"), vcs_type="git", branch="main", is_dirty=False),
            RepoStatus(name="proj2", path=Path("/tmp/p2"), vcs_type="git", branch="feat", is_dirty=True, dirty_count=3, unpushed_count=1),
        ]
        out = format_radar_table(statuses)
        self.assertIn("proj1", out)
        self.assertIn("Clean", out)
        self.assertIn("proj2", out)
        self.assertIn("3 dirty", out)
        self.assertIn("↑ 1", out)

    def test_empty_radar_table(self):
        out = format_radar_table([])
        self.assertIn("No repositories discovered", out)


if __name__ == "__main__":
    unittest.main()
