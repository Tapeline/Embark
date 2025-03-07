from pathlib import Path
from typing import Final

from tests.runner import run_after, run_embark

_INSTALLED_INNO: Final = r"C:\Program Files\BlankInnoSetupProgram\{0}"
_INSTALLED_INNOx86: Final = (
    r"C:\Program Files (x86)\BlankInnoSetupProgram\{0}"
)


def _read_one_of(*paths: str) -> str:
    for path in paths:
        if Path(path).exists():
            return Path(path).read_text()
    raise FileNotFoundError(paths)


def _read_any_prog_file(filename: str) -> str:
    return _read_one_of(
        _INSTALLED_INNO.format(filename),
        _INSTALLED_INNOx86.format(filename),
    )


def test_inno_setup():
    """Test that std.install with inno works."""
    proc = run_embark("tests/fixtures/test_install_innosetup.yml")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    with run_after(
        r'"C:\Program Files\BlankInnoSetupProgram\unins000.exe" '
        "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-"
    ):
        assert _read_any_prog_file("test.txt") == "this is an executable"


def test_inno_setup_updating():
    """Test that std.install with inno works on updates."""
    proc = run_embark("tests/fixtures/test_install_innosetup_updates.yml")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    with run_after(
        r'"C:\Program Files\BlankInnoSetupProgram\unins000.exe" '
        "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-"
    ):
        assert _read_any_prog_file("test_upd.txt") == "this is an update"
