import os
import sys
import time
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from subprocess import Popen

import imagehash
import pywinauto
from PIL import Image, ImageGrab
from PIL.ImageFile import ImageFile


def wait_for_win(
        window_name: str = "Embark UI"
) -> pywinauto.WindowSpecification:
    """Wait for window to be visible."""
    win = pywinauto.Desktop(backend="win32")[window_name]
    win.wait("visible")
    time.sleep(0.5)
    return win


def capture(window: pywinauto.WindowSpecification) -> Image:
    """Screenshot the window."""
    return ImageGrab.grab(bbox=_clean_win_rect(window))


def _clean_win_rect(
        window: pywinauto.WindowSpecification
) -> tuple[int, int, int, int]:
    rect = window.rectangle()
    return (
        rect.left + 8,    # crop pywinauto margin
        rect.top + 32,    # crop windows titlebar
        rect.right - 8,   # crop pywinauto margin
        rect.bottom - 8,  # crop pywinauto margin
    )


@contextmanager
def use_window(
        window_name: str = "Embark UI",
        extend_delay: float = 0.0
) -> Generator[pywinauto.WindowSpecification]:
    """Wait for window, then close."""
    win = wait_for_win(window_name)
    time.sleep(extend_delay)
    try:
        yield win
    finally:
        win.close()


def are_images_similar(
        image_a: Image,
        image_b: Image,
        cutoff: int = 5
) -> bool:
    """Check that images are ≈similar."""
    hash0 = imagehash.average_hash(image_a)
    hash1 = imagehash.average_hash(image_b)
    return hash0 - hash1 < cutoff


def get_ui_fixt(name: str) -> ImageFile:
    """Get UI fixture file."""
    return Image.open(Path("tests", "fixtures", "ui_screenshots", name))


def _main():  # pragma: no cover
    """Util func for generating new screenshots."""
    Popen(
        f"python -m {sys.argv[1]}",
        shell=True,
        env=os.environ | {
            "UI_LOCALE": "en",
            "UI_THEME": "light"
        }
    )
    ext_delay = 1.5
    if len(sys.argv) == 5:
        ext_delay = float(sys.argv[4])
    with use_window(sys.argv[2], extend_delay=ext_delay) as window:
        capture(window).save(sys.argv[3])


if __name__ == '__main__':  # pragma: no cover
    _main()
