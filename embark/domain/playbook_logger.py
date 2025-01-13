from abc import ABC, abstractmethod
from typing import Any, Self


class AbstractLogger(ABC):
    @abstractmethod
    def info(self, message, *args):
        raise NotImplementedError

    @abstractmethod
    def warning(self, message, *args):
        raise NotImplementedError

    @abstractmethod
    def error(self, message, *args):
        raise NotImplementedError

    @abstractmethod
    def exception(self, message, *args):
        raise NotImplementedError

    @abstractmethod
    def start_progress(self, uid: str, title: str):
        raise NotImplementedError

    @abstractmethod
    def set_progress(self, uid: str, progress: float):
        """
        Set progress bar
        :param uid: progress id
        :param progress: [0;1]
        """
        raise NotImplementedError

    @abstractmethod
    def finish_progress(self, uid: str):
        raise NotImplementedError


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


class AbstractTaskLogger(AbstractLogger, ABC):
    @abstractmethod
    def task_started(self):
        raise NotImplementedError

    @abstractmethod
    def task_skipped(self):
        raise NotImplementedError

    @abstractmethod
    def task_ended(self, is_successful: bool, error_message: str | None = None):
        raise NotImplementedError


class AbstractPlaybookLogger(AbstractLogger, ABC):
    @abstractmethod
    def playbook_started(self):
        raise NotImplementedError

    @abstractmethod
    def playbook_ended(self, is_successful: bool, error_message: str | None = None):
        raise NotImplementedError

    @abstractmethod
    def create_child_task_logger(self, task) -> AbstractTaskLogger:
        raise NotImplementedError
