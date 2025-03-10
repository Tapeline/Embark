import sys
from contextlib import contextmanager
from typing import Sequence, Final, final

from attrs import frozen

from embark import output
from embark.domain.interfacing.installs_provider import InstallationsInterface, Installation
from embark.domain.interfacing.os_provider import OSInterface, ConsoleCommandResult


class MockInstall(Installation):
    ...


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
        pass

    def uninstall(self, installation: MockInstall) -> None:
        pass

    def install_quietly(self, installer_path: str, *, admin: bool = False) -> None:
        pass

    def install(self, installer_path: str, *, admin: bool = False) -> None:
        pass


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
        pass

    def run(
            self,
            command: str | Sequence[str],
            *,
            stdin: str | None = None,
            timeout: float | None = None,
            env: dict | None = None,
            cwd: str | None = None
    ) -> ConsoleCommandResult:
        pass

    def get_install_interface(self) -> MockInstallInterface:
        return MockInstallInterface(self)


class MockWriteStream:
    def __init__(self):
        self._text = ""

    def write(self, text: str) -> None:
        self._text += text

    @property
    def value(self):
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
    output._stderr = stderr
    output._stdout = stdout
    yield Streams(stdout, stderr)
    output._stdout = sys.stdout
    output._stderr = sys.stderr
