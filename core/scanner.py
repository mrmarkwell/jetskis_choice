"""Workspace Scanner for discovering local Git and Piper repositories."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import List, Optional, Set


@dataclass
class DiscoveredRepo:
    name: str
    path: Path
    vcs_type: str  # 'git' or 'piper'

    def to_dict(self):
        return {
            "name": self.name,
            "path": str(self.path),
            "vcs_type": self.vcs_type,
        }


class WorkspaceScanner:
    """Recursively scans directories to locate repositories."""

    IGNORED_DIRS: Set[str] = {
        ".git", ".hg", "node_modules", ".venv", "venv",
        "__pycache__", ".cache", "build", "dist", ".gemini"
    }

    def __init__(self, root: Path, max_depth: int = 3):
        self.root = root.resolve()
        self.max_depth = max_depth

    def scan(self) -> List[DiscoveredRepo]:
        repos: List[DiscoveredRepo] = []
        if not self.root.exists():
            return repos

        # If the root itself is a repository
        if (self.root / ".git").exists():
            repos.append(DiscoveredRepo(name=self.root.name, path=self.root, vcs_type="git"))
            # In a git repo root, we usually don't need to descend further unless searching submodules
            return repos

        self._scan_recursive(self.root, current_depth=0, repos=repos)
        # Deduplicate and sort
        repos.sort(key=lambda r: str(r.path))
        return repos

    def _scan_recursive(self, current: Path, current_depth: int, repos: List[DiscoveredRepo]) -> None:
        if current_depth > self.max_depth:
            return

        try:
            entries = list(current.iterdir())
        except (PermissionError, OSError):
            return

        # Check for Git
        git_dir = current / ".git"
        if git_dir.exists():
            repos.append(DiscoveredRepo(name=current.name, path=current, vcs_type="git"))
            return

        # Check for Piper CitC
        if "/google/src/cloud/" in str(current) and (current / "google3").exists():
            repos.append(DiscoveredRepo(name=current.name, path=current, vcs_type="piper"))
            return

        for entry in entries:
            if entry.is_dir() and entry.name not in self.IGNORED_DIRS:
                self._scan_recursive(entry, current_depth + 1, repos)
