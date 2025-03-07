from typing import Any, Self

from embark.domain.playbook_logger import AbstractLogger


class ProgressReporter:
    """Context manager for progress reporting."""

    def __init__(self, logger: AbstractLogger, uid: str, title: str):
        """Create reporter."""
        self._uid = uid
        self._title = title
        self._logger = logger

    def __enter__(self) -> Self:
        """Report start."""
        self._logger.start_progress(self._uid, self._title)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Report end."""
        self._logger.finish_progress(self._uid)

    def set_progress(self, progress: float) -> None:
        """Report progress."""
        self._logger.set_progress(self._uid, progress)
