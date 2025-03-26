import sys
from collections.abc import Generator, Sequence
from contextlib import contextmanager
from typing import Final, assert_never, final

from attrs import frozen

from embark import output
from embark.domain.interfacing.installs_provider import (
    Installation,
    InstallationsInterface,
)
from embark.domain.interfacing.os_provider import (
    ConsoleCommandResult,
    OSInterface,
)


class MockInstall(Installation):
    """Mock install."""


_INSTALLS: Final = (
    MockInstall("NameA", "1.0", "PubA"),
    MockInstall("NameB", "1.1", "PubA"),
    MockInstall("NameC", "1.2", "PubB"),
    MockInstall("NameD", "1.3", "PubB"),
)


class MockInstallInterface(InstallationsInterface[MockInstall]):
    """Mock installs."""

    def get_all_installs(self) -> Sequence[MockInstall]:
        """Get all installs."""
        return _INSTALLS

    def uninstall_quietly(self, installation: MockInstall) -> None:
        """Should never happen."""
        assert_never(...)

    def uninstall(self, installation: MockInstall) -> None:
        """Should never happen in testing."""
        assert_never(...)

    def install_quietly(
            self, installer_path: str, *, admin: bool = False
    ) -> None:
        """Should never happen in testing."""
        assert_never(...)

    def install(self, installer_path: str, *, admin: bool = False) -> None:
        """Should never happen in testing."""
        assert_never(...)


class MockOSInterface(OSInterface):
    """Mock OS."""

    def run_console(
            self,
            command: str | Sequence[str],
            *,
            stdin: str | None = None,
            timeout: float | None = None,
            env: dict | None = None,
            cwd: str | None = None
    ) -> ConsoleCommandResult:
        """Should never happen."""
        return assert_never(...)

    def run(
            self,
            command: str | Sequence[str],
            *,
            stdin: str | None = None,
            timeout: float | None = None,
            env: dict | None = None,
            cwd: str | None = None
    ) -> ConsoleCommandResult:
        """Should never happen."""
        return assert_never(...)

    def get_install_interface(self) -> MockInstallInterface:
        """Get install interface."""
        return MockInstallInterface(self)


class MockWriteStream:
    """Mocked stream."""

    def __init__(self):
        """Init mocked stream."""
        self._text = ""

    def write(self, text: str) -> None:
        """Write text."""
        self._text += text

    @property
    def value(self):  # noqa: WPS110
        """Get text."""
        return self._text

    def flush(self) -> None:
        """Flush."""


@final
@frozen
class Streams:
    """Mocked streams."""

    stdout: MockWriteStream
    stderr: MockWriteStream


@contextmanager
def mock_streams() -> Generator[Streams]:
    """Intercept stdout and stderr."""
    stdout = MockWriteStream()
    stderr = MockWriteStream()
    output._stderr = stderr  # noqa: SLF001
    output._stdout = stdout  # noqa: SLF001
    yield Streams(stdout, stderr)
    output._stdout = sys.stdout  # noqa: SLF001
    output._stderr = sys.stderr  # noqa: SLF001
