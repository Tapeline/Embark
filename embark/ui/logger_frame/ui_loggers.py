from embark.domain.execution.playbook import Playbook
from embark.domain.playbook_logger import AbstractTaskLogger
from embark.domain.tasks.task import Task
from embark.impl.cli_loggers import CLIPlaybookLogger, CLITaskLogger
from embark.ui.logger_frame.components import GUILoggerFrame


class GUIPlaybookLogger(CLIPlaybookLogger):
    def __init__(self, playbook: Playbook, logger_frame: GUILoggerFrame):
        super().__init__(playbook)
        self.logger_frame = logger_frame

    def playbook_started(self):
        super().playbook_started()
        self.logger_frame.notify_started(self.playbook)

    def playbook_ended(self, is_successful: bool, error_message: str | None = None):
        super().playbook_ended(is_successful, error_message)
        self.logger_frame.notify_ended(is_successful, error_message)

    def info(self, message, *args):
        super().info(message, *args)
        self.logger_frame.inform(message, *args)

    def warning(self, message, *args):
        super().warning(message, *args)
        self.logger_frame.warning(message, *args)

    def error(self, message, *args):
        super().error(message, *args)
        self.logger_frame.error(message, *args)

    def exception(self, message, *args):
        super().exception(message, *args)
        self.logger_frame.exception(message, *args)

    def create_child_task_logger(self, task) -> AbstractTaskLogger:
        return GUITaskLogger(self.playbook, task, self.logger_frame)


class GUITaskLogger(CLITaskLogger):
    def __init__(self, playbook: Playbook, task: Task, parent_logger_frame: GUILoggerFrame):
        super().__init__(playbook, task)
        self.logger_frame = parent_logger_frame.create_task_logger(task)

    def task_started(self):
        super().task_started()
        self.logger_frame.notify_started()

    def task_skipped(self):
        super().task_skipped()
        self.logger_frame.notify_skipped()

    def task_ended(self, is_successful: bool, error_message: str | None = None):
        super().task_ended(is_successful, error_message)
        self.logger_frame.notify_ended(is_successful, error_message)

    def info(self, message, *args):
        super().info(message, *args)
        self.logger_frame.inform(message, *args)

    def warning(self, message, *args):
        super().warning(message, *args)
        self.logger_frame.warning(message, *args)

    def error(self, message, *args):
        super().error(message, *args)
        self.logger_frame.error(message, *args)

    def exception(self, message, *args):
        super().exception(message, *args)
        self.logger_frame.exception(message, *args)
