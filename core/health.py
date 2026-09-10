"""Workstation Developer Health Scorer & Hygiene Auditor."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

from core.inspector import RepoStatus


@dataclass
class HealthReport:
    score: int  # 0 to 100
    grade: str  # EXCELLENT, GOOD, FAIR, NEEDS ATTENTION
    total_repos: int
    clean_repos: int
    dirty_repos: int
    total_unpushed_commits: int
    recommendations: List[str] = field(default_factory=list)


class WorkstationHealthScorer:
    """Calculates developer hygiene score from repo statuses."""

    @classmethod
    def score(cls, statuses: List[RepoStatus]) -> HealthReport:
        if not statuses:
            return HealthReport(
                score=100,
                grade="EXCELLENT",
                total_repos=0,
                clean_repos=0,
                dirty_repos=0,
                total_unpushed_commits=0,
                recommendations=["No repositories discovered. Workspace is clear."],
            )

        total = len(statuses)
        dirty_count = sum(1 for s in statuses if s.is_dirty)
        clean_count = total - dirty_count
        unpushed_total = sum(s.unpushed_count for s in statuses)

        # Base score 100
        score = 100
        recs: List[str] = []

        # Deduct for dirty repos (up to 30 points)
        if dirty_count > 0:
            deduction = min(30, int((dirty_count / total) * 30))
            score -= deduction
            for s in statuses:
                if s.is_dirty:
                    recs.append(f"Repository '{s.name}' has {s.dirty_count} uncommitted file(s). Commit or stash them.")

        # Deduct for unpushed commits (up to 30 points)
        if unpushed_total > 0:
            deduction = min(30, unpushed_total * 5)
            score -= deduction
            for s in statuses:
                if s.unpushed_count > 0:
                    recs.append(f"Repository '{s.name}' has {s.unpushed_count} unpushed commit(s). Run 'git push'.")

        score = max(0, min(100, score))

        if score >= 90:
            grade = "EXCELLENT"
        elif score >= 75:
            grade = "GOOD"
        elif score >= 60:
            grade = "FAIR"
        else:
            grade = "NEEDS ATTENTION"

        if not recs:
            recs.append("All repositories clean and synchronized. Outstanding hygiene!")

        return HealthReport(
            score=score,
            grade=grade,
            total_repos=total,
            clean_repos=clean_count,
            dirty_repos=dirty_count,
            total_unpushed_commits=unpushed_total,
            recommendations=recs,
        )
