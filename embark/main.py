"""Main file"""

import logging
import argparse

logging.basicConfig(level=logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s %(name)-30s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
ch.setFormatter(formatter)
for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
logging.getLogger().addHandler(ch)

# cannot put imports before logging config
# pylint: disable=wrong-import-position
from .commands import cmd_run, cmd_dev_list_installs, cmd_dev_query_install


def _configure_arg_parser():
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
    args = _configure_arg_parser().parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
