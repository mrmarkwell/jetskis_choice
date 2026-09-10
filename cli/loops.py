"""Loops CLI command implementation."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import List, Optional

from core.loop_tracker import LoopProject, LoopTracker
from core.scanner import WorkspaceScanner


def format_loops_table(projects: List[LoopProject]) -> str:
    if not projects:
        return "No autonomous Ralph/Autoloop projects discovered in workspace."

    lines = []
    lines.append("==========================================================================================")
    lines.append("                           🤖 AUTONOMOUS LOOP RADAR HUB                                   ")
    lines.append("==========================================================================================")
    header = f"{'Project':<20} {'Runs':<7} {'Progress':<12} {'Tasks':<12} {'Active Phase':<24} {'Status'}"
    lines.append(header)
    lines.append("-" * 90)

    for p in projects:
        prog_bar = f"{p.completion_pct:4.1f}%"
        tasks_str = f"{p.completed_tasks}/{p.total_tasks}"
        status_str = "🟢 Active" if p.is_active else "✔ Done"
        phase_str = p.active_phase[:22] if p.active_phase else "-"
        lines.append(f"{p.name:<20} {p.total_runs:<7} {prog_bar:<12} {tasks_str:<12} {phase_str:<24} {status_str}")

    lines.append("==========================================================================================")
    return "\n".join(lines)


def run_loops(root_path: Path) -> int:
    scanner = WorkspaceScanner(root_path)
    repos = scanner.scan()
    projects: List[LoopProject] = []
    for r in repos:
        p = LoopTracker.parse_project(r.path)
        if p:
            projects.append(p)

    print(format_loops_table(projects))
    return 0
