"""
run subcommand
"""

import time


def command(args):
    """Subcommand impl"""
    # pylint: disable=import-outside-toplevel
    from embark.application import Application
    app = Application(args.filename, file_encoding=args.encoding)
    app.run()
    time.sleep(0.5)
    input("Press [ENTER] to close")
