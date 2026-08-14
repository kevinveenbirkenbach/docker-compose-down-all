import os
import tempfile
import unittest
from unittest import mock

from docodol.core import (
    COMPOSE_DOWN,
    REQUIRED_BINARIES,
    MissingBinaryError,
    compose_down,
    iter_project_dirs,
)


class TestIterProjectDirs(unittest.TestCase):
    def test_yields_only_directories_sorted(self):
        with tempfile.TemporaryDirectory() as base:
            os.mkdir(os.path.join(base, "zeta"))
            os.mkdir(os.path.join(base, "alpha"))
            with open(os.path.join(base, "loose.txt"), "w") as handle:
                handle.write("")

            self.assertEqual(
                list(iter_project_dirs(base)),
                [os.path.join(base, "alpha"), os.path.join(base, "zeta")],
            )

    def test_empty_directory_yields_nothing(self):
        with tempfile.TemporaryDirectory() as base:
            self.assertEqual(list(iter_project_dirs(base)), [])


class TestComposeDown(unittest.TestCase):
    def test_invokes_docker_compose_down_in_path(self):
        with mock.patch("docodol.core.subprocess.run") as run:
            run.return_value.returncode = 0
            self.assertEqual(compose_down("/srv/app"), 0)

        run.assert_called_once_with(list(COMPOSE_DOWN), cwd="/srv/app", check=False)

    def test_propagates_exit_code(self):
        with mock.patch("docodol.core.subprocess.run") as run:
            run.return_value.returncode = 17
            self.assertEqual(compose_down("/srv/app"), 17)

    def test_missing_docker_raises_missing_binary(self):
        with mock.patch("docodol.core.subprocess.run") as run:
            run.side_effect = FileNotFoundError

            with self.assertRaises(MissingBinaryError) as caught:
                compose_down("/srv/app")

        self.assertEqual(caught.exception.binary, "docker")


class TestRequiredBinaries(unittest.TestCase):
    def test_declares_every_external_command_the_package_calls(self):
        self.assertEqual(set(REQUIRED_BINARIES), {COMPOSE_DOWN[0]})


if __name__ == "__main__":
    unittest.main()
