from tkinter import LEFT, NW, W, Widget, X
from typing import Any

from customtkinter import CTkFrame, CTkLabel

from embark.domain.tasks.task import Task
from embark.localization.i18n import L
from embark.ui.components.loader import LoaderIcon, LoaderState
from embark.ui.components.logger_base import (
    AbstractLoggerFrame,
    LogMessageComponent,
    log_format,
)
from embark.ui.components.progress import ProgressMixin
from embark.ui.constants import HEADER_FONT


class GUITaskLoggerComponent(CTkFrame, ProgressMixin, AbstractLoggerFrame):
    """Task logger component."""

    def __init__(self, root: Widget, task: Task) -> None:
        """Create component."""
        CTkFrame.__init__(self, root)
        ProgressMixin.__init__(self)
        self.task = task
        self._header_pane = CTkFrame(self)
        self._task_status = LoaderIcon(
            self._header_pane,
        )
        self._task_header = CTkLabel(
            self._header_pane,
            text=task.get_display_name(),
            font=HEADER_FONT()
        )
        self._task_status.pack(anchor=W, side=LEFT, padx=10, pady=5)
        self._task_header.pack(
            anchor=W,
            fill=X,
            side=LEFT,
            padx=5,
            pady=5
        )
        self._header_pane.pack(fill=X, padx=8, pady=8)

    def notify_started(self) -> None:
        """Notify task started."""
        self._task_status.state = LoaderState.LOADING
        self.inform(L("UI.task_started"))

    def notify_skipped(self) -> None:
        """Notify task skipped."""
        self._task_status.state = LoaderState.SKIPPED
        self.inform(L("UI.task_skipped"))

    def notify_ended(
            self, *, is_successful: bool, error_message: str | None = None
    ) -> None:
        """Notify task ended."""
        if is_successful:
            self._task_status.state = LoaderState.OK
        else:
            self._task_status.state = LoaderState.FAILED
            self.error(error_message or "error")
        self.inform(L("UI.task_ended"))

    def log(self, level: str, message: str, *args: Any) -> None:
        """Basic log impl."""
        component = LogMessageComponent(
            self, level, log_format(message, *args)
        )
        component.pack(padx=10, anchor=NW)

    @property
    def log_component(self) -> Widget:
        """Get log component."""
        return self

    def default_inform(self, message: str, *args: Any) -> None:
        """Default information logging."""
        self.inform(message, *args)
