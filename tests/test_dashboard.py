"""Hermetic unit tests for Keel Dashboard."""

from pathlib import Path
import unittest

from cli.dashboard import render_dashboard


class TestDashboard(unittest.TestCase):

    def test_render_dashboard(self):
        out = render_dashboard(Path("."))
        self.assertIn("KEEL", out)
        self.assertIn("Workstation Health", out)
        self.assertIn("WORKSTATION RADAR", out)


if __name__ == "__main__":
    unittest.main()
