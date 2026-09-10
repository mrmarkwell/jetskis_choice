"""Hermetic unit tests for WorkspaceScanner."""

from pathlib import Path
import tempfile
import unittest

from core.scanner import DiscoveredRepo, WorkspaceScanner


class TestWorkspaceScanner(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp_dir.name)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_scan_empty_directory(self):
        scanner = WorkspaceScanner(self.root)
        self.assertEqual(scanner.scan(), [])

    def test_scan_finds_git_repos(self):
        # Create mock git repos
        repo1 = self.root / "proj_alpha"
        (repo1 / ".git").mkdir(parents=True)

        repo2 = self.root / "subfolder" / "proj_beta"
        (repo2 / ".git").mkdir(parents=True)

        # Non-repo folder
        (self.root / "ignored_folder").mkdir()

        scanner = WorkspaceScanner(self.root, max_depth=3)
        repos = scanner.scan()

        self.assertEqual(len(repos), 2)
        names = {r.name for r in repos}
        self.assertEqual(names, {"proj_alpha", "proj_beta"})
        for r in repos:
            self.assertEqual(r.vcs_type, "git")

    def test_scan_root_itself_is_repo(self):
        (self.root / ".git").mkdir()
        scanner = WorkspaceScanner(self.root)
        repos = scanner.scan()
        self.assertEqual(len(repos), 1)
        self.assertEqual(repos[0].path, self.root)


if __name__ == "__main__":
    unittest.main()
