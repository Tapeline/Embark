"""dev_query_install subcommand."""

from embark.output import write_out
from embark.std.target.install.installs_repo import WindowsInstallsRepository


def command(args):
    """Subcommand impl"""
    repo = WindowsInstallsRepository()
    for install in repo.get_all_installs():
        if install.matches(
            args.name,
            args.publisher,
            args.version,
            args.ignore_version
        ):
            write_out(f"Name:      {install.name}")
            write_out(f"Version:   {install.version}")
            write_out(f"Publisher: {install.publisher}")
            return
