from tests.runner import run_embark


def test_variables_in_file(snapshot):
    """Test that variables in file work."""
    proc = run_embark("tests/fixtures/test_vars_in_file.yml")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert proc.stdout == snapshot


def test_variables_in_separate_file(snapshot):
    """Test that variables in .variables.yml file work."""
    proc = run_embark("tests/fixtures/test_vars_in_sep_file.yml")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert proc.stdout == snapshot


def test_variables_mixing(snapshot):
    """Test that variables from env, .variables and playbook work together."""
    proc = run_embark(
        "tests/fixtures/test_vars_mixing.yml",
        env={
            "VAR3": "env"
        }
    )
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert proc.stdout == snapshot
