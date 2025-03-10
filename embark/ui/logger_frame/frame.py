"""
Logger UI frame
"""

import os
import threading
import tkinter
from tkinter import DISABLED, messagebox

from customtkinter import CTk, CTkButton, CTkFont, CTkFrame, CTkLabel

from embark.impl import action
from embark.impl.task_loader_repo import TaskLoaderRepository
from embark.localization.i18n import L
from embark.platform_impl.windows.os_provider import WindowsInterface
from embark.resources import get_resource
from embark.ui import utils
from embark.ui.debug_frames import exec_frame, vars_frame
from embark.ui.logger_frame.components import GUILoggerFrame
from embark.ui.logger_frame.context_factory import GUIContextFactory


class LoggerFrame(CTk):
    """Main UI frame"""

    def __init__(self, encoding, playbook_path):
        super().__init__()
        self._encoding = encoding
        self._playbook_path = playbook_path
        self.title("Embark UI")
        self.iconbitmap(get_resource("icon.ico"))
        self._font = CTkFont("TkDefaultFont", 16, "bold")
        self._setup_ui()
        self._ctx_factory = GUIContextFactory(
            self._logger_frame, WindowsInterface()
        )
        self._loader_repo = TaskLoaderRepository()
        utils.center(self, 1000, 700)

    def _setup_ui(self):
        """Create and place UI components"""
        self._left_pane = CTkFrame(self)
        self._lp_title = CTkLabel(
            self._left_pane,
            text="Embark",
            font=self._font
        )
        self._lp_subtitle = CTkLabel(
            self._left_pane,
            text=L("UI.running_playbook")
        )
        self._lp_stop_btn = CTkButton(
            self._left_pane,
            text=L("UI.stop_playbook"),
            command=self._stop_playbook_cmd
        )
        self._lp_debug_title = CTkLabel(self._left_pane, text=L("UI.debug"))
        self._lp_debug_vars_btn = CTkButton(
            self._left_pane,
            text=L("UI.debug_vars"),
            command=self._debug_vars_cmd
        )
        self._lp_debug_eval_btn = CTkButton(
            self._left_pane,
            text=L("UI.debug_exec"),
            command=self._debug_eval_cmd
        )
        self._lp_title.pack(side=tkinter.LEFT, padx=12, pady=8, fill="y")
        self._lp_stop_btn.pack(
            side=tkinter.LEFT, padx=12, pady=8, fill="y"
        )
        self._lp_debug_title.pack(
            side=tkinter.LEFT, padx=12, pady=8, fill="y"
        )
        self._lp_debug_vars_btn.pack(
            side=tkinter.LEFT, padx=12, pady=8, fill="y"
        )
        self._lp_debug_eval_btn.pack(
            side=tkinter.LEFT, padx=12, pady=8, fill="y"
        )
        self._lp_copyright = CTkLabel(
            self._left_pane, text="© Tapeline 2024-2025"
        )
        self._lp_copyright.pack(side=tkinter.RIGHT, padx=12, pady=8)

        self._logger_frame = GUILoggerFrame(self)

        self._left_pane.pack(side=tkinter.TOP, fill="x", pady=12, padx=12)
        self._logger_frame.pack(
            side=tkinter.TOP, fill="both", expand=True, pady=12, padx=12
        )
        self.configure(bg_color="#FFFF00")

    def _stop_playbook_cmd(self):
        if messagebox.askyesno(L("UI.ask_title"), L("UI.you_sure_want_exit")):
            self.destroy()

    def _debug_vars_cmd(self):
        if self._logger_frame.playbook is not None:
            vars_frame.show(self._logger_frame.playbook)

    def _debug_eval_cmd(self):
        if self._logger_frame.playbook is not None:
            exec_frame.show(self._logger_frame.playbook)

    def run(self):
        self.after(500, self._start_thread)
        self.mainloop()

    def _start_thread(self):
        self._app_thread = threading.Thread(target=self._launch_app)
        self._app_thread.start()
        self._check_thread()

    def _check_thread(self):
        if self._app_thread.is_alive():
            self.after(100, self._check_thread)
        else:
            self._lp_stop_btn.configure(state=DISABLED)

    def _launch_app(self):
        os.chdir(os.path.dirname(os.path.abspath(self._playbook_path)))
        action.execute_playbook_file(
            self._ctx_factory, self._loader_repo,
            self._playbook_path, self._encoding
        )
