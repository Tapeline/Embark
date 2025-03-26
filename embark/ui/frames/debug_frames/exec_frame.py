"""Eval debug UI frame."""

from tkinter import messagebox
from typing import Any, Final

from customtkinter import CTk, CTkButton, CTkTextbox

from embark.domain.execution.playbook import Playbook
from embark.localization.i18n import L
from embark.resources import get_resource
from embark.ui import utils
from embark.ui.constants import CONSOLE_FONT, PAD4, UTIL_WIN_SIZE

_FONT_SIZE: Final = 14


class DebugExecFrame(CTk):
    """Main UI frame."""

    def __init__(self, playbook: Playbook) -> None:
        """Create frame."""
        super().__init__()
        self._playbook = playbook
        self.title(L("UI.debug_exec"))
        self.resizable(width=False, height=False)
        self.iconbitmap(get_resource("icon.ico"))
        self._setup_ui()
        utils.center(self, *UTIL_WIN_SIZE)

    def _setup_ui(self) -> None:
        """Create and place UI components."""
        self._cmd = CTkTextbox(self, font=CONSOLE_FONT())
        self._execute_btn = CTkButton(
            self,
            text=L("UI.execute_expression"),
            command=self._exec
        )
        self._result_box = CTkTextbox(self, font=CONSOLE_FONT())
        self._cmd.pack(anchor="nw", fill="both", expand=True, **PAD4)
        self._execute_btn.pack(anchor="nw", fill="x", **PAD4)
        self._result_box.pack(
            anchor="nw",
            fill="both",
            expand=True,
            **PAD4
        )

    def _log(self, *args: Any) -> None:
        self._result_box.insert(
            "end",
            " ".join(map(str, args))
        )
        self._result_box.insert("end", "\n")

    def _exec(self) -> None:
        try:
            exec(  # noqa: WPS421, S102
                self._cmd.get("0.0", "end"),
                {
                    "playbook": self._playbook,
                    "print": self._log
                }
            )
        except Exception as exc:
            messagebox.showerror(
                "Error occurred",
                str(exc)
            )


def show(playbook: Playbook) -> None:
    """Show exec frame."""
    win = DebugExecFrame(playbook)
    win.mainloop()
