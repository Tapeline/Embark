import os
from subprocess import Popen

from tests.e2e.ui.capture import (
    are_images_similar,
    capture,
    get_ui_fixt,
    use_window,
)


def test_playbook_run():
    """Test that playbook run UI works."""
    Popen(
        "python -m tests.e2e.ui.run_test_echo_ui",
        shell=True,
        env=os.environ | {
            "UI_LOCALE": "en"
        }
    )
    with use_window(extend_delay=2) as window:
        win_cap = capture(window)
        win_cap.save("tests/captured/run.png")
        assert are_images_similar(
            win_cap,
            get_ui_fixt("runner.png")
        )
