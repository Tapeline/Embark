import logging

from embark import log_config
from embark.domain.execution.playbook import Playbook
from embark.domain.playbook_logger import AbstractPlaybookLogger, AbstractTaskLogger
from embark.domain.tasks.task import Task


class CLIPlaybookLogger(AbstractPlaybookLogger):
    def __init__(self, playbook: Playbook):
        self.playbook = playbook
        self.logger = logging.getLogger(playbook.name)
        log_config.setup_default_handlers(self.logger)

    def playbook_started(self):
        self.logger.info("Playbook started")

    def playbook_ended(self, is_successful: bool, error_message: str | None = None):
        if is_successful:
            self.logger.info("Playbook ended")
        else:
            self.logger.error("Playbook failed:\n%s", error_message)

    def info(self, message, *args):
        self.logger.info(message, *args)

    def warning(self, message, *args):
        self.logger.warning(message, *args)

    def error(self, message, *args):
        self.logger.error(message, *args)

    def exception(self, message, *args):
        self.logger.exception(message, *args)

    def create_child_task_logger(self, task) -> AbstractTaskLogger:
        return CLITaskLogger(self.playbook, task)


class CLITaskLogger(AbstractTaskLogger):
    def __init__(self, playbook: Playbook, task: Task):
        self.playbook = playbook
        self.task = task
        self.logger = logging.getLogger(task.name)
        log_config.setup_default_handlers(self.logger)

    def task_started(self):
        self.logger.info("Task started")

    def task_skipped(self):
        self.logger.info("Task skipped")

    def task_ended(self, is_successful: bool, error_message: str | None = None):
        if is_successful:
            self.logger.info("Task complete")
        else:
            self.logger.error("Task failed:\n%s", error_message)

    def info(self, message, *args):
        self.logger.info(message, *args)

    def warning(self, message, *args):
        self.logger.warning(message, *args)

    def error(self, message, *args):
        self.logger.error(message, *args)

    def exception(self, message, *args):
        self.logger.exception(message, *args)
