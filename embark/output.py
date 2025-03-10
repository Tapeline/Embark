import sys
from typing import Any

_stdout = sys.stdout
_stderr = sys.stderr


def write_out(*args: Any, sep: str = " ") -> None:
    """Print to stdout."""
    _stdout.write(sep.join(map(str, args)))
    _stdout.write("\n")
    _stdout.flush()


def write_err(*args: Any, sep: str = " ") -> None:
    """Print to stderr."""
    _stderr.write(sep.join(map(str, args)))
    _stderr.write("\n")
    _stderr.flush()
