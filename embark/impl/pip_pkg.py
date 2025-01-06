"""Provides functions for interaction with pip."""

try:
    from pip import main as pip_main
except ImportError:
    from pip._internal import main as pip_main  # noqa


def install_requirements(req_file_path: str) -> int:
    """Install requirements with pip."""
    return pip_main(["install", "-r", req_file_path])
