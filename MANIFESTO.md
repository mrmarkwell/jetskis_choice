# Jetski's Choice — Project Manifesto

> "The sovereign developer workstation radar & autonomous agent loop hub."

---

## 1. Vision & Core Purpose
Software engineers and AI agents work across multiple repositories, experimental directories, and autonomous loops. Context gets fragmented across terminal windows and directories.

**Jetski's Choice** (`keel`) is a fast, offline-first terminal radar that:
1. **Scans & Monitors Workspaces**: Discovers local repositories (Git and Piper/CitC), tracking dirty files, uncommitted changes, unpushed commits, and stale branches.
2. **Autonomous Loop Hub**: Discovers and monitors running or completed Ralph/Autoloop projects by inspecting `AGENT_LOG.md` and `ROADMAP.md`, computing real-time task velocities and completion percentages across all local projects.
3. **Developer Health Score**: Computes a holistic workstation hygiene score (0–100) based on uncommitted drift, unpushed work, and test integrity.
4. **Retro ASCII Helm TUI**: Delivers a rich, beautiful terminal dashboard with real-time status.

---

## 2. Core Pillars
### Sovereign & Dependency-Free
Operates 100% offline using Python 3 standard library only. Instant startup (<20ms). Zero pip or npm packages.

### Universal VCS & Loop Support
Native understanding of both Git and Google3 CitC/Piper workspaces, plus seamless auto-discovery of Autoloop / Ralph harnesses.

### High Terminal Ergonomics
Clean ANSI styling, compact summary tables, and intuitive CLI subcommands (`radar`, `loops`, `health`, `dashboard`).

---

## 3. Non-Negotiable Invariants
- 100% hermetic unit test pass required for every commit.
- Test suite execution latency must stay under 2.0 seconds.
- Zero external package dependencies (Python standard library only).
- All file reads across repositories must be strictly read-only and safe.

---

## 4. Autonomous Development Protocol
This codebase is developed, maintained, and self-improved primarily by autonomous LLM agents running in bounded execution loops ("Ralph loops"):
- Every agent is ephemeral, stateless, and self-contained.
- Institutional memory is externalized into living markdown documents (`ROADMAP.md`, `DECISIONS.md`, `AGENT_LOG.md`, `IDEAS.md`).
- Every cycle is tested, verified, and committed cleanly.
