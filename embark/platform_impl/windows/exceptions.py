class WindowsPlatformException(Exception):
    """Thrown on any Windows interaction failure."""

    def __init__(
            self,
            return_code: int = 0,
            stdout: str = "",
            stderr: str = ""
    ) -> None:
        """Create exception."""
        self.stdout = stdout
        self.stderr = stderr
        self.return_code = return_code

    def __str__(self):
        """Transform to string."""
        return (
            f"Platform exception (retcode={self.return_code}):\n"
            f"{self.stdout}\n"
            f"---\n"
            f"{self.stderr}"
        )


class InstallationCommandNotProvidedException(Exception):
    """Thrown when install attempted, but no command specified."""


class CannotUninstallException(WindowsPlatformException):
    """Thrown when uninstall cannot be performed."""


class CannotUninstallQuietlyException(CannotUninstallException):
    """Thrown when silent uninstall cannot be performed."""


class CannotInstallException(WindowsPlatformException):
    """Thrown when install cannot be performed."""


class CannotInstallQuietlyException(CannotInstallException):
    """Thrown when silent install cannot be performed."""
