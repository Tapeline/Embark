import tkinter
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from customtkinter import CTkLabel

from embark.ui.constants import LOG_FONT

test_mode: bool = False  # do not insert time so tests are reproducible


def log_format(message: str, *args: Any) -> str:
    """Format log message."""
    if not args:  # pragma: no cover
        args = ()
    if test_mode:  # pragma: no cover
        return message % args
    try:
        return (  # pragma: no cover
                "[" +
                datetime.now().strftime("%H:%M:%S") +
                "] " +
                message % args
        )
    except TypeError:
        return (  # pragma: no cover
                "[" +
                datetime.now().strftime("%H:%M:%S") +
                "] " +
                message % args
        )


class LogMessageComponent(CTkLabel):
    """Component containing log message."""

    def __init__(
            self,
            root: tkinter.Widget,
            log_level: str,
            message: str
    ) -> None:
        """Create component."""
        if log_level == "info":
            message = f"ⓘ {message}"
        if log_level == "warning":
            message = f"! {message}"
        if log_level in {"error", "exception"}:
            message = f"X {message}"
        super().__init__(
            root,
            text=message,
            font=LOG_FONT(),
            anchor="nw",
            justify="left"
        )


class AbstractLoggerFrame(ABC):
    """ABC for log frames."""

    def inform(self, message: str, *args: Any) -> None:
        """Log info."""
        self.log("info", message, *args)

    def warning(self, message: str, *args: Any) -> None:
        """Log warning."""
        self.log("warning", message, *args)

    def error(self, message: str, *args: Any) -> None:
        """Log error."""
        self.log("error", message, *args)

    def exception(self, message: str, *args: Any) -> None:
        """Log exception."""
        self.log("exception", message, *args)

    @abstractmethod
    def log(self, level: str, message: str, *args: Any) -> None:
        """Basic log function."""
