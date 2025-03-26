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
    report: bool = False


class RunCommand(AbstractCommand[RunCommandArgs]):
    """run command."""

    _args_type = RunCommandArgs

    def _run(self, args: RunCommandArgs) -> int:
        """Subcommand impl."""
        app = Application(
            self.os_interface, args.filename, file_encoding=args.encoding
        )
        exit_code = app.run(save_report=args.report)
        time.sleep(0.5)
        return exit_code
