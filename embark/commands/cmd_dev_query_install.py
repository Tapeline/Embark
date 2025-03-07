"""dev_query_install subcommand."""

from embark.output import write_out
from embark.platform_impl.windows.os_provider import WindowsInterface


def command(args):
    """Subcommand impl"""
    repo = WindowsInterface().get_install_interface()
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
            return
