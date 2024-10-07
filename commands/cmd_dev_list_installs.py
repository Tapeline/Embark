"""
dev_list_installs subcommand
"""


# pylint: disable=unused-argument
def command(args):
    """Subcommand impl"""
    # pylint: disable=import-outside-toplevel
    from std.target.install.installs_repo import WindowsInstallsRepository
    repo = WindowsInstallsRepository()
    for i, install in enumerate(repo.get_all_installs()):
        print(f"--- {i + 1} ---")
        print(f"Name:      {install.name}")
        print(f"Version:   {install.version}")
        print(f"Publisher: {install.publisher}")
