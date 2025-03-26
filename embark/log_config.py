"""Default log configs."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import Handler, Logger


def get_default_handler() -> "Handler":
    """Default stdout handler config."""
    # pylint: disable=import-outside-toplevel
    import logging
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s %(name)-30s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    ch.setFormatter(formatter)
    return ch


def get_file_handler() -> "Handler":
    """Default file handler config."""
    # pylint: disable=import-outside-toplevel
    import logging
    ch = logging.FileHandler("embark.log")
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s %(name)-30s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    ch.setFormatter(formatter)
    return ch


def setup_default_handlers(logger: "Logger") -> None:
    """Clear old handlers and add default."""
    ch = get_default_handler()
    for logging_handler in logger.handlers:
        logger.removeHandler(logging_handler)
    logger.addHandler(ch)
    logger.addHandler(get_file_handler())
    logger.parent = None
