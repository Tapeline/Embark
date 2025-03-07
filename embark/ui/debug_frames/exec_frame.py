"""Eval debug UI frame"""
from typing import Final

from customtkinter import CTk, CTkButton, CTkFont, CTkTextbox

from embark.domain.execution.playbook import Playbook
from embark.localization.i18n import L
from embark.resources import get_resource
from embark.ui import utils

_FONT_SIZE: Final = 14


class DebugExecFrame(CTk):
    """Main UI frame."""

    def __init__(self, playbook: Playbook):
        super().__init__()
        self._playbook = playbook
        self.title(L("UI.debug_exec"))
        self.geometry("500x600")
        self.resizable(width=False, height=False)
        self.iconbitmap(get_resource("icon.ico"))
        utils.center(self)
        self._font = CTkFont("Consolas", _FONT_SIZE, "normal")
        self._setup_ui()

    def _setup_ui(self):
        """Create and place UI components"""
        self._cmd = CTkTextbox(self, font=self._font)
        self._execute_btn = CTkButton(
            self,
            text=L("UI.execute_expression"),
            command=self._exec
        )
        self._result_box = CTkTextbox(self, font=self._font)
        self._cmd.pack(anchor="nw", padx=4, pady=4, fill="both", expand=True)
        self._execute_btn.pack(anchor="nw", padx=4, pady=4, fill="x")
        self._result_box.pack(
            anchor="nw",
            padx=4,
            pady=4,
            fill="both",
            expand=True
        )

    def _log(self, *args):
        self._result_box.insert("end", " ".join(map(str, args)) + "\n")

    def _exec(self):
        exec(  # noqa: WPS421, S102
            self._cmd.get("0.0", "end"),
            {
                "playbook": self._playbook,
                "print": self._log
            }
        )


def show(playbook):
    win = DebugExecFrame(playbook)
    win.mainloop()
