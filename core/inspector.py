"""Repository Inspector for extracting VCS health and branch status."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Any, Dict, Optional


@dataclass
class RepoStatus:
    name: str
    path: Path
    vcs_type: str
    branch: str = "main"
    is_dirty: bool = False
    dirty_count: int = 0
    unpushed_count: int = 0
    last_commit_msg: str = ""
    last_commit_date: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "path": str(self.path),
            "vcs_type": self.vcs_type,
            "branch": self.branch,
            "is_dirty": self.is_dirty,
            "dirty_count": self.dirty_count,
            "unpushed_count": self.unpushed_count,
            "last_commit_msg": self.last_commit_msg,
            "last_commit_date": self.last_commit_date,
        }


class RepoInspector:
    """Extracts git status, unpushed commits, and branch metadata."""

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path.resolve()

    def _run_git(self, args: list[str]) -> str:
        try:
            res = subprocess.run(
                ["git"] + args,
                cwd=str(self.repo_path),
                capture_output=True,
                text=True,
                check=False,
            )
            return res.stdout.strip() if res.returncode == 0 else ""
        except Exception:
            return ""

    def inspect(self) -> RepoStatus:
        name = self.repo_path.name
        git_dir = self.repo_path / ".git"

        if not git_dir.exists():
            # Piper CitC workspace fallback
            return RepoStatus(
                name=name,
                path=self.repo_path,
                vcs_type="piper" if "/google/src/cloud/" in str(self.repo_path) else "local",
                branch="citc",
            )

        # 1. Branch
        branch = self._run_git(["rev-parse", "--abbrev-ref", "HEAD"]) or "HEAD"

        # 2. Status & dirty files
        porcelain = self._run_git(["status", "--porcelain"])
        dirty_lines = [l for l in porcelain.split("\n") if l.strip()]
        dirty_count = len(dirty_lines)
        is_dirty = dirty_count > 0

        # 3. Unpushed commits
        unpushed_str = self._run_git(["log", "@{u}..HEAD", "--oneline"])
        unpushed_count = len([l for l in unpushed_str.split("\n") if l.strip()]) if unpushed_str else 0

        # 4. Last commit
        last_commit_msg = self._run_git(["log", "-1", "--pretty=format:%s"])
        last_commit_date = self._run_git(["log", "-1", "--pretty=format:%cr"])

        return RepoStatus(
            name=name,
            path=self.repo_path,
            vcs_type="git",
            branch=branch,
            is_dirty=is_dirty,
            dirty_count=dirty_count,
            unpushed_count=unpushed_count,
            last_commit_msg=last_commit_msg,
            last_commit_date=last_commit_date,
        )
