from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from embark.domain.tasks.task import Task


class AbstractLogger(ABC):
    """ABC for any logger."""

    @abstractmethod
    def info(self, message: str, *args: Any) -> None:
        """Info level log."""

    @abstractmethod
    def warning(self, message: str, *args: Any) -> None:
        """Warning level log."""

    @abstractmethod
    def error(self, message: str, *args: Any) -> None:
        """Error level log."""

    @abstractmethod
    def exception(self, message: str, *args: Any) -> None:
        """Exception log."""

    @abstractmethod
    def start_progress(self, uid: str, title: str) -> None:
        """Start progress bar."""

    @abstractmethod
    def set_progress(self, uid: str, progress: float) -> None:
        """
        Set progress bar.

        Args:
            uid: progress id
            progress: progress amount in [0;1]

        """

    @abstractmethod
    def finish_progress(self, uid: str) -> None:
        """Mark progress as finished."""


class AbstractTaskLogger(AbstractLogger, ABC):
    """ABC for task loggers."""

    @abstractmethod
    def task_started(self) -> None:
        """Notify task started."""

    @abstractmethod
    def task_skipped(self) -> None:
        """Notify task skipped."""

    @abstractmethod
    def task_ended(
            self,
            *,
            is_successful: bool,
            error_message: str | None = None
    ) -> None:
        """Notify task ended with status."""


class AbstractPlaybookLogger(AbstractLogger, ABC):
    """ABC for playbook loggers."""

    @abstractmethod
    def playbook_started(self) -> None:
        """Notify playbook started."""

    @abstractmethod
    def playbook_ended(
            self,
            *,
            is_successful: bool,
            error_message: str | None = None
    ) -> None:
        """Notify playbook ended."""

    @abstractmethod
    def create_child_task_logger(self, task: "Task") -> AbstractTaskLogger:
        """Create logger for task."""
