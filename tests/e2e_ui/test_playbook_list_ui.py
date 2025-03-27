import os
from subprocess import Popen

from tests.e2e_ui.capture import (
    are_images_similar,
    capture,
    get_ui_fixt,
    use_window,
)


def test_playbook_list():
    """Test that playbook list UI works."""
    Popen(
        "python -m embark",
        shell=True,
        env=os.environ | {
            "UI_LOCALE": "en",
            "UI_LIST_BASE_DIR": "tests/fixtures/test_playbook_list_ui"
        }
    )
    with use_window() as window:
        assert are_images_similar(
            capture(window),
            get_ui_fixt("list_window.png")
        )
