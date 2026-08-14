import os
import subprocess

COMPOSE_DOWN = ("docker", "compose", "down")

REQUIRED_BINARIES = ("docker",)
EXIT_MISSING_BINARY = 127


class MissingBinaryError(RuntimeError):
    """A required external command is not installed.

    Args:
        binary: Name of the missing executable.
    """

    def __init__(self, binary):
        super().__init__(f"required command '{binary}' is not installed")
        self.binary = binary


def iter_project_dirs(base_dir):
    """Yield the first-level subdirectories of base_dir, sorted by name.

    Args:
        base_dir: Directory whose children are scanned.
    """
    for entry in sorted(os.listdir(base_dir)):
        path = os.path.join(base_dir, entry)
        if os.path.isdir(path):
            yield path


def compose_down(path):
    """Run 'docker compose down' in path and return its exit code.

    Args:
        path: Working directory for the compose call.
    """
    try:
        return subprocess.run(list(COMPOSE_DOWN), cwd=path, check=False).returncode
    except FileNotFoundError as error:
        raise MissingBinaryError(COMPOSE_DOWN[0]) from error
