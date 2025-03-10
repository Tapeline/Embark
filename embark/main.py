"""Main file"""

import argparse
import logging
import sys

from embark import log_config
from embark.ui import main as ui_main

logging.basicConfig(level=logging.INFO)
log_config.setup_default_handlers(logging.getLogger())

# cannot put imports before logging config
from embark.commands.cmd_dev_list_installs import DevListInstallsCommand
from embark.commands.cmd_dev_query_install import DevQueryInstallCommand
from embark.commands.cmd_run import RunCommand
from embark.platform_impl.windows.os_provider import WindowsInterface


os_interface = WindowsInterface()


def _configure_arg_parser():  # noqa: WPS213 (too many expressions)
    """Configures CLI arguments and subcommands"""
    parser = argparse.ArgumentParser(
        prog="embark",
        description="Embark playbook executor"
    )
    sub_parsers = parser.add_subparsers(help="sub-command help")

    parser_run = sub_parsers.add_parser("run", help="Run playbook")
    parser_run.add_argument(
        "filename",
        help="Playbook config"
    )
    parser_run.add_argument(
        "--encoding",
        default=None,
        help="Config file encoding"
    )
    parser_run.set_defaults(func=RunCommand(os_interface))

    parser_dev_list_installs = sub_parsers.add_parser(
        "dev_list_installs",
        aliases=("dli",),
        help="List all installations exactly as Embark sees them"
    )
    parser_dev_list_installs.set_defaults(
        func=DevListInstallsCommand(os_interface)
    )

    parser_dev_query_install = sub_parsers.add_parser(
        "dev_query_install",
        aliases=("dqi",),
        help="Get installation"
    )
    parser_dev_query_install.add_argument(
        "name",
        help="Program name"
    )
    parser_dev_query_install.add_argument(
        "--publisher",
        help="Program publisher",
        default=None
    )
    parser_dev_query_install.add_argument(
        "--version",
        help="Program version",
        default=None
    )
    parser_dev_query_install.add_argument(
        "--ignore-version",
        action="store_true",
        help="Accept any version",
        default=False
    )
    parser_dev_query_install.set_defaults(
        func=DevQueryInstallCommand(os_interface)
    )
    return parser


def main():
    """Main function"""
    if len(sys.argv) == 1:
        ui_main.main()
    else:
        args = _configure_arg_parser().parse_args()
        args.func(args)


if __name__ == "__main__":
    main()
