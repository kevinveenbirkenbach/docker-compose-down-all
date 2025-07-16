#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Iterate through first-level subdirectories and run 'docker compose down' in each."
    )
    parser.add_argument(
        "base_dir",
        nargs="?",
        default=".",
        help="Base directory to search (default: current directory)."
    )
    parser.add_argument(
        "-n", "--dry-run",
        action="store_true",
        help="Show commands without executing them."
    )
    args = parser.parse_args()

    base_dir = args.base_dir
    if not os.path.isdir(base_dir):
        print(f"Error: '{base_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Iterate through all first-level subdirectories
    for entry in sorted(os.listdir(base_dir)):
        path = os.path.join(base_dir, entry)
        if os.path.isdir(path):
            print(f"Switching to directory: {path}")
            cmd = ["docker", "compose", "down"]

            if args.dry_run:
                print(f"DRY RUN: {' '.join(cmd)}")
            else:
                result = subprocess.run(cmd, cwd=path)
                if result.returncode != 0:
                    print(
                        f"Error: 'docker compose down' failed in {path} (exit code {result.returncode})",
                        file=sys.stderr
                    )

            print(f"Finished in: {path}")
            print("-----------------------------")


if __name__ == "__main__":
    main()
