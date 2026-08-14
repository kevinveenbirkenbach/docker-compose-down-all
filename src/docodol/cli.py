import argparse
import os
import sys

from docodol.core import (
    COMPOSE_DOWN,
    EXIT_MISSING_BINARY,
    MissingBinaryError,
    compose_down,
    iter_project_dirs,
)


def build_parser():
    """Return the argument parser for the docodol command."""
    parser = argparse.ArgumentParser(
        description=(
            "Iterate through first-level subdirectories and run "
            "'docker compose down' in each."
        )
    )
    parser.add_argument(
        "base_dir",
        nargs="?",
        default=".",
        help="Base directory to search (default: current directory).",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Show commands without executing them.",
    )
    return parser


def main(argv=None):
    """Run 'docker compose down' in every first-level subdirectory.

    Args:
        argv: Argument list, defaults to sys.argv[1:].

    Returns:
        Process exit code.
    """
    args = build_parser().parse_args(argv)

    if not os.path.isdir(args.base_dir):
        print(f"Error: '{args.base_dir}' is not a directory.", file=sys.stderr)
        return 1

    try:
        for path in iter_project_dirs(args.base_dir):
            print(f"Switching to directory: {path}")

            if args.dry_run:
                print(f"DRY RUN: {' '.join(COMPOSE_DOWN)}")
            else:
                returncode = compose_down(path)
                if returncode != 0:
                    print(
                        f"Error: 'docker compose down' failed in {path} "
                        f"(exit code {returncode})",
                        file=sys.stderr,
                    )

            print(f"Finished in: {path}")
            print("-----------------------------")
    except MissingBinaryError as error:
        print(f"Error: {error}", file=sys.stderr)
        return EXIT_MISSING_BINARY

    return 0
