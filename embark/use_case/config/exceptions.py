"""Provides configuration loading exception."""


class ConfigLoadingException(Exception):
    """Thrown when config cannot be loaded."""

    def __init__(self, message: str) -> None:
        """Create exception."""
        super().__init__()
        self.add_note(message)
        self.message = message

    def __str__(self) -> str:
        """Convert to string."""
        return f"{self.__class__.__name__}: {self.message}"


class TaskLoadingException(ConfigLoadingException):
    """Thrown when task loader cannot load a task."""


class InvalidConfigException(ConfigLoadingException):
    """Thrown when config format is invalid."""


class LoaderNotFoundException(ConfigLoadingException):
    """Thrown when task loader is not found."""

    def __init__(self, loader_name: str) -> None:
        """Create exception."""
        super().__init__(f"Task loader {loader_name} not found")
        self.loader_name = loader_name
