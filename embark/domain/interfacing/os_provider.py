from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from attrs import frozen

from embark.domain.interfacing.installs_provider import InstallationsInterface


@frozen
class ConsoleCommandResult:
    """Result of running console command."""

    stdout: str
    stderr: str
    return_code: int

    @property
    def is_successful(self) -> bool:
        """Check whether command executed successfully."""
        return self.return_code == 0


class OSInterface[
    InstallInterface_T: InstallationsInterface   # type: ignore
        = InstallationsInterface
](ABC):
    """Provides methods for interacting with OS."""

    @abstractmethod
    def run_console(
            self,
            command: str | Sequence[str],
            *,
            stdin: str | None = None,
            timeout: float | None = None,
            env: dict[str, Any] | None = None,
            cwd: str | None = None
    ) -> ConsoleCommandResult:
        """Run a command in console."""

    @abstractmethod
    def run(
            self,
            command: str | Sequence[str],
            *,
            stdin: str | None = None,
            timeout: float | None = None,
            env: dict[str, Any] | None = None,
            cwd: str | None = None
    ) -> ConsoleCommandResult:
        """Run a command in console."""

    @abstractmethod
    def get_install_interface(self) -> InstallInterface_T:
        """Get an installations interface."""
