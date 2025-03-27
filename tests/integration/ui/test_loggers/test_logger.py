import os
from subprocess import Popen

from tests.e2e.ui.capture import (
    are_images_similar,
    capture,
    get_ui_fixt,
    use_window,
)


def test_ui_logger():
    """Ensure UI logger is rendered properly."""
    Popen(
        "python -m tests.integration.ui.test_loggers.logger_test_window",
        shell=True,
        env=os.environ | {
            "UI_LOCALE": "en",
            "UI_THEME": "light"
        }
    )
    with use_window("Logger test", extend_delay=1.5) as window:
        assert are_images_similar(
            capture(window),
            get_ui_fixt("loggers.png")
        )
