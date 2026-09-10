"""Hermetic unit tests for RepoInspector."""

from pathlib import Path
import subprocess
import tempfile
import unittest

from core.inspector import RepoInspector, RepoStatus


class TestRepoInspector(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp_dir.name)
        # Initialize a real git repo in temp dir
        subprocess.run(["git", "init", "-b", "main"], cwd=str(self.root), capture_output=True, check=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=str(self.root), check=True)
        subprocess.run(["git", "config", "user.name", "Tester"], cwd=str(self.root), check=True)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_inspect_clean_repo(self):
        # Initial commit
        (self.root / "README.md").write_text("# Test\n")
        subprocess.run(["git", "add", "README.md"], cwd=str(self.root), check=True)
        subprocess.run(["git", "commit", "-m", "initial commit"], cwd=str(self.root), check=True)

        inspector = RepoInspector(self.root)
        status = inspector.inspect()

        self.assertEqual(status.name, self.root.name)
        self.assertEqual(status.branch, "main")
        self.assertFalse(status.is_dirty)
        self.assertEqual(status.dirty_count, 0)
        self.assertEqual(status.last_commit_msg, "initial commit")

    def test_inspect_dirty_repo(self):
        # Create uncommitted file
        (self.root / "dirty.txt").write_text("uncommitted")
        inspector = RepoInspector(self.root)
        status = inspector.inspect()

        self.assertTrue(status.is_dirty)
        self.assertEqual(status.dirty_count, 1)


if __name__ == "__main__":
    unittest.main()
