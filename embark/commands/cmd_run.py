"""run subcommand."""

import time
from typing import final

from attrs import frozen

from embark.application import Application
from embark.commands.base import AbstractCommand


@final
@frozen
class RunCommandArgs:
    """Arguments for run command."""

    filename: str
    encoding: str | None = None


class RunCommand(AbstractCommand[RunCommandArgs]):
    _args_type = RunCommandArgs

    def _run(self, args: RunCommandArgs) -> int:
        """Subcommand impl."""
        app = Application(
            self.os_interface, args.filename, file_encoding=args.encoding
        )
        exit_code = app.run()
        time.sleep(0.5)
        return exit_code
