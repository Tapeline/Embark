class WindowsPlatformException(Exception):
    """Thrown on any Windows interaction failure."""


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
