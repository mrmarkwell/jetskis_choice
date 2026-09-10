"""Hermetic smoke test for Keel CLI and package initialization."""

import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cli.main import create_parser, main
from core.version import __app_name__, __version__


class TestSmoke(unittest.TestCase):

    def test_version_metadata(self):
        self.assertEqual(__app_name__, "keel")
        self.assertEqual(__version__, "0.1.0")

    def test_cli_help(self):
        parser = create_parser()
        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            code = main([])
            self.assertEqual(code, 0)
            self.assertIn("keel", mock_out.getvalue())


if __name__ == "__main__":
    unittest.main()
