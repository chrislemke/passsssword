import functools
import os
import shutil
import subprocess
from contextlib import contextmanager
from typing import Any, Callable, Dict, Iterator, Tuple

from dotenv import load_dotenv


class EnvFileExistsError(FileExistsError):
    """Exception raised when a .env file already exists in the search path."""

    def __init__(self, search_dir: str) -> None:
        super().__init__(
            f"A '.env' file already exists in the directory: {search_dir}. Operation aborted."
        )


class OpNotFoundError(EnvironmentError):
    """Exception raised when the 'op' software is not found."""

    def __init__(self) -> None:
        super().__init__("The 'op' software is not installed. Please install it first.")


class EnvOpFileNotFoundError(FileNotFoundError):
    """Exception raised when the '.env.op' file is not found."""

    def __init__(self) -> None:
        super().__init__(
            "The '.env.op' file was not found in the search directories. Operation aborted."
        )


def decjector(func: Callable[..., Any]) -> Callable[..., Any]:
    """A decorator to execute the `op inject` command before execution and
    remove the `.env` file containing the raw passwords afterwards.

    This function utilizes the 1Password CLI's `inject` command to create a temporary
    environment file from a '.env.op' file. For more information on the `inject` command,
    visit: https://developer.1password.com/docs/cli/reference/commands/inject

    Example of `inject` command:
    ```
    op inject -i .env.op -o .env
    ```

    This decorator performs the following tasks:
    1. Checks if the 'op' software is installed.
    2. Searches for a '.env.op' file in the current and parent directories.
    3. Creates a '.env' file using 'op inject'.
    4. Executes the decorated function.
    5. Removes the '.env' file.

    Raises:
        EnvFileExistsError: If a '.env' file already exists in the search path.
        OpNotFoundError: If the 'op' software is not installed.
        EnvOpFileNotFoundError: If the '.env.op' file is not found.

    Returns:
        Callable[..., Any]: The return value of the decorated function.
    """

    @functools.wraps(func)
    def wrapper(*args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Any:
        env_file_created = False
        try:
            if not shutil.which("op"):
                raise OpNotFoundError()

            current_dir = os.getcwd()
            found_file = False
            file_path_op = None

            for i in range(4):
                search_dir = os.path.join(current_dir, *([".."] * i))
                file_path_op = os.path.join(search_dir, ".env.op")
                file_path_env = os.path.join(search_dir, ".env")

                if os.path.exists(file_path_env):
                    raise EnvFileExistsError(search_dir)

                if os.path.exists(file_path_op):
                    found_file = True
                    break

            if not found_file or file_path_op is None:
                raise EnvOpFileNotFoundError()

            relative_file_path_op = os.path.relpath(file_path_op)

            subprocess.run(
                ["op", "inject", "-i", relative_file_path_op, "-o", ".env"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            env_file_created = True

            load_dotenv(".env")

            result = func(*args, **kwargs)
            return result

        finally:
            if env_file_created and os.path.exists(".env"):
                os.remove(".env")

    return wrapper


@contextmanager
def contextor() -> Iterator[None]:
    """A context manager to handle the creation and deletion of a temporary
    '.env' file utilizing the 1Password CLI's `inject` command.

    This function automates the process of creating a temporary environment file from a
    '.env.op' file, loading the environment variables, and ensuring the temporary '.env'
    file is removed afterwards. For more information on the `inject` command, refer to:
    https://developer.1password.com/docs/cli/reference/commands/inject

    Example of `inject` command:
    ```
    op inject -i .env.op -o .env
    ```

    The context manager performs the following tasks:
    1. Checks for the availability of the 'op' software.
    2. Searches for a '.env.op' file in the current directory and up to three parent directories.
    3. Creates a '.env' file using 'op inject'.
    4. Loads the environment variables from the '.env' file using `load_dotenv`.
    5. Ensures the '.env' file is removed after exiting the context, even in the case of an exception.

    Raises:
        OpNotFoundError: If the 'op' software is not found.
        EnvFileExistsError: If a '.env' file already exists in the search path.
        EnvOpFileNotFoundError: If the '.env.op' file is not found.

    Yields:
        None: This context manager does not yield any value, but ensures proper setup
              and cleanup of the temporary environment file.
    """
    env_file_created = False
    try:
        if not shutil.which("op"):
            raise OpNotFoundError()

        current_dir = os.getcwd()
        found_file = False
        file_path_op = None

        for i in range(4):
            search_dir = os.path.join(current_dir, *([".."] * i))
            file_path_op = os.path.join(search_dir, ".env.op")
            file_path_env = os.path.join(search_dir, ".env")

            if os.path.exists(file_path_env):
                raise EnvFileExistsError(search_dir)

            if os.path.exists(file_path_op):
                found_file = True
                break

        if not found_file or file_path_op is None:
            raise EnvOpFileNotFoundError()

        relative_file_path_op = os.path.relpath(file_path_op)

        subprocess.run(
            ["op", "inject", "-i", relative_file_path_op, "-o", ".env"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        env_file_created = True

        load_dotenv(".env")

        yield

    finally:
        if env_file_created and os.path.exists(".env"):
            os.remove(".env")
