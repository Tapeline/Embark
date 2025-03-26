from typing import Any

from embark.domain.execution.playbook import Playbook
from embark.domain.playbook_logger import AbstractTaskLogger
from embark.domain.tasks.task import Task
from embark.impl.cli_loggers import CLIPlaybookLogger, CLITaskLogger
from embark.ui.components.playbook_logger import GUIPlaybookLoggerComponent


class GUIPlaybookLogger(CLIPlaybookLogger):
    """GUI logger for playbook."""

    def __init__(
            self,
            playbook: Playbook,
            logger_frame: GUIPlaybookLoggerComponent
    ) -> None:
        """Create logger."""
        super().__init__(playbook)
        self.logger_frame = logger_frame

    def playbook_started(self) -> None:
        """Notify playbook started."""
        super().playbook_started()
        self.logger_frame.notify_started(self.playbook)

    def playbook_ended(
            self,
            *,
            is_successful: bool,
            error_message: str | None = None
    ) -> None:
        """Notify playbook ended."""
        super().playbook_ended(
            is_successful=is_successful, error_message=error_message
        )
        self.logger_frame.notify_ended(
            is_successful=is_successful, error_message=error_message
        )

    def info(self, message: str, *args: Any) -> None:
        """Log info."""
        super().info(message, *args)
        self.logger_frame.inform(message, *args)

    def warning(self, message: str, *args: Any) -> None:
        """Log warning."""
        super().warning(message, *args)
        self.logger_frame.warning(message, *args)

    def error(self, message: str, *args: Any) -> None:
        """Log error."""
        super().error(message, *args)
        self.logger_frame.error(message, *args)

    def exception(self, message: str, *args: Any) -> None:
        """Log exception."""
        super().exception(message, *args)
        self.logger_frame.exception(message, *args)

    def create_child_task_logger(self, task: Task) -> AbstractTaskLogger:
        """Create logger for task."""
        return GUITaskLogger(self.playbook, task, self.logger_frame)

    def start_progress(self, uid: str, title: str) -> None:
        """Start progressbar."""
        self.logger_frame.start_progress(uid, title)

    def set_progress(self, uid: str, progress: float) -> None:
        """Set current progress on progressbar."""
        self.logger_frame.set_progress(uid, progress)

    def finish_progress(self, uid: str) -> None:
        """Mark progressbar finished."""
        self.logger_frame.finish_progress(uid)


class GUITaskLogger(CLITaskLogger):
    """GUI logger for task."""

    def __init__(
            self,
            playbook: Playbook,
            task: Task,
            parent_logger_frame: GUIPlaybookLoggerComponent
    ) -> None:
        """Create logger."""
        super().__init__(playbook, task)
        self.logger_frame = parent_logger_frame.create_task_logger(task)

    def task_started(self) -> None:
        """Notify task started."""
        super().task_started()
        self.logger_frame.notify_started()

    def task_skipped(self) -> None:
        """Notify task skipped."""
        super().task_skipped()
        self.logger_frame.notify_skipped()

    def task_ended(
            self,
            *,
            is_successful: bool,
            error_message: str | None = None
    ) -> None:
        """Notify task ended."""
        super().task_ended(
            is_successful=is_successful, error_message=error_message
        )
        self.logger_frame.notify_ended(
            is_successful=is_successful, error_message=error_message
        )

    def info(self, message: str, *args: Any) -> None:
        """Log info."""
        super().info(message, *args)
        self.logger_frame.inform(message, *args)

    def warning(self, message: str, *args: Any) -> None:
        """Log warning."""
        super().warning(message, *args)
        self.logger_frame.warning(message, *args)

    def error(self, message: str, *args: Any) -> None:
        """Log error."""
        super().error(message, *args)
        self.logger_frame.error(message, *args)

    def exception(self, message: str, *args: Any) -> None:
        """Log exception."""
        super().exception(message, *args)
        self.logger_frame.exception(message, *args)

    def start_progress(self, uid: str, title: str) -> None:
        """Start progressbar."""
        self.logger_frame.start_progress(uid, title)

    def set_progress(self, uid: str, progress: float) -> None:
        """Set current progress on progressbar."""
        self.logger_frame.set_progress(uid, progress)

    def finish_progress(self, uid: str) -> None:
        """Mark progressbar finished."""
        self.logger_frame.finish_progress(uid)
