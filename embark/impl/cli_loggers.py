import logging
from abc import abstractmethod

from embark import log_config
from embark.domain.execution.playbook import Playbook
from embark.domain.playbook_logger import (
    AbstractLogger,
    AbstractPlaybookLogger,
    AbstractTaskLogger,
)
from embark.domain.tasks.task import Task


class CommonCLILogger(AbstractLogger):
    def __init__(self):
        self._processes = {}

    @property
    @abstractmethod
    def logger(self) -> logging.Logger:
        raise NotImplementedError

    def info(self, message, *args) -> None:
        self.logger.info(message, *args)

    def warning(self, message, *args) -> None:
        self.logger.warning(message, *args)

    def error(self, message, *args) -> None:
        self.logger.error(message, *args)

    def exception(self, message, *args) -> None:
        self.logger.exception(message, *args)

    def start_progress(self, uid: str, title: str) -> None:
        self.info("Process %s started", title)
        self._processes[uid] = title

    def set_progress(self, uid: str, progress: float) -> None:
        self.info("%s: %s", uid, str(int(progress * 100)))

    def finish_progress(self, uid: str) -> None:
        self.info("Process %s started", self._processes[uid])


class CLIPlaybookLogger(AbstractPlaybookLogger, CommonCLILogger):
    def __init__(self, playbook: Playbook):
        super().__init__()
        self.playbook = playbook
        self._logger = logging.getLogger(playbook.name)
        log_config.setup_default_handlers(self._logger)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    def playbook_started(self) -> None:
        self.logger.info("Playbook started")

    def playbook_ended(
            self,
            *,
            is_successful: bool,
            error_message: str | None = None
    ) -> None:
        if is_successful:
            self.logger.info("Playbook ended")
        else:
            self.logger.error("Playbook failed:\n%s", error_message)

    def create_child_task_logger(self, task) -> AbstractTaskLogger:
        return CLITaskLogger(self.playbook, task)


class CLITaskLogger(AbstractTaskLogger, CommonCLILogger):
    def __init__(self, playbook: Playbook, task: Task):
        super().__init__()
        self.playbook = playbook
        self.task = task
        self._logger = logging.getLogger(playbook.name)
        log_config.setup_default_handlers(self._logger)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    def task_started(self) -> None:
        self.logger.info("Task started")

    def task_skipped(self) -> None:
        self.logger.info("Task skipped")

    def task_ended(
            self,
            *,
            is_successful: bool,
            error_message: str | None = None
    ) -> None:
        if is_successful:
            self.logger.info("Task complete")
        else:
            self.logger.error("Task failed:\n%s", error_message)
