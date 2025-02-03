from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from tkinter import LEFT

from customtkinter import (
    CTkScrollableFrame,
    CTkLabel,
    CTkFrame,
    CTkFont,
    CTkProgressBar
)

from embark.localization.i18n import L


_LOG_FONT = ("Consolas", 14, "normal")
_HEADER_FONT = ("TkDefaultFont", 16, "bold")
_SUBHEADER_FONT = ("TkDefaultFont", 14, "normal")


class LogMessageComponent(CTkLabel):
    def __init__(self, root, log_level, message):
        if log_level == "info":
            message = f"ⓘ {message}"
        if log_level == "warning":
            message = f"! {message}"
        if log_level == "error" or log_level == "exception":
            message = f"X {message}"
        super().__init__(root, text=message, font=CTkFont(*_LOG_FONT))


class AbstractLoggerFrame(ABC):
    def inform(self, message, *args):
        self.log("info", message, *args)

    def warning(self, message, *args):
        self.log("warning", message, *args)

    def error(self, message, *args):
        self.log("error", message, *args)

    def exception(self, message, *args):
        self.log("exception", message, *args)

    @abstractmethod
    def log(self, level, message: str, *args):
        raise NotImplementedError


@dataclass
class Progress:
    uid: str
    title: str
    progress: float
    progressbar: CTkProgressBar


class ProgressMixin:
    def __init__(self) -> None:
        self._progresses: dict[str, Progress] = {}

    @property
    @abstractmethod
    def log_component(self):
        raise NotImplementedError

    @abstractmethod
    def default_inform(self, message, *args):
        raise NotImplementedError

    def start_progress(self, uid: str, title: str):
        frame = CTkFrame(self.log_component)
        label = CTkLabel(frame, text=title, font=_SUBHEADER_FONT)
        label.pack(anchor="nw", padx=8, pady=4)
        progressbar = CTkProgressBar(frame, mode="indeterminate")
        progressbar.pack(anchor="nw", padx=8, pady=8, fill="x")
        progress = Progress(
            uid=uid,
            title=title,
            progress=-1,
            progressbar=progressbar
        )
        frame.pack(fill="x", padx=10)
        self._progresses[uid] = progress

    def set_progress(self, uid: str, progress: float):
        if uid not in self._progresses:
            self.default_inform(str(int(progress * 100)) + "%")
            return
        p = self._progresses[uid]
        p.progress = progress
        if p.progressbar._mode == "indeterminate":
            p.progressbar.configure(mode="determinate", require_redraw=True)
        p.progressbar.set(progress)

    def finish_progress(self, uid: str):
        if uid not in self._progresses:
            self.default_inform("100%")
            return
        p = self._progresses[uid]
        p.progress = 100
        if p.progressbar._mode == "indeterminate":
            p.progressbar.configure(mode="determinate", require_redraw=True)
        p.progressbar.set(1)


class GUILoggerFrame(CTkFrame, ProgressMixin, AbstractLoggerFrame):
    def __init__(self, root):
        super().__init__(root)  # type: ignore
        ProgressMixin.__init__(self)
        self.playbook = None
        self._progresses: dict[str, Progress] = {}
        self._header_pane = CTkFrame(self)
        self._logs_pane = CTkScrollableFrame(self)
        self._playbook_status = CTkLabel(
            self._header_pane,
            text="⌛",
            font=_HEADER_FONT
        )
        self._playbook_header = CTkLabel(
            self._header_pane,
            text=L("UI.waiting_for_playbook"),
            font=_HEADER_FONT
        )
        self._playbook_status.pack(anchor="w", side=LEFT, padx=5, pady=2)
        self._playbook_header.pack(
            anchor="w",
            fill="x",
            side=LEFT,
            padx=2,
            pady=2
        )
        self._header_pane.pack(fill="x")
        self._logs_pane.pack(fill="both", expand=True)
        self.configure(bg_color="#FF0000", require_redraw=True)

    def notify_started(self, playbook):
        self.playbook = playbook
        self._playbook_header.configure(
            require_redraw=True,
            text=playbook.name
        )
        self.inform(L("UI.playbook_started"))

    def notify_ended(self, is_successful: bool, error_message: str | None):
        if is_successful:
            self._playbook_status.configure(require_redraw=True, text="✅")
        else:
            self._playbook_status.configure(require_redraw=True, text="❌")
            self.error(error_message)
        self.inform(L("UI.playbook_ended"))

    def log(self, level, message: str, *args):
        component = LogMessageComponent(
            self._logs_pane,
            level,
            _format(message, *args)
        )
        component.pack(anchor="nw", padx=2, pady=2)

    def create_task_logger(self, task) -> "TaskLoggerFrame":
        task_logger_frame = TaskLoggerFrame(self._logs_pane, task)
        task_logger_frame.pack(fill="x", anchor="nw", padx=10, pady=10)
        return task_logger_frame

    @property
    def log_component(self):
        return self._logs_pane

    def default_inform(self, message, *args):
        self.inform(message, *args)


class TaskLoggerFrame(CTkFrame, ProgressMixin, AbstractLoggerFrame):
    def __init__(self, root, task):
        super().__init__(root)  # type: ignore
        ProgressMixin.__init__(self)
        self.task = task
        self._header_pane = CTkFrame(self)
        self._task_status = CTkLabel(
            self._header_pane,
            text="❔",
            font=_HEADER_FONT
        )
        self._task_header = CTkLabel(
            self._header_pane,
            text=task.get_display_name(),
            font=_HEADER_FONT
        )
        self._task_status.pack(anchor="w", side=LEFT, padx=10, pady=5)
        self._task_header.pack(
            anchor="w",
            fill="x",
            side=LEFT,
            padx=5,
            pady=5
        )
        self._header_pane.pack(fill="x")

    def notify_started(self):
        self._task_status.configure(require_redraw=True, text="⏳")
        self.inform(L("UI.task_started"))

    def notify_skipped(self):
        self._task_status.configure(require_redraw=True, text="⏩")
        self.inform(L("UI.task_skipped"))

    def notify_ended(self, is_successful: bool, error_message: str | None):
        if is_successful:
            self._task_status.configure(require_redraw=True, text="✅")
        else:
            self._task_status.configure(require_redraw=True, text="❌")
            self.error(error_message)
        self.inform(L("UI.task_ended"))

    def log(self, level, message: str, *args):
        component = LogMessageComponent(self, level, _format(message, *args))
        component.pack(padx=10, anchor="nw")

    @property
    def log_component(self):
        return self

    def default_inform(self, message, *args):
        self.inform(message, *args)


def _format(message: str, *args):
    return (
        "[" +
        datetime.now().strftime("%d/%m/%Y %H:%M:%S") +
        "] " +
        message % args
    )
