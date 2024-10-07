"""
dev_query_install subcommand
"""
import re


def command(args):
    """Subcommand impl"""
    # pylint: disable=import-outside-toplevel
    from std.target.install.installs_repo import WindowsInstallsRepository
    repo = WindowsInstallsRepository()
    for install in repo.get_all_installs():
        if (re.fullmatch(args.name, install.name) is not None
                and (install.publisher == args.publisher or install.publisher is None) and
                (install.version == args.version or args.ignore_version)):
            print(f"Name:      {install.name}")
            print(f"Version:   {install.version}")
            print(f"Publisher: {install.publisher}")
            return
