"""Main file"""

import logging
import argparse
import os
import sys

from embark import log_config
from embark.ui import main as ui_main

logging.basicConfig(level=logging.INFO)
log_config.setup_default_handlers(logging.getLogger())

# cannot put imports before logging config
from embark.commands import (  # noqa: E402 (import not on top)
    cmd_run,
    cmd_dev_list_installs,
    cmd_dev_query_install
)


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
    parser_run.set_defaults(func=cmd_run.command)

    parser_dev_list_installs = sub_parsers.add_parser(
        "dev_list_installs",
        aliases=("dli",),
        help="List all installations exactly as Embark sees them"
    )
    parser_dev_list_installs.set_defaults(func=cmd_dev_list_installs.command)

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
    parser_dev_query_install.set_defaults(func=cmd_dev_query_install.command)
    return parser


def main():
    """Main function"""
    if len(sys.argv) == 1:
        ui_main.main()
    else:
        args = _configure_arg_parser().parse_args()
        args.func(args)


if __name__ == '__main__':
    main()
