import subprocess
from collections.abc import Sequence

from embark.domain.interfacing.os_provider import OSInterface, ConsoleCommandResult
from embark.platform_impl.windows.installs_provider import WindowsInstallationsInterface


class WindowsInterface(OSInterface[WindowsInstallationsInterface]):
    """Implementation for interacting with Windows."""

    def run_console(
            self,
            command: str | Sequence[str],
            *,
            stdin: str | None = None,
            timeout: float | None = None,
            env: dict | None = None,
            cwd: str | None = None,
    ) -> ConsoleCommandResult:
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
            env: dict | None = None,
            cwd: str | None = None,
    ) -> ConsoleCommandResult:
        return self._run_impl(
            command,
            stdin=stdin,
            timeout=timeout,
            env=env,
            cwd=cwd,
            is_shell=False,
        )

    def _run_impl(
            self,
            command: str | Sequence[str],
            *,
            is_shell: bool,
            stdin: str | None = None,
            timeout: float | None = None,
            env: dict | None = None,
            cwd: str | None = None,
    ) -> ConsoleCommandResult:
        proc = subprocess.run(
            command,
            input=stdin,
            timeout=timeout,
            env=env,
            cwd=cwd,
            text=True,
            universal_newlines=True,
            shell=is_shell,
        )
        return ConsoleCommandResult(
            stdout=proc.stdout,
            stderr=proc.stderr,
            return_code=proc.returncode
        )

    def get_install_interface(self) -> WindowsInstallationsInterface:
        return WindowsInstallationsInterface(self)
