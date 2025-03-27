from tkinter import BOTH, LEFT, NW, Tk, W, Widget, X
from typing import Any

from customtkinter import CTkFrame, CTkLabel, CTkScrollableFrame

from embark.domain.execution.playbook import Playbook
from embark.domain.tasks.task import Task
from embark.localization.i18n import L
from embark.ui.components.loader import LoaderIcon, LoaderState
from embark.ui.components.logger_base import (
    AbstractLoggerFrame,
    LogMessageComponent,
    log_format,
)
from embark.ui.components.progress import Progress, ProgressMixin
from embark.ui.components.task_logger import GUITaskLoggerComponent
from embark.ui.constants import HEADER_FONT


class GUIPlaybookLoggerComponent(CTkFrame, ProgressMixin, AbstractLoggerFrame):
    """Playbook logger component."""

    def __init__(self, root: Widget | Tk) -> None:
        """Create component."""
        CTkFrame.__init__(self, root)
        ProgressMixin.__init__(self)
        self.playbook: Playbook | None = None
        self._progresses: dict[str, Progress] = {}
        self._header_pane = CTkFrame(self)
        self._logs_pane: Widget = CTkScrollableFrame(self)
        self._playbook_status = LoaderIcon(self._header_pane)
        self._playbook_header = CTkLabel(
            self._header_pane,
            text=L("UI.waiting_for_playbook"),
            font=HEADER_FONT()
        )
        self._playbook_status.pack(anchor=W, side=LEFT, padx=8, pady=8)
        self._playbook_header.pack(
            anchor=W,
            fill=X,
            side=LEFT,
            padx=8,
            pady=8
        )
        self._header_pane.pack(fill=X)
        self._logs_pane.pack(fill=BOTH, expand=True)

    def notify_started(self, playbook: Playbook) -> None:
        """Notify playbook started."""
        self.playbook = playbook
        self._playbook_header.configure(
            require_redraw=True,
            text=playbook.name
        )
        self._playbook_status.state = LoaderState.LOADING
        self.inform(L("UI.playbook_started"))

    def notify_ended(
            self, *, is_successful: bool, error_message: str | None = None
    ) -> None:
        """Notify playbook ended."""
        if is_successful:
            self._playbook_status.state = LoaderState.OK
        else:
            self._playbook_status.state = LoaderState.FAILED
            self.error(error_message or "error")
        self.inform(L("UI.playbook_ended"))

    def log(self, level: str, message: str, *args: Any) -> None:
        """Basic log impl."""
        component = LogMessageComponent(
            self._logs_pane,
            level,
            log_format(message, *args)
        )
        component.pack(anchor=NW, padx=2, pady=2)

    def create_task_logger(self, task: Task) -> GUITaskLoggerComponent:
        """Create child logger for task."""
        task_logger_frame = GUITaskLoggerComponent(self._logs_pane, task)
        task_logger_frame.pack(fill="x", anchor="nw", padx=10, pady=10)
        return task_logger_frame

    @property
    def log_component(self) -> Widget:
        """Get log component."""
        return self._logs_pane

    def default_inform(self, message: str, *args: Any) -> None:
        """Default information logging."""
        self.inform(message, *args)
