"""
Main UI file
"""

from embark.commands import cmd_run
from embark.ui import main_frame


DEFAULT_ENCODING = "UTF-8"


class ArgsMock:
    """Mocks argparse arg object"""
    # pylint: disable=too-few-public-methods
    filename: str
    encoding: str = DEFAULT_ENCODING


def main():
    """Main UI function"""
    args = ArgsMock()
    args.filename = main_frame.ask_for_playbook(args.encoding)
    if args.filename is None:
        return
    cmd_run.command(args)
