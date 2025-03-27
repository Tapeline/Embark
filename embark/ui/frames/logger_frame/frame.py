"""Logger UI frame."""

import threading
from tkinter import BOTH, DISABLED, LEFT, RIGHT, TOP, X, Y, messagebox
from typing import Final

from customtkinter import CTk, CTkButton, CTkFrame, CTkLabel

from embark.impl import action
from embark.impl.task_loader_repo import TaskLoaderRepository
from embark.localization.i18n import L
from embark.platform_impl.windows.os_provider import WindowsInterface
from embark.resources import get_resource
from embark.ui import utils
from embark.ui.components.playbook_logger import GUIPlaybookLoggerComponent
from embark.ui.constants import (
    COPYRIGHT_TEXT,
    HEADER_FONT,
    MAIN_WIN_SIZE,
    PAD12_8,
)
from embark.ui.frames.debug_frames import exec_frame, vars_frame
from embark.ui.frames.logger_frame.context_factory import GUIContextFactory


class LoggerFrame(CTk):  # noqa: WPS214
    """Main UI frame."""

    _thread_check_timeout: Final = 500

    def __init__(self, encoding: str | None, playbook_path: str) -> None:
        """Create frame."""
        super().__init__()
        self._encoding = encoding
        self._playbook_path = playbook_path
        self.title("Embark UI")
        self.iconbitmap(get_resource("icon.ico"))
        self._ctx_factory: GUIContextFactory | None = None
        self._loader_repo = TaskLoaderRepository()
        utils.center(self, *MAIN_WIN_SIZE)

    def run(self) -> None:
        """Run thread."""
        self._setup_ui()
        self.after(self._thread_check_timeout, self._start_thread)
        self.mainloop()

    def _setup_ui(self) -> None:
        """Create and place UI components."""
        self._left_pane = CTkFrame(self)
        self._lp_title = CTkLabel(
            self._left_pane,
            text="Embark",
            font=HEADER_FONT()
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
        self._lp_title.pack(side=LEFT, fill=Y, **PAD12_8)
        self._lp_stop_btn.pack(side=LEFT, fill=Y, **PAD12_8)
        self._lp_debug_title.pack(side=LEFT, fill=Y, **PAD12_8)
        self._lp_debug_vars_btn.pack(side=LEFT, fill=Y, **PAD12_8)
        self._lp_debug_eval_btn.pack(side=LEFT, fill=Y, **PAD12_8)
        self._lp_copyright = CTkLabel(self._left_pane, text=COPYRIGHT_TEXT)
        self._lp_copyright.pack(side=RIGHT, **PAD12_8)

        self._logger_frame = GUIPlaybookLoggerComponent(self)
        self._ctx_factory = GUIContextFactory(
            self._logger_frame, WindowsInterface()
        )
        self._left_pane.pack(side=TOP, fill=X, **PAD12_8)
        self._logger_frame.pack(
            side=TOP, fill=BOTH, expand=True, **PAD12_8
        )

    def _stop_playbook_cmd(self) -> None:
        if messagebox.askyesno(L("UI.ask_title"), L("UI.you_sure_want_exit")):
            self.destroy()

    def _debug_vars_cmd(self) -> None:
        if self._logger_frame.playbook is not None:
            vars_frame.show(self._logger_frame.playbook)

    def _debug_eval_cmd(self) -> None:
        if self._logger_frame.playbook is not None:
            exec_frame.show(self._logger_frame.playbook)

    def _start_thread(self) -> None:
        self._app_thread = threading.Thread(target=self._launch_app)
        self._app_thread.start()
        self._check_thread()

    def _check_thread(self) -> None:
        if self._app_thread.is_alive():
            self.after(100, self._check_thread)
        else:
            self._lp_stop_btn.configure(state=DISABLED)

    def _launch_app(self) -> None:
        if self._ctx_factory is None:
            raise AssertionError("Context factory not created")
        action.execute_playbook_file(
            self._ctx_factory, self._loader_repo,
            self._playbook_path, self._encoding
        )
