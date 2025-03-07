"""dev_list_installs subcommand."""
from embark.output import write_out
from embark.platform_impl.windows.os_provider import WindowsInterface


def command(args):
    """Subcommand impl."""
    repo = WindowsInterface().get_install_interface()
    for index, install in enumerate(repo.get_all_installs()):
        write_out(f"--- {index + 1} ---")
        write_out(f"Name:      {install.name}")
        write_out(f"Version:   {install.version}")
        write_out(f"Publisher: {install.publisher}")
