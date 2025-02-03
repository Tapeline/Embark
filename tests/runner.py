import os
import shutil
import subprocess
from contextlib import contextmanager


def run_embark(
        *args: str,
        env: dict | None = None,
        **kwargs
) -> subprocess.CompletedProcess:
    """Run embark with args."""
    proc_args = ["python", "-m", "embark.main", "run", *args]
    proc_env = os.environ
    if env:
        proc_env |= env
    proc = subprocess.Popen(
        proc_args,
        bufsize=1,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd=".",
        env=proc_env,
        **kwargs
    )
    while proc.poll() is None:
        ...
    return subprocess.CompletedProcess(
        proc_args,
        returncode=proc.returncode,
        stdout=proc.stdout.read(),
        stderr=proc.stderr.read()
    )


@contextmanager
def remove_after(*paths: str):
    try:
        yield
    finally:
        for path in paths:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
