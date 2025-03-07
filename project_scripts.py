import os
import shutil
import subprocess
import sys


def check_mypy():
    process = subprocess.run(
        "mypy --install-types",
        stderr=sys.stderr,
        stdout=sys.stdout, check=False
    )
    if process.returncode != 0:
        exit(process.returncode)
    process = subprocess.run(
        "mypy embark",
        stderr=sys.stderr,
        stdout=sys.stdout, check=False
    )
    if process.returncode != 0:
        exit(process.returncode)


def check_imports():
    process = subprocess.run(
        "lint-imports",
        stderr=sys.stderr,
        stdout=sys.stdout, check=False
    )
    if process.returncode != 0:
        exit(process.returncode)


def check_ruff():
    process = subprocess.run(
        "ruff check",
        stderr=sys.stderr,
        stdout=sys.stdout, check=False
    )
    if process.returncode != 0:
        exit(process.returncode)


def check_wps():
    process = subprocess.run(
        "flake8 ./embark",
        stderr=sys.stderr,
        stdout=sys.stdout, check=False
    )
    if process.returncode != 0:
        exit(process.returncode)


def check_all():
    check_all_no_wps()
    check_wps()


def check_all_no_wps():
    check_mypy()
    check_imports()
    check_ruff()


def clean_build():
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    build()


def build():
    process = subprocess.run(
        "build.bat",
        stderr=sys.stderr,
        stdout=sys.stdout, check=False
    )
    sys.exit(process.returncode)
