"""Main UI frame and tools."""

import os
from contextlib import suppress
from functools import partial
from pathlib import Path
from tkinter import EW, W
from typing import Final

import yaml
from customtkinter import CTk, CTkButton, CTkLabel

from embark.localization.i18n import L
from embark.resources import get_resource
from embark.ui import utils
from embark.ui.constants import HEADER_FONT, PAD16, UTIL_WIN_SIZE


class PlaybookChooseFrame(CTk):
    """Main UI frame."""

    _gap: Final = 16

    def __init__(self, encoding: str | None) -> None:
        """Create frame."""
        super().__init__()
        self.title("Embark UI")
        self.resizable(width=False, height=False)
        self.iconbitmap(get_resource("icon.ico"))
        self._controller = Controller(encoding)
        self._setup_ui()
        self._selected_file: str | None = None
        utils.center(self, *UTIL_WIN_SIZE)

    @property
    def selected_file(self) -> str | None:
        """Get selected file."""
        return self._selected_file

    def _setup_ui(self) -> None:
        """Create and place UI components."""
        self.columnconfigure(index=0, weight=1)
        self._label1 = CTkLabel(
            self, anchor=W,
            text=L("UI.playbooks_found_title")
        )
        self._label1.configure(font=HEADER_FONT())
        self._label1.grid(
            row=0,
            column=0,
            padx=self._gap,
            pady=(self._gap, 0),
            sticky=W
        )
        self._label2 = CTkLabel(
            self,
            text=L("UI.playbooks_found_subtitle"),
            anchor=W
        )
        self._label2.grid(
            row=1,
            column=0,
            padx=self._gap,
            pady=(0, self._gap),
            sticky=W
        )
        playbooks = self._controller.scan_playbooks()
        if len(playbooks) == 0:
            self._404_label = CTkLabel(
                self,
                text=L("UI.playbooks_not_found"),
                anchor=W
            )
            self._404_label.grid(
                row=2,
                column=0,
                sticky=W,
                **PAD16
            )
            return
        row = 2
        self._buttons = []
        for filename, name in playbooks.items():
            button = CTkButton(
                self, text=name,
                command=partial(self._choose_playbook, filename)
            )
            button.grid(
                row=row,
                column=0,
                padx=self._gap,
                pady=self._gap // 2,
                sticky=EW
            )
            button.configure(font=HEADER_FONT())
            self._buttons.append(button)
            row += 1

    def _choose_playbook(self, filename: str) -> None:
        """Set desired playbook file and exit."""
        self._selected_file = filename
        self.destroy()


class Controller:
    """Main frame controller."""

    def __init__(self, encoding: str | None) -> None:
        """Create controller."""
        base_dir = os.environ.get("UI_LIST_BASE_DIR") or ""
        self._base_dir = os.path.abspath(base_dir)
        self._encoding = encoding

    def scan_playbooks(self) -> dict[str, str]:
        """Scan for playbooks."""
        playbooks: dict[str, str] = {}
        for filename in os.listdir(self._base_dir):
            if not filename.endswith(".yml"):
                continue
            self._try_add_playbook(filename, playbooks)
        return playbooks

    def _try_add_playbook(
            self,
            filename: str,
            playbooks: dict[str, str]
    ) -> None:
        with suppress(yaml.YAMLError):
            playbook = Path(self._base_dir, filename)
            config_obj = yaml.safe_load(playbook.read_text())
            if "name" in config_obj and "tasks" in config_obj:  # noqa: WPS529
                playbooks[str(playbook)] = config_obj["name"]


def ask_for_playbook(encoding: str | None) -> str | None:
    """Open window and ask user for playbook."""
    frame = PlaybookChooseFrame(encoding)
    frame.mainloop()
    return frame.selected_file
