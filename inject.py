import inspect
from contextlib import contextmanager
from typing import Any


@contextmanager
def inject(*names: dict[str, Any]) -> None:
    frame = inspect.currentframe()
    upper_frame = inspect.getouterframes(frame)[2].frame
    backup = upper_frame.f_locals.copy()
    for name_dict in names:
        upper_frame.f_locals.update(name_dict)
    yield
    upper_frame.f_locals.clear()
    upper_frame.f_locals.update(backup)
