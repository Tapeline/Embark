from abc import ABC, abstractmethod


class AbstractLogger(ABC):
    @abstractmethod
    def info(self, message, *args):
        """Info level log."""

    @abstractmethod
    def warning(self, message, *args):
        """Warning level log."""

    @abstractmethod
    def error(self, message, *args):
        """Error level log."""

    @abstractmethod
    def exception(self, message, *args):
        """Exception log."""

    @abstractmethod
    def start_progress(self, uid: str, title: str):
        """Start progress bar."""

    @abstractmethod
    def set_progress(self, uid: str, progress: float):
        """
        Set progress bar
        :param uid: progress id
        :param progress: [0;1]
        """

    @abstractmethod
    def finish_progress(self, uid: str):
        """Mark progress as finished."""


class AbstractTaskLogger(AbstractLogger, ABC):
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
    def create_child_task_logger(self, task) -> AbstractTaskLogger:
        """Create logger for task."""
