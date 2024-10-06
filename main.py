"""Main file"""

import logging
import argparse
import time

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


def _configure_arg_parser():
    parser = argparse.ArgumentParser(
        prog="embark",
        description="Embark playbook executor"
    )
    parser.add_argument(
        "filename",
        help="Playbook config"
    )
    parser.add_argument(
        "--encoding",
        default=None,
        help="Config file encoding"
    )
    return parser


def _get_args():
    """Get arguments from argparse"""
    return _configure_arg_parser().parse_args()


def main():
    """Main function"""
    # pylint: disable=import-outside-toplevel
    from application import Application
    args = _get_args()
    app = Application(args.filename, file_encoding=args.encoding)
    app.run()


if __name__ == '__main__':
    main()
    time.sleep(0.5)
    input("Press [ENTER] to close")
