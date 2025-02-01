"""dev_list_installs subcommand."""
from embark.output import write_out
from embark.std.target.install.installs_repo import WindowsInstallsRepository


def command(args):
    """Subcommand impl."""
    repo = WindowsInstallsRepository()
    for index, install in enumerate(repo.get_all_installs()):
        write_out(f"--- {index + 1} ---")
        write_out(f"Name:      {install.name}")
        write_out(f"Version:   {install.version}")
        write_out(f"Publisher: {install.publisher}")
