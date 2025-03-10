from pathlib import Path
from typing import Final

from tests.runner import remove_after, run_embark

_TARGET: Final = "tests/fixtures/cmd.out"


def test_cmd():
    """Test that ``std.cmd`` is working properly."""
    proc = run_embark("tests/fixtures/test_cmd.yml")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    with remove_after(_TARGET):
        assert Path(_TARGET).read_text().strip() == "Hello, World!"
