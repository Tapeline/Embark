from pathlib import Path
from typing import Final

from tests.runner import remove_after, run_embark

_TARGET: Final = "tests/fixtures/custom_task.out"


def test_custom_task():
    """Test that custom tasks are working properly."""
    proc = run_embark("tests/fixtures/test_custom_task.yml")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    with remove_after(_TARGET):
        assert Path(_TARGET).read_text() == "Hello, World!"
