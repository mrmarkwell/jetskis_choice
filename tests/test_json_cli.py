"""Hermetic unit tests for Keel JSON CLI output."""

import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from cli.main import main


class TestJsonCLI(unittest.TestCase):

    def test_dashboard_json_output(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            code = main(["dashboard", "--root", ".", "--json"])
            self.assertEqual(code, 0)
            data = json.loads(mock_out.getvalue())
            self.assertIn("health", data)
            self.assertIn("loops", data)
            self.assertIn("repos", data)

    def test_radar_json_output(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            code = main(["radar", "--root", ".", "--json"])
            self.assertEqual(code, 0)
            data = json.loads(mock_out.getvalue())
            self.assertIsInstance(data, list)

    def test_loops_json_output(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            code = main(["loops", "--root", ".", "--json"])
            self.assertEqual(code, 0)
            data = json.loads(mock_out.getvalue())
            self.assertIsInstance(data, list)

    def test_health_json_output(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            code = main(["health", "--root", ".", "--json"])
            self.assertEqual(code, 0)
            data = json.loads(mock_out.getvalue())
            self.assertIn("score", data)
            self.assertIn("grade", data)


if __name__ == "__main__":
    unittest.main()
