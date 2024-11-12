import os
import shutil
import subprocess
import sys

from mypy.api import run as mypy_run
from pylint import lint


def check_pylint():
    lint.Run(["embark", "--fail-under=9.75"])


def check_mypy():
    process = subprocess.run("mypy --install-types")
    if process.returncode != 0:
        print(process.stdout)
        print(process.stderr, file=sys.stderr)
        exit(process.returncode)
    stdout, stderr, exit_code = mypy_run(["embark/main.py"])
    print(stdout, file=sys.stdout)
    print(stderr, file=sys.stderr)
    if exit_code != 0:
        exit(exit_code)


def check_all():
    check_mypy()
    check_pylint()


def clean_build():
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    build()


def build():
    process = subprocess.run("build.bat")
    print(process.stdout)
    print(process.stderr, file=sys.stderr)
    exit(process.returncode)
