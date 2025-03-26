"""Implementation of contexts."""

import os
import time
from typing import TYPE_CHECKING, Final

from embark.domain.execution.context import (
    AbstractContextFactory,
    AbstractPlaybookExecutionContext,
    TaskExecutionContext,
)
from embark.domain.execution.playbook import Playbook
from embark.domain.interfacing.os_provider import OSInterface
from embark.domain.playbook_logger import AbstractPlaybookLogger
from embark.impl.cli_loggers import CLIPlaybookLogger

if TYPE_CHECKING:
    from embark.domain.tasks.task import Task


LOGGER_WAIT_SECONDS: Final[float] = 0.2


class CLIPlaybookExecutionContext(AbstractPlaybookExecutionContext):
    """Implementation of playbook execution context."""

    def __init__(self, playbook: Playbook, os_interface: OSInterface) -> None:
        """Create context."""
        self._playbook = playbook
        self._os_provider = os_interface

    def ask_should_proceed(self, text: str) -> bool:
        """Blocking function to ask user."""
        time.sleep(LOGGER_WAIT_SECONDS)
        print(text)  # noqa: WPS421
        answer = input("y/n> ")  # noqa: WPS421
        return answer.lower() == "y"

    @property
    def playbook(self) -> Playbook:
        """Get playbook."""
        return self._playbook

    def file_path(self, path: str) -> str:
        """Expand file path."""
        return os.path.expandvars(path)

    def create_logger(self) -> AbstractPlaybookLogger:
        """Create logger for playbook."""
        return CLIPlaybookLogger(self._playbook)

    @property
    def os_provider(self) -> OSInterface:
        """Get OS interface."""
        return self._os_provider


class CLIContextFactory(AbstractContextFactory):
    """Implementation of context factory."""

    def __init__(self, os_interface: OSInterface) -> None:
        """Create factory."""
        self.os_interface = os_interface

    def create_playbook_context(
            self,
            playbook: Playbook
    ) -> AbstractPlaybookExecutionContext:
        """Create playbook context."""
        return CLIPlaybookExecutionContext(playbook, self.os_interface)

    def create_task_context(
            self,
            playbook_context: AbstractPlaybookExecutionContext,
            task: "Task"
    ) -> TaskExecutionContext:
        """Create task context."""
        return TaskExecutionContext(playbook_context, task)
