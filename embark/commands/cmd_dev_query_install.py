"""dev_query_install subcommand."""

from typing import final

from attrs import frozen

from embark.commands.base import AbstractCommand
from embark.output import write_out


@final
@frozen
class DevQueryInstallCommandArgs:
    """Arguments for dev_query_install command."""

    name: str
    publisher: str
    version: str
    ignore_version: bool = False


class DevQueryInstallCommand(AbstractCommand[DevQueryInstallCommandArgs]):
    """dev_query_install command."""

    _args_type = DevQueryInstallCommandArgs

    def _run(self, args: DevQueryInstallCommandArgs) -> int:
        """Subcommand impl."""
        repo = self.os_interface.get_install_interface()
        for install in repo.get_all_installs():
            if install.matches(
                args.name,
                args.publisher,
                args.version,
                ignore_version=args.ignore_version
            ):
                write_out(f"Name:      {install.name}")
                write_out(f"Version:   {install.version}")
                write_out(f"Publisher: {install.publisher}")
        return 0
