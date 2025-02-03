from tests.runner import run_embark


def test_echo_task(snapshot):
    """Test that std.echo works."""
    proc = run_embark("tests/fixtures/test_echo.yml")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert proc.stdout == snapshot
