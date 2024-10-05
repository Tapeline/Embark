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


def _configure_arg_parser():
    parser = argparse.ArgumentParser(
        prog="Embark CLI",
        description="Embark playbook executor"
    )
    parser.add_argument("filename")
    parser.add_argument("--encoding", default=None)
    return parser


def _get_args():
    return _configure_arg_parser().parse_args()


def main():
    from application import Application
    args = _get_args()
    app = Application(args.filename, file_encoding=args.encoding)
    app.run()


if __name__ == '__main__':
    main()
