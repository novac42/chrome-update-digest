"""
Command line entry points for the Chrome update digest toolbox.

The CLI provides lightweight wrappers around the existing processor scripts so
they can be executed via `uv run chrome-update-digest-cli <command> ...`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable, Iterable, Optional

from chrome_update_digest import __version__


def _invoke(script: Callable[[], int | None], argv: Iterable[str]) -> int:
    old_argv = sys.argv
    sys.argv = [script.__module__] + list(argv)
    try:
        result = script()
        return int(result) if isinstance(result, int) else 0
    finally:
        sys.argv = old_argv


def main(argv: Optional[Iterable[str]] = None) -> int:
    """Dispatch entry point for the chrome-update-digest CLI."""
    parser = argparse.ArgumentParser(
        prog="chrome-update-digest-cli",
        description="Utilities for managing Chrome release digest artefacts.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print the chrome-update-digest version and exit.",
    )

    subparsers = parser.add_subparsers(dest="command")

    process_parser = subparsers.add_parser(
        "process",
        help="Run the clean data pipeline (delegates to processors.clean_data_pipeline).",
    )
    process_parser.add_argument(
        "pipeline_args",
        nargs=argparse.REMAINDER,
        help="Arguments forwarded to clean_data_pipeline.py",
    )

    monitor_parser = subparsers.add_parser(
        "monitor",
        help="Track upstream release notes (delegates to processors.monitor_releases).",
    )
    monitor_parser.add_argument(
        "monitor_args",
        nargs=argparse.REMAINDER,
        help="Arguments forwarded to monitor_releases.py",
    )

    args, remainder = parser.parse_known_args(argv)

    if args.version and not args.command:
        print(__version__)
        return 0

    if args.command == "process":
        from chrome_update_digest.processors.clean_data_pipeline import main as process_main

        forwarded = args.pipeline_args if hasattr(args, "pipeline_args") else remainder
        return _invoke(process_main, forwarded)

    if args.command == "monitor":
        from chrome_update_digest.processors.monitor_releases import main as monitor_main

        forwarded = args.monitor_args if hasattr(args, "monitor_args") else remainder
        return _invoke(monitor_main, forwarded)

    if args.command:
        parser.error(f"Unknown command: {args.command}")
        return 1

    if args.version:
        print(__version__)
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":  # pragma: no cover - manual invocation
    sys.exit(main())
