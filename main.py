import argparse

from application import Application


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
    args = _get_args()
    app = Application(args.filename, file_encoding=args.encoding)
    app.run()


if __name__ == '__main__':
    main()
