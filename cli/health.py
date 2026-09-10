"""Health CLI command implementation."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import List

from core.health import HealthReport, WorkstationHealthScorer
from core.inspector import RepoInspector
from core.scanner import WorkspaceScanner


def format_health_report(report: HealthReport) -> str:
    lines = []
    lines.append("======================================================================")
    lines.append("                🩺 WORKSTATION DEVELOPER HEALTH SCORE                  ")
    lines.append("======================================================================")
    lines.append(f"Health Score:        {report.score}/100 [{report.grade}]")
    lines.append(f"Total Repositories:  {report.total_repos}")
    lines.append(f"Clean Repositories:  {report.clean_repos}/{report.total_repos}")
    lines.append(f"Unpushed Commits:    {report.total_unpushed_commits}")
    lines.append("----------------------------------------------------------------------")
    lines.append("Recommendations:")
    for rec in report.recommendations:
        lines.append(f"  • {rec}")
    lines.append("======================================================================")
    return "\n".join(lines)


def run_health(root_path: Path, json_output: bool = False) -> int:
    scanner = WorkspaceScanner(root_path)
    repos = scanner.scan()
    statuses = [RepoInspector(r.path).inspect() for r in repos]
    report = WorkstationHealthScorer.score(statuses)
    if json_output:
        import json
        payload = {
            "score": report.score,
            "grade": report.grade,
            "total_repos": report.total_repos,
            "clean_repos": report.clean_repos,
            "dirty_repos": report.dirty_repos,
            "unpushed_commits": report.total_unpushed_commits,
            "recommendations": report.recommendations,
        }
        print(json.dumps(payload, indent=2))
    else:
        print(format_health_report(report))
    return 0
