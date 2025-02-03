from pathlib import Path
from typing import Final

from tests.runner import run_embark, remove_after

_COPIED: Final = "tests/fixtures/copied.txt"


def test_copy_task():
    """Test that std.copy works."""
    proc = run_embark("tests/fixtures/test_copy.yml")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    with remove_after(_COPIED):
        assert Path(_COPIED).read_text() == "Hello, World!"


def test_copy_task_overwrite():
    """Test that std.copy with overwrite works."""
    Path("tests/fixtures/copied.txt").write_text("Some text")
    proc = run_embark("tests/fixtures/test_copy_overwrite.yml")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    with remove_after(_COPIED):
        assert Path(_COPIED).read_text() == "Hello, World!"


def test_copy_task_skip_if_missing():
    """Test that std.copy:skip_if_missing works."""
    proc = run_embark("tests/fixtures/test_copy_skip.yml")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
