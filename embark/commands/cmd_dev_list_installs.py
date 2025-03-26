"""dev_list_installs subcommand."""

from embark.commands.base import AbstractCommand, NoArgs
from embark.output import write_out


class DevListInstallsCommand(AbstractCommand[NoArgs]):
    """dev_list_installs command."""

    _args_type = NoArgs

    def _run(self, args: NoArgs) -> int:
        """Subcommand impl."""
        repo = self.os_interface.get_install_interface()
        for index, install in enumerate(repo.get_all_installs()):
            write_out(f"--- {index + 1} ---")
            write_out(f"Name:      {install.name}")
            write_out(f"Version:   {install.version}")
            write_out(f"Publisher: {install.publisher}")
        return 0
