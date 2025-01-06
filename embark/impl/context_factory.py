"""Implementation of contexts."""

import os
import time
from typing import TYPE_CHECKING

from embark.domain.execution.playbook import Playbook
from embark.domain.tasks.task import (
    AbstractContextFactory,
    TaskExecutionContext,
    AbstractPlaybookExecutionContext,
)

if TYPE_CHECKING:
    from embark.domain.tasks.task import Task


class PlaybookExecutionContext(AbstractPlaybookExecutionContext):
    """Implementation of playbook execution context."""

    def __init__(self, playbook: Playbook) -> None:
        """Create context."""
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


class ContextFactory(AbstractContextFactory):
    """Implementation of context factory."""

    def create_playbook_context(
            self,
            playbook: Playbook
    ) -> AbstractPlaybookExecutionContext:
        return PlaybookExecutionContext(playbook)

    def create_task_context(
            self,
            playbook_context: AbstractPlaybookExecutionContext,
            task: Task
    ) -> TaskExecutionContext:
        return TaskExecutionContext(playbook_context, task)
