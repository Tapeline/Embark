import subprocess
from collections.abc import Sequence

from embark.domain.interfacing.os_provider import (
    ConsoleCommandResult,
    OSInterface,
)
from embark.platform_impl.windows.installs_provider import (
    WindowsInstallationsInterface,
)


class WindowsInterface(OSInterface[WindowsInstallationsInterface]):
    """Implementation for interacting with Windows."""

    def run_console(
            self,
            command: str | Sequence[str],
            *,
            stdin: str | None = None,
            timeout: float | None = None,
            env: dict[str, str] | None = None,
            cwd: str | None = None,
    ) -> ConsoleCommandResult:
        """Run using shell."""
        return self._run_impl(
            command,
            stdin=stdin,
            timeout=timeout,
            env=env,
            cwd=cwd,
            is_shell=True,
        )

    def run(
            self,
            command: str | Sequence[str],
            *,
            stdin: str | None = None,
            timeout: float | None = None,
            env: dict[str, str] | None = None,
            cwd: str | None = None,
    ) -> ConsoleCommandResult:
        """Run command."""
        return self._run_impl(
            command,
            stdin=stdin,
            timeout=timeout,
            env=env,
            cwd=cwd,
            is_shell=False,
        )

    def get_install_interface(self) -> WindowsInstallationsInterface:
        """Get installations interface."""
        return WindowsInstallationsInterface(self)

    def _run_impl(  # noqa: WPS211
            self,
            command: str | Sequence[str],
            *,
            is_shell: bool,
            stdin: str | None = None,
            timeout: float | None = None,
            env: dict[str, str] | None = None,
            cwd: str | None = None,
    ) -> ConsoleCommandResult:
        proc = subprocess.run(  # noqa: S603
            command,
            input=stdin,
            timeout=timeout,
            env=env,
            cwd=cwd,
            text=True,
            shell=is_shell, check=False,
        )
        return ConsoleCommandResult(
            stdout=proc.stdout,
            stderr=proc.stderr,
            return_code=proc.returncode
        )
