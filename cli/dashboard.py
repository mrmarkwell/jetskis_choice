"""Unified Retro ASCII Ship's Helm Workstation Dashboard for Keel."""

from __future__ import annotations

from pathlib import Path
from typing import List

from cli.loops import format_loops_table
from cli.radar import format_radar_table
from core.health import WorkstationHealthScorer
from core.inspector import RepoInspector
from core.loop_tracker import LoopTracker
from core.scanner import WorkspaceScanner

HELM_BANNER = r"""
        .---.
       /  |  \
  ====(   ⚓   )====   KEEL — JETSKI'S CHOICE WORKSTATION RADAR
       \  |  /
        '---'
"""


def render_dashboard(root_path: Path) -> str:
    scanner = WorkspaceScanner(root_path)
    repos = scanner.scan()

    statuses = [RepoInspector(r.path).inspect() for r in repos]
    projects = [p for p in (LoopTracker.parse_project(r.path) for r in repos) if p is not None]
    health = WorkstationHealthScorer.score(statuses)

    lines = []
    lines.append(HELM_BANNER)
    lines.append(f"  ⚡ Workstation Health: {health.score}/100 [{health.grade}] | {len(repos)} Repos | {len(projects)} Autonomous Loops")
    lines.append("")
    lines.append(format_loops_table(projects))
    lines.append("")
    lines.append(format_radar_table(statuses))
    return "\n".join(lines)


def run_dashboard(root_path: Path) -> int:
    print(render_dashboard(root_path))
    return 0
