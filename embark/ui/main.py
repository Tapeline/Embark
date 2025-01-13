"""
Main UI file
"""
from embark.application import Application
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
    app = Application(args.filename, file_encoding=args.encoding)
    app.run()
