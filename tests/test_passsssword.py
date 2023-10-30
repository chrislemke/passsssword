import os
import subprocess
from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch

import pytest

from src.passsssword import (
    EnvFileExistsError,
    EnvOpFileNotFoundError,
    OpNotFoundError,
    contextor,
    decjector,
)


def test_OpNotFoundError() -> None:
    with patch("shutil.which", return_value=None):

        @decjector
        def dummy_func() -> None:
            pass

        with pytest.raises(OpNotFoundError):
            dummy_func()


def test_EnvFileExistsError(tmp_path: Path) -> None:
    os.chdir(tmp_path)
    with open(".env", "w"):
        pass
    with patch("shutil.which", return_value="op_path"):

        @decjector
        def dummy_func() -> None:
            pass

        with pytest.raises(EnvFileExistsError):
            dummy_func()


def test_EnvOpFileNotFoundError(tmp_path: Path) -> None:
    os.chdir(tmp_path)
    with patch("shutil.which", return_value="op_path"):

        @decjector
        def dummy_func() -> None:
            pass

        with pytest.raises(EnvOpFileNotFoundError):
            dummy_func()


def test_env_file_created_and_removed(tmp_path: Path) -> None:
    os.chdir(tmp_path)
    with open(".env.op", "w"):
        pass
    with patch("shutil.which", return_value="op_path"), patch(
        "subprocess.run", side_effect=lambda *args, **kwargs: open(".env", "w").close()
    ) as mock_run:

        @decjector
        def dummy_func() -> None:
            assert os.path.exists(".env")

        dummy_func()

    assert not os.path.exists(".env")
    mock_run.assert_called()


def test_decorated_function_executed(tmp_path: Path) -> None:
    os.chdir(tmp_path)
    with open(".env.op", "w"):
        pass
    with patch("shutil.which", return_value="op_path"), patch("subprocess.run"):

        @decjector
        def dummy_func() -> str:
            return "Executed"

        result = dummy_func()
    assert result == "Executed"


def __create_env_file(*args: Any, **kwargs: Any) -> None:
    with open(".env", "w") as f:
        f.write("TEST=VALUE")


def test_contextor_creates_and_removes_env_file(tmp_path: Path) -> None:
    os.chdir(tmp_path)

    with open(".env.op", "w") as f:
        f.write("DUMMY=VALUE")

    mock_run = Mock(side_effect=__create_env_file)

    with patch("shutil.which", return_value=True), patch("subprocess.run", mock_run):
        with contextor():
            mock_run.assert_called_with(
                ["op", "inject", "-i", ".env.op", "-o", ".env"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            assert os.path.exists(".env")

        assert not os.path.exists(".env")
