import sys
from typing import Any


def write_out(*args: Any, sep: str = " ") -> None:
    """Print to stdout."""
    sys.stdout.write(sep.join(map(str, args)))
    sys.stdout.flush()


def write_err(*args: Any, sep: str = " ") -> None:
    """Print to stderr."""
    sys.stderr.write(sep.join(map(str, args)))
    sys.stderr.flush()
