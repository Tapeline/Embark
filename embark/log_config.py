"""Default log configs"""


def get_default_handler():
    """Default stdout handler config"""
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


def setup_default_handlers(logger):
    """Clear old handlers and add default"""
    ch = get_default_handler()
    for handler in logger.handlers:
        logger.removeHandler(handler)
    logger.addHandler(ch)
    logger.parent = None
