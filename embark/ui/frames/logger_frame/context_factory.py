"""Implementation of contexts."""

import os
from tkinter import messagebox

from embark.domain.execution.context import (
    AbstractContextFactory,
    AbstractPlaybookExecutionContext,
    TaskExecutionContext,
)
from embark.domain.execution.playbook import Playbook
from embark.domain.interfacing.os_provider import OSInterface
from embark.domain.playbook_logger import AbstractPlaybookLogger
from embark.domain.tasks.task import Task
from embark.localization.i18n import L
from embark.ui.components.playbook_logger import GUIPlaybookLoggerComponent
from embark.ui.frames.logger_frame.ui_loggers import GUIPlaybookLogger


class GUIPlaybookExecutionContext(AbstractPlaybookExecutionContext):
    """Implementation of playbook execution context."""

    def __init__(
            self,
            playbook: Playbook,
            logger_frame: GUIPlaybookLoggerComponent,
            os_interface: OSInterface
    ) -> None:
        """Create context."""
        self._playbook = playbook
        self._logger_frame = logger_frame
        self._os_interface = os_interface

    def ask_should_proceed(self, text: str) -> bool:
        """Blocking function for asking."""
        return messagebox.askyesno(L("UI.ask_header"), text)

    @property
    def playbook(self) -> Playbook:
        """Get playbook."""
        return self._playbook

    def file_path(self, path: str) -> str:
        """Expand file path."""
        return os.path.expandvars(path)

    def create_logger(self) -> AbstractPlaybookLogger:
        """Create logger."""
        return GUIPlaybookLogger(self._playbook, self._logger_frame)

    @property
    def os_provider(self) -> OSInterface:
        """Get OS provider."""
        return self._os_interface


class GUIContextFactory(AbstractContextFactory):
    """Implementation of context factory."""

    def __init__(
            self,
            logger_frame: GUIPlaybookLoggerComponent,
            os_interface: OSInterface
    ) -> None:
        """Create context factory."""
        self._logger_frame = logger_frame
        self._os_interface = os_interface

    def create_playbook_context(
            self,
            playbook: Playbook
    ) -> AbstractPlaybookExecutionContext:
        """Create context for playbook."""
        return GUIPlaybookExecutionContext(
            playbook, self._logger_frame, self._os_interface
        )

    def create_task_context(
            self,
            playbook_context: AbstractPlaybookExecutionContext,
            task: Task
    ) -> TaskExecutionContext:
        """Create context for task."""
        return TaskExecutionContext(playbook_context, task)
