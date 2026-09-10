"""Radar CLI command implementation."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import List, Optional

from core.inspector import RepoInspector, RepoStatus
from core.scanner import WorkspaceScanner


def format_radar_table(statuses: List[RepoStatus]) -> str:
    if not statuses:
        return "No repositories discovered in workspace."

    lines = []
    lines.append("==========================================================================================")
    lines.append("                                📡 WORKSPACE RADAR                                        ")
    lines.append("==========================================================================================")
    header = f"{'Repository':<22} {'VCS':<7} {'Branch':<15} {'Status':<14} {'Unpushed':<10} {'Last Commit'}"
    lines.append(header)
    lines.append("-" * 90)

    for s in statuses:
        status_str = f"⚡ {s.dirty_count} dirty" if s.is_dirty else "✔ Clean"
        unpushed_str = f"↑ {s.unpushed_count}" if s.unpushed_count > 0 else "Synced"
        commit_snippet = f"\"{s.last_commit_msg[:24]}\"" if s.last_commit_msg else "-"
        lines.append(f"{s.name:<22} {s.vcs_type:<7} {s.branch:<15} {status_str:<14} {unpushed_str:<10} {commit_snippet}")

    lines.append("==========================================================================================")
    return "\n".join(lines)


def run_radar(root_path: Path) -> int:
    scanner = WorkspaceScanner(root_path)
    repos = scanner.scan()
    statuses = [RepoInspector(r.path).inspect() for r in repos]
    print(format_radar_table(statuses))
    return 0
