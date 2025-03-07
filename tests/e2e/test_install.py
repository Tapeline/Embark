from pathlib import Path
from typing import Final

from tests.runner import run_embark, run_after

_INSTALLED: Final = "C:\\embark_test\\BlankInnoSetupProgram\\test.txt"


def test_inno_setup():
    """Test that std.install with inno works."""
    proc = run_embark("tests/fixtures/test_install_innosetup.yml")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert Path(_INSTALLED).read_text() == "this is an executable"
