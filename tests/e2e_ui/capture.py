import time
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

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
    rect = window.rectangle()
    return ImageGrab.grab(
        bbox=(
            rect.left + 8, rect.top, rect.right - 8, rect.bottom - 8
        )
    )


@contextmanager
def use_window(
        window_name: str = "Embark UI"
) -> Generator[pywinauto.WindowSpecification]:
    """Wait for window, then close."""
    win = wait_for_win(window_name)
    yield win
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
