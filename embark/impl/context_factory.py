"""
Implementation of contexts
"""
import os
import time

from embark.domain.playbook_logger import AbstractPlaybookLogger
from embark.domain.tasks.task import (AbstractContextFactory,
                                      TaskExecutionContext,
                                      AbstractPlaybookExecutionContext)
from embark.impl.cli_loggers import CLIPlaybookLogger


class CLIPlaybookExecutionContext(AbstractPlaybookExecutionContext):
    """Implementation of playbook execution context"""

    def __init__(self, playbook):
        self._playbook = playbook

    def ask_should_proceed(self, text: str) -> bool:
        time.sleep(0.2)
        print(text)
        answer = input("y/n> ")
        return answer.lower() == "y"

    @property
    def playbook(self):
        return self._playbook

    def file_path(self, path) -> str:
        return os.path.expandvars(path)

    def create_logger(self) -> AbstractPlaybookLogger:
        return CLIPlaybookLogger(self._playbook)


class CLIContextFactory(AbstractContextFactory):
    """Implementation of context factory"""

    def create_playbook_context(self, playbook) -> AbstractPlaybookExecutionContext:
        return CLIPlaybookExecutionContext(playbook)

    def create_task_context(self, playbook_context, task) -> TaskExecutionContext:
        return TaskExecutionContext(playbook_context, task)
