"""Main CLI argument parsing and dispatch for Keel."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import List, Optional

from cli.radar import run_radar
from cli.loops import run_loops
from cli.health import run_health
from cli.dashboard import run_dashboard
from core.version import __app_name__, __description__, __version__


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=__app_name__,
        description=f"{__app_name__}: {__description__}",
    )
    parser.add_argument("--version", "-v", action="version", version=f"{__app_name__} {__version__}")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # dashboard command
    dash_parser = subparsers.add_parser("dashboard", help="Display unified ASCII helm workstation dashboard")
    dash_parser.add_argument("--root", default=".", help="Root directory to scan")
    dash_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    # radar command
    radar_parser = subparsers.add_parser("radar", help="Scan local repositories for git/VCS status")
    radar_parser.add_argument("--root", default=".", help="Root directory to scan")
    radar_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    # loops command
    loops_parser = subparsers.add_parser("loops", help="Discover and monitor autonomous Ralph/Autoloop projects")
    loops_parser.add_argument("--root", default=".", help="Root directory to scan")
    loops_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    # health command
    health_parser = subparsers.add_parser("health", help="Compute workstation developer hygiene score")
    health_parser.add_argument("--root", default=".", help="Root directory to scan")
    health_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command or args.command == "dashboard":
        return run_dashboard(Path(args.root if hasattr(args, "root") else "."), json_output=args.json)

    if args.command == "radar":
        return run_radar(Path(args.root), json_output=args.json)
    elif args.command == "loops":
        return run_loops(Path(args.root), json_output=args.json)
    elif args.command == "health":
        return run_health(Path(args.root if hasattr(args, "root") else "."), json_output=args.json)

    return 0


if __name__ == "__main__":
    sys.exit(main())
