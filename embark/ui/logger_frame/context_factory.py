"""
Implementation of contexts
"""
import os
from tkinter import messagebox

from embark.domain.interfacing.os_provider import OSInterface
from embark.domain.playbook_logger import AbstractPlaybookLogger
from embark.domain.tasks.task import (
    AbstractContextFactory,
    AbstractPlaybookExecutionContext,
    TaskExecutionContext,
)
from embark.localization.i18n import L
from embark.platform_impl.windows.os_provider import WindowsInterface
from embark.ui.logger_frame.ui_loggers import GUIPlaybookLogger


class GUIPlaybookExecutionContext(AbstractPlaybookExecutionContext):
    """Implementation of playbook execution context"""

    def __init__(self, playbook, logger_frame):
        self._playbook = playbook
        self._logger_frame = logger_frame

    def ask_should_proceed(self, text: str) -> bool:
        return messagebox.askyesno(L("UI.ask_header"), text)

    @property
    def playbook(self):
        return self._playbook

    def file_path(self, path) -> str:
        return os.path.expandvars(path)

    def create_logger(self) -> AbstractPlaybookLogger:
        return GUIPlaybookLogger(self._playbook, self._logger_frame)

    @property
    def os_provider(self) -> OSInterface:
        return WindowsInterface()


class GUIContextFactory(AbstractContextFactory):
    """Implementation of context factory"""

    def __init__(self, logger_frame):
        self._logger_frame = logger_frame

    def create_playbook_context(
            self,
            playbook
    ) -> AbstractPlaybookExecutionContext:
        return GUIPlaybookExecutionContext(playbook, self._logger_frame)

    def create_task_context(
            self,
            playbook_context,
            task
    ) -> TaskExecutionContext:
        return TaskExecutionContext(playbook_context, task)
