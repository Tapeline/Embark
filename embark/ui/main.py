"""
Main UI file
"""

from embark.commands import cmd_run
from embark.ui import main_frame
from embark.ui.logger_frame.frame import LoggerFrame

DEFAULT_ENCODING = "UTF-8"


class ArgsMock:
    """Mocks argparse arg object"""
    # pylint: disable=too-few-public-methods
    filename: str
    encoding: str = DEFAULT_ENCODING


def _main():
    """Main UI function"""
    args = ArgsMock()
    args.filename = main_frame.ask_for_playbook(DEFAULT_ENCODING)
    if args.filename is None:
        return
    cmd_run.command(args)


def main():
    playbook_path = main_frame.ask_for_playbook(DEFAULT_ENCODING)
    logger_frame = LoggerFrame(DEFAULT_ENCODING, playbook_path)
    logger_frame.run()
