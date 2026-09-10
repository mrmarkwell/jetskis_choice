"""Main CLI argument parsing and dispatch for Keel."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from core.version import __app_name__, __description__, __version__


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=__app_name__,
        description=f"{__app_name__}: {__description__}",
    )
    parser.add_argument("--version", "-v", action="version", version=f"{__app_name__} {__version__}")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # radar command
    radar_parser = subparsers.add_parser("radar", help="Scan local repositories for git/VCS status")
    radar_parser.add_argument("--root", default=".", help="Root directory to scan (default: current dir)")

    # loops command
    loops_parser = subparsers.add_parser("loops", help="Discover and monitor autonomous Ralph/Autoloop projects")
    loops_parser.add_argument("--root", default=".", help="Root directory to scan")

    # health command
    health_parser = subparsers.add_parser("health", help="Compute workstation developer hygiene score")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "radar":
        print("Keel Radar: scanning...")
        return 0
    elif args.command == "loops":
        print("Keel Loops: discovering...")
        return 0
    elif args.command == "health":
        print("Keel Health: computing...")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
