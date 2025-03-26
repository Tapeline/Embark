import logging
from abc import abstractmethod
from typing import Any

from embark import log_config
from embark.domain.execution.playbook import Playbook
from embark.domain.playbook_logger import (
    AbstractLogger,
    AbstractPlaybookLogger,
    AbstractTaskLogger,
)
from embark.domain.tasks.task import Task


class CommonCLILogger(AbstractLogger):
    """Common logging for terminal."""

    def __init__(self) -> None:
        """Init logger."""
        self._processes: dict[str, str] = {}

    @property
    @abstractmethod
    def logger(self) -> logging.Logger:
        """Get logger."""

    def info(self, message: str, *args: Any) -> None:
        """Display info message."""
        self.logger.info(message, *args)

    def warning(self, message: str, *args: Any) -> None:
        """Display warn message."""
        self.logger.warning(message, *args)

    def error(self, message: str, *args: Any) -> None:
        """Display error message."""
        self.logger.error(message, *args)

    def exception(self, message: str, *args: Any) -> None:
        """Display exception message."""
        self.logger.exception(message, *args)

    def start_progress(self, uid: str, title: str) -> None:
        """Start progressbar with some title."""
        self.info("Process %s started", title)
        self._processes[uid] = title

    def set_progress(self, uid: str, progress: float) -> None:
        """Set the progressbar."""
        self.info("%s: %s", uid, str(int(progress * 100)))

    def finish_progress(self, uid: str) -> None:
        """Finish the progress."""
        self.info("Process %s started", self._processes[uid])


class CLIPlaybookLogger(AbstractPlaybookLogger, CommonCLILogger):
    """Playbook logger for terminal."""

    def __init__(self, playbook: Playbook) -> None:
        """Create logger."""
        super().__init__()
        self.playbook = playbook
        self._logger = logging.getLogger(playbook.name)
        log_config.setup_default_handlers(self._logger)

    @property
    def logger(self) -> logging.Logger:
        """Get logger."""
        return self._logger

    def playbook_started(self) -> None:
        """Notify playbook started."""
        self.logger.info("Playbook started")

    def playbook_ended(
            self,
            *,
            is_successful: bool,
            error_message: str | None = None
    ) -> None:
        """Notify playbook ended."""
        if is_successful:
            self.logger.info("Playbook ended")
        else:
            self.logger.error("Playbook failed:\n%s", error_message)

    def create_child_task_logger(self, task: Task) -> AbstractTaskLogger:
        """Create logger for a task."""
        return CLITaskLogger(self.playbook, task)


class CLITaskLogger(AbstractTaskLogger, CommonCLILogger):
    """Task logger for terminal."""

    def __init__(self, playbook: Playbook, task: Task) -> None:
        """Init logger."""
        super().__init__()
        self.playbook = playbook
        self.task = task
        self._logger = logging.getLogger(task.name)
        log_config.setup_default_handlers(self._logger)

    @property
    def logger(self) -> logging.Logger:
        """Get logger."""
        return self._logger

    def task_started(self) -> None:
        """Notify task started."""
        self.logger.info("Task started")

    def task_skipped(self) -> None:
        """Notify task skipped."""
        self.logger.info("Task skipped")

    def task_ended(
            self,
            *,
            is_successful: bool,
            error_message: str | None = None
    ) -> None:
        """Notify task ended."""
        if is_successful:
            self.logger.info("Task complete")
        else:
            self.logger.error("Task failed:\n%s", error_message)
