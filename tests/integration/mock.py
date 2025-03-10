import sys
from collections.abc import Sequence
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
    def get_all_installs(self) -> Sequence[MockInstall]:
        return _INSTALLS

    def uninstall_quietly(self, installation: MockInstall) -> None:
        assert_never(...)

    def uninstall(self, installation: MockInstall) -> None:
        assert_never(...)

    def install_quietly(
            self, installer_path: str, *, admin: bool = False
    ) -> None:
        assert_never(...)

    def install(self, installer_path: str, *, admin: bool = False) -> None:
        assert_never(...)


class MockOSInterface(OSInterface):
    def run_console(
            self,
            command: str | Sequence[str],
            *,
            stdin: str | None = None,
            timeout: float | None = None,
            env: dict | None = None,
            cwd: str | None = None
    ) -> ConsoleCommandResult:
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
        return assert_never(...)

    def get_install_interface(self) -> MockInstallInterface:
        return MockInstallInterface(self)


class MockWriteStream:
    def __init__(self):
        self._text = ""

    def write(self, text: str) -> None:
        self._text += text

    @property
    def value(self):  # noqa: WPS110
        return self._text

    def flush(self) -> None:
        ...


@final
@frozen
class Streams:
    stdout: MockWriteStream
    stderr: MockWriteStream


@contextmanager
def mock_streams() -> Streams:
    stdout = MockWriteStream()
    stderr = MockWriteStream()
    output._stderr = stderr  # noqa: SLF001
    output._stdout = stdout  # noqa: SLF001
    yield Streams(stdout, stderr)
    output._stdout = sys.stdout  # noqa: SLF001
    output._stderr = sys.stderr  # noqa: SLF001
