"""Implementation of contexts."""

import os
import time
from typing import TYPE_CHECKING, Final

from embark.domain.execution.playbook import Playbook
from embark.domain.interfacing.os_provider import OSInterface
from embark.domain.tasks.task import (
    AbstractContextFactory,
    TaskExecutionContext,
    AbstractPlaybookExecutionContext,
)
from embark.domain.playbook_logger import AbstractPlaybookLogger
from embark.impl.cli_loggers import CLIPlaybookLogger
from embark.platform_impl.windows.os_provider import WindowsInterface

if TYPE_CHECKING:
    from embark.domain.tasks.task import Task


LOGGER_WAIT_SECONDS: Final[float] = 0.2


class CLIPlaybookExecutionContext(AbstractPlaybookExecutionContext):
    """Implementation of playbook execution context."""

    def __init__(self, playbook: Playbook) -> None:
        """Create context."""
        self._playbook = playbook
        self._os_provider = WindowsInterface()

    def ask_should_proceed(self, text: str) -> bool:
        time.sleep(LOGGER_WAIT_SECONDS)
        print(text)  # noqa: WPS421
        answer = input("y/n> ")  # noqa: WPS421
        return answer.lower() == "y"

    @property
    def playbook(self):
        return self._playbook

    def file_path(self, path) -> str:
        return os.path.expandvars(path)

    def create_logger(self) -> AbstractPlaybookLogger:
        return CLIPlaybookLogger(self._playbook)

    @property
    def os_provider(self) -> OSInterface:
        return self._os_provider


class CLIContextFactory(AbstractContextFactory):
    """Implementation of context factory"""

    def create_playbook_context(
            self,
            playbook: Playbook
    ) -> AbstractPlaybookExecutionContext:
        return CLIPlaybookExecutionContext(playbook)

    def create_task_context(
            self,
            playbook_context: AbstractPlaybookExecutionContext,
            task: "Task"
    ) -> TaskExecutionContext:
        return TaskExecutionContext(playbook_context, task)
