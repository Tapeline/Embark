from abc import ABC, abstractmethod
from collections.abc import Sequence

from attrs import frozen

from embark.domain.interfacing.installs_provider import InstallationsInterface


@frozen
class ConsoleCommandResult:
    stdout: str
    stderr: str
    return_code: int

    @property
    def is_successful(self) -> bool:
        return self.return_code == 0


class OSInterface[
    InstallInterface_T: InstallationsInterface
](ABC):
    @abstractmethod
    def run_console(
            self,
            command: str | Sequence[str],
            *,
            stdin: str | None = None,
            timeout: float | None = None,
            env: dict | None = None,
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
            env: dict | None = None,
            cwd: str | None = None
    ) -> ConsoleCommandResult:
        """Run a command in console."""

    @abstractmethod
    def get_install_interface(self) -> InstallInterface_T:
        """Get an installations interface."""
