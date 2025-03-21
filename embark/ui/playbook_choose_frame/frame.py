"""
Main UI frame and tools
"""

import os

import yaml
from customtkinter import CTk, CTkButton, CTkFont, CTkLabel

from embark.localization.i18n import L
from embark.resources import get_resource
from embark.ui import utils


class PlaybookChooseFrame(CTk):
    """Main UI frame"""

    def __init__(self, encoding):
        super().__init__()
        self.title("Embark UI")
        self.resizable(width=False, height=False)
        self.iconbitmap(get_resource("icon.ico"))
        self._font = CTkFont("TkDefaultFont", 16, "bold")
        self._controller = Controller(encoding)
        self._setup_ui()
        self._selected_file = None
        utils.center(self, 600, 600)

    def _setup_ui(self):
        """Create and place UI components"""
        self._label1 = CTkLabel(
            self, anchor="w",
            text=L("UI.playbooks_found_title")
        )
        self._label1.configure(font=self._font)
        self._label1.grid(
            row=0,
            column=0,
            padx=(16, 16),
            pady=(16, 0),
            sticky="w"
        )
        self._label2 = CTkLabel(
            self,
            text=L("UI.playbooks_found_subtitle"),
            anchor="w"
        )
        self._label2.grid(
            row=1,
            column=0,
            padx=(16, 16),
            pady=(0, 16),
            sticky="w"
        )
        playbooks = self._controller.get_playbooks()
        if len(playbooks) == 0:
            self._404_label = CTkLabel(
                self,
                text=L("UI.playbooks_not_found"),
                anchor="w"
            )
            self._404_label.grid(
                row=2,
                column=0,
                padx=(16, 16),
                pady=(16, 16),
                sticky="w"
            )
            return
        row = 2
        self._buttons = []
        for file, name in playbooks.items():
            button = CTkButton(
                self, text=name,
                command=lambda *_, f=file: self._choose_playbook(f)
            )
            button.grid(row=row, column=0, padx=(16, 16), pady=8, sticky="we")
            button.configure(font=self._font, width=50)
            self._buttons.append(button)
            row += 1

    def _choose_playbook(self, filename):
        """Set desired playbook file and exit"""
        self._selected_file = filename
        self.destroy()

    def get_selected_file(self) -> str | None:
        # pylint: disable=missing-function-docstring
        return self._selected_file


class Controller:
    """Main frame controller"""

    # pylint: disable=too-few-public-methods
    def __init__(self, encoding, base_dir=""):
        self._base_dir = os.path.abspath(base_dir)
        self._encoding = encoding

    def get_playbooks(self) -> dict[str, str]:
        # pylint: disable=missing-function-docstring
        playbooks = {}
        for filename in os.listdir(self._base_dir):
            if not filename.endswith(".yml"):
                continue
            try:
                playbook = os.path.join(self._base_dir, filename)
                with open(playbook, encoding=self._encoding) as f:
                    data = yaml.safe_load(f.read())
                    if "name" in data:
                        playbooks[playbook] = data["name"]
            except yaml.YAMLError:
                continue
        return playbooks


def ask_for_playbook(encoding) -> str | None:
    """Open window and ask user for playbook"""
    frame = PlaybookChooseFrame(encoding)
    frame.mainloop()
    return frame.get_selected_file()
