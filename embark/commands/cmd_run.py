"""run subcommand."""

import time

from embark.application import Application


def command(args):
    """Subcommand impl"""
    app = Application(args.filename, file_encoding=args.encoding)
    app.run()
    time.sleep(0.5)
    input("Press [ENTER] to close")  # noqa: WPS421
