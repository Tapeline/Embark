"""Main UI file."""
import os

import customtkinter

from embark.ui.frames.logger_frame.frame import LoggerFrame
from embark.ui.playbook_choose_frame.frame import ask_for_playbook

DEFAULT_ENCODING = "UTF-8"


class ArgsMock:
    """Mocks argparse arg object."""

    filename: str
    encoding: str = DEFAULT_ENCODING


def main() -> None:
    """UI entrypoint."""
    customtkinter.set_appearance_mode(
        os.environ.get("UI_THEME") or "system"
    )
    playbook_path = ask_for_playbook(DEFAULT_ENCODING)
    if playbook_path is None:
        return
    logger_frame = LoggerFrame(DEFAULT_ENCODING, playbook_path)
    logger_frame.run()
