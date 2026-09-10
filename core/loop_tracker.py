"""Autonomous Ralph/Autoloop Repository Detector and Telemetry Parser."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Any, Dict, List, Optional


@dataclass
class LoopProject:
    name: str
    path: Path
    total_runs: int = 0
    latest_run_num: int = 0
    latest_run_title: str = ""
    latest_run_date: str = ""
    total_tasks: int = 0
    completed_tasks: int = 0
    active_phase: str = ""
    is_active: bool = True

    @property
    def completion_pct(self) -> float:
        return (self.completed_tasks / self.total_tasks * 100.0) if self.total_tasks > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "path": str(self.path),
            "total_runs": self.total_runs,
            "latest_run": self.latest_run_num,
            "latest_title": self.latest_run_title,
            "completion_pct": round(self.completion_pct, 1),
            "completed_tasks": self.completed_tasks,
            "total_tasks": self.total_tasks,
            "active_phase": self.active_phase,
            "is_active": self.is_active,
        }


class LoopTracker:
    """Discovers and parses Autoloop projects."""

    @staticmethod
    def is_loop_project(repo_path: Path) -> bool:
        return (repo_path / "AGENT_LOG.md").exists() and (repo_path / "ROADMAP.md").exists()

    @classmethod
    def parse_project(cls, repo_path: Path) -> Optional[LoopProject]:
        if not cls.is_loop_project(repo_path):
            return None

        name = repo_path.name
        log_file = repo_path / "AGENT_LOG.md"
        roadmap_file = repo_path / "ROADMAP.md"

        # 1. Parse AGENT_LOG.md
        log_content = log_file.read_text(encoding="utf-8")
        runs = [int(x) for x in re.findall(r"\[Run (\d+)\]", log_content)]
        total_runs = len(runs)
        latest_run = runs[-1] if runs else 0

        latest_title = ""
        latest_date = ""
        latest_match = re.search(r"##\s+\[Run\s+\d+\]\s*[—–-]\s*([^\n]+)", log_content)
        if latest_match:
            latest_title = latest_match.group(1).strip()
            date_m = re.search(r"(\d{4}-\d{2}-\d{2})", latest_title)
            if date_m:
                latest_date = date_m.group(1)

        # 2. Parse ROADMAP.md
        roadmap_content = roadmap_file.read_text(encoding="utf-8")
        task_matches = re.findall(r"^-\s+\[( |x|X|TODO|IN PROGRESS|DONE)\]", roadmap_content, re.MULTILINE)
        total_tasks = len(task_matches)
        completed_tasks = sum(1 for st in task_matches if st in ("x", "X", "DONE"))
        is_active = any(st in (" ", "TODO", "IN PROGRESS") for st in task_matches)

        active_phase = ""
        phase_m = re.search(r"Active Phase\*\*:\s*([^\n]+)", roadmap_content)
        if phase_m:
            active_phase = phase_m.group(1).strip()

        return LoopProject(
            name=name,
            path=repo_path,
            total_runs=total_runs,
            latest_run_num=latest_run,
            latest_run_title=latest_title,
            latest_run_date=latest_date,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            active_phase=active_phase,
            is_active=is_active,
        )
