import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"


def run_cli(*args, path=None):
    """Run 'python -m docodol' with the working tree on PYTHONPATH.

    Args:
        args: Command line arguments for the CLI.
        path: Replacement PATH, used to hide the docker binary.
    """
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_DIR)
    if path is not None:
        env["PATH"] = str(path)
    return subprocess.run(
        [sys.executable, "-m", "docodol", *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


class TestCli(unittest.TestCase):
    def test_dry_run_lists_every_subdirectory(self):
        with tempfile.TemporaryDirectory() as base:
            os.mkdir(os.path.join(base, "alpha"))
            os.mkdir(os.path.join(base, "beta"))

            result = run_cli(base, "--dry-run")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("alpha", result.stdout)
        self.assertIn("beta", result.stdout)
        self.assertIn("DRY RUN: docker compose down", result.stdout)

    def test_missing_directory_exits_non_zero(self):
        result = run_cli("/nonexistent/docodol/path")

        self.assertEqual(result.returncode, 1)
        self.assertIn("is not a directory", result.stderr)

    def test_help_exits_zero(self):
        result = run_cli("--help")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("docker compose down", result.stdout)

    def test_missing_docker_fails_cleanly(self):
        with (
            tempfile.TemporaryDirectory() as base,
            tempfile.TemporaryDirectory() as empty,
        ):
            os.mkdir(os.path.join(base, "alpha"))

            result = run_cli(base, path=empty)

        self.assertEqual(result.returncode, 127)
        self.assertIn("required command 'docker' is not installed", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
