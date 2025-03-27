import tkinter
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

from customtkinter import CTkFrame, CTkLabel, CTkProgressBar

from embark.ui.constants import SUBHEADER_FONT


@dataclass
class Progress:
    """Progressbar."""

    uid: str
    title: str
    progress: float
    progressbar: CTkProgressBar


class ProgressMixin:
    """Helper mixin for progressbar."""

    def __init__(self) -> None:
        """Create mixin."""
        self._progresses: dict[str, Progress] = {}

    @property
    @abstractmethod
    def log_component(self) -> tkinter.Widget:
        """Get logging component."""

    @abstractmethod
    def default_inform(self, message: str, *args: Any) -> None:
        """Inform progress with text."""

    def start_progress(self, uid: str, title: str) -> None:
        """Start progressbar."""
        frame = CTkFrame(self.log_component)
        label = CTkLabel(frame, text=title, font=SUBHEADER_FONT())
        label.pack(anchor="nw", padx=8, pady=4)
        progressbar = CTkProgressBar(frame, mode="indeterminate")
        progressbar.pack(anchor="nw", padx=8, pady=(0, 8), fill="x")
        progress = Progress(
            uid=uid,
            title=title,
            progress=-1,
            progressbar=progressbar
        )
        frame.pack(fill="x", padx=10, pady=(0, 8))
        self._progresses[uid] = progress

    def set_progress(self, uid: str, progress: float) -> None:
        """Set progress on progressbar."""
        if uid not in self._progresses:
            self.default_inform(f"{int(progress * 100)}%")
            return
        target = self._progresses[uid]
        target.progress = progress
        if target.progressbar._mode == "indeterminate":  # noqa: SLF001
            target.progressbar.configure(
                mode="determinate", require_redraw=True
            )
        target.progressbar.set(progress)

    def finish_progress(self, uid: str) -> None:
        """Finish progressbar."""
        if uid not in self._progresses:
            self.default_inform("100%")
            return
        target = self._progresses[uid]
        target.progress = 100
        if target.progressbar._mode == "indeterminate":  # noqa: SLF001
            target.progressbar.configure(
                mode="determinate", require_redraw=True
            )
        target.progressbar.set(1)
