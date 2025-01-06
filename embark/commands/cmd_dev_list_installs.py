"""dev_list_installs subcommand."""

from embark.std.target.install.installs_repo import WindowsInstallsRepository


def command(args):
    """Subcommand impl."""
    repo = WindowsInstallsRepository()
    for i, install in enumerate(repo.get_all_installs()):
        print(f"--- {i + 1} ---")
        print(f"Name:      {install.name}")
        print(f"Version:   {install.version}")
        print(f"Publisher: {install.publisher}")
