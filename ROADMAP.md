# Project Roadmap & Backlog

This document is the single source of truth for current project status, active tasks, and future backlog.
Autonomous agents must consult this document during boot and update it upon completing work.

---

## Current Status Overview
- **Active Phase**: Phase 0 (Harness Setup) & Phase 1 (Core Discovery Engine)
- **Overall Progress**: 1 Completed / 14 Total Tasks Tracked
- **Target Environment**: GIT (Python Standard Library)

---

## Phase Breakdown

### Phase 0: Repository Architecture & Verification Harness
- [x] **Task 0.1**: Initialize autonomous harness, living state machines, and developer tooling (ADR-001, ADR-002, ADR-003).
- [ ] **Task 0.2**: Establish core package architecture (`core/`, `cli/`, `tests/`) and executable entrypoint `keel`.
- [ ] **Task 0.3**: Implement initial test harness and verifying smoke test.
- [ ] **Task 0.4**: Configure automated doctor verification command in `config/autoloop.json`.

### Phase 1: Workspace Scanner & VCS Radar Engine
- [ ] **Task 1.1**: Implement `WorkspaceScanner` to discover Git and Piper/CitC repositories across filesystem roots.
- [ ] **Task 1.2**: Implement `RepoInspector` to extract branch, dirty status, uncommitted count, and unpushed commit count.
- [ ] **Task 1.3**: Implement CLI subcommand `keel radar` with formatted ANSI table output.
- [ ] **Task 1.4**: Hermetic unit tests for scanner and inspector with mock directories.

### Phase 2: Autonomous Loop Hub & Telemetry Tracker
- [ ] **Task 2.1**: Implement `LoopDetector` to identify Autoloop / Ralph repositories via `AGENT_LOG.md` and `ROADMAP.md`.
- [ ] **Task 2.2**: Implement `LoopTelemetry` parser extracting run count, active phase, completion %, and latest run status.
- [ ] **Task 2.3**: Implement CLI subcommand `keel loops` displaying multi-project agent progress.
- [ ] **Task 2.4**: Hermetic unit tests for loop telemetry parser.

### Phase 3: Workstation Health Score & Retro Dashboard
- [ ] **Task 3.1**: Implement `WorkstationHealthScorer` computing weighted hygiene score (0–100) and actionable recommendations.
- [ ] **Task 3.2**: Implement CLI subcommand `keel health`.
- [ ] **Task 3.3**: Implement ASCII Ship's Helm Dashboard (`keel dashboard` / `keel tui`).
- [ ] **Task 3.4**: Comprehensive end-to-end regression tests and documentation.
