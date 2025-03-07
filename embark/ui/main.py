"""Main UI file."""

from embark.ui.logger_frame.frame import LoggerFrame
from embark.ui.playbook_choose_frame.frame import ask_for_playbook

DEFAULT_ENCODING = "UTF-8"


class ArgsMock:
    """Mocks argparse arg object"""

    filename: str
    encoding: str = DEFAULT_ENCODING


def main():
    playbook_path = ask_for_playbook(DEFAULT_ENCODING)
    if playbook_path is None:
        return
    logger_frame = LoggerFrame(DEFAULT_ENCODING, playbook_path)
    logger_frame.run()
