"""Variables debug UI frame."""

from typing import Final

from customtkinter import CTk, CTkFont, CTkLabel, CTkScrollableFrame

from embark.domain.execution.playbook import Playbook
from embark.localization.i18n import L
from embark.resources import get_resource
from embark.ui import utils
from embark.ui.constants import UTIL_WIN_SIZE

_FONT_SIZE: Final = 14


class DebugVariablesFrame(CTk):
    """Main UI frame."""

    def __init__(self, playbook: Playbook) -> None:
        """Create frame."""
        super().__init__()
        self._playbook = playbook
        self.title(L("UI.debug_vars"))
        self.resizable(width=False, height=False)
        self.iconbitmap(get_resource("icon.ico"))
        self._font = CTkFont("Consolas", _FONT_SIZE, "normal")
        self._setup_ui()
        utils.center(self, *UTIL_WIN_SIZE)

    def _setup_ui(self) -> None:  # noqa: WPS210
        """Create and place UI components."""
        variables = self._playbook.variables.vars.items()
        envs = self._playbook.variables.envs.items()
        self._scrollable1 = CTkScrollableFrame(self)
        self._scrollable = CTkScrollableFrame(
            self._scrollable1,
            orientation="horizontal"
        )
        for index in range(len(variables) + len(envs) + 2):
            self._scrollable.rowconfigure(index=index, weight=1)
        self._scrollable.columnconfigure(index=0, weight=1)
        self._scrollable.columnconfigure(index=1, weight=1)
        self._vars_title = CTkLabel(
            self._scrollable,
            text=L("UI.debug_vars_section")
        )
        self._envs_title = CTkLabel(
            self._scrollable,
            text=L("UI.debug_envs_section")
        )
        self._vars_title.grid(row=0, column=0, columnspan=2, sticky="nw")
        row = 1
        for var, val in variables:
            var_label = CTkLabel(self._scrollable, text=var, font=self._font)
            val_label = CTkLabel(self._scrollable, text=val, font=self._font)
            var_label.grid(row=row, column=0, sticky="nw")
            val_label.grid(row=row, column=1, sticky="nw", padx=4)
            row += 1
        self._scrollable.pack(fill="both", expand=True)
        self._scrollable1.pack(fill="both", expand=True)


def show(playbook: Playbook) -> None:
    """Show vars frame."""
    win = DebugVariablesFrame(playbook)
    win.mainloop()
