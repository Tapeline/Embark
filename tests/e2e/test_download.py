from pathlib import Path
from typing import Final

from tests.runner import remove_after, run_embark
from tests.server import serve_fixture_files

_TARGET: Final = "tests/fixtures/gpl3.txt"
_ORIGINAL: Final = "tests/fixtures/gpl-3.0-original.txt"


def test_download_task(serve_fixture_files):
    """Test that std.download works."""
    proc = run_embark("tests/fixtures/test_download.yml")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    with remove_after(_TARGET):
        assert Path(_TARGET).read_text() == Path(_ORIGINAL).read_text()


def test_download_task_overwrite(serve_fixture_files):
    """Test that std.download with overwrite works."""
    Path(_TARGET).write_text("Some text")
    proc = run_embark("tests/fixtures/test_download_overwrite.yml")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    with remove_after(_TARGET):
        assert Path(_TARGET).read_text() == Path(_ORIGINAL).read_text()
