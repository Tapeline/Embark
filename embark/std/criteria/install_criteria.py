"""
Provides criteria which account installed programs
"""
import re

from embark.domain.tasks.task import AbstractExecutionCriteria, TaskExecutionContext
from embark.std.target.install.installs_repo import WindowsInstallsRepository


class ProgramNotInstalledCriteria(AbstractExecutionCriteria):
    """Execute if specific version of specific program is not installed"""
    def __init__(self, name: str, version: str | None, publisher: str | None,
                 ignore_version: bool = False):
        self.name = name
        self.version = version
        self.publisher = publisher
        self.ignore_version = ignore_version

    def should_execute(self, context: TaskExecutionContext) -> bool:
        repo = WindowsInstallsRepository()
        for install in repo.get_all_installs():
            if (re.fullmatch(self.name, install.name) is not None
                    and (install.publisher == self.publisher or install.publisher is None) and
                    (install.version == self.version or self.ignore_version)):
                return False
        return True

    def get_display_name(self):
        return f"Program {self.name} {self.version} by {self.publisher} not installed"
