from domain.tasks.task import AbstractExecutionCriteria, TaskExecutionContext
from std.target.install.installs_repo import WindowsInstallsRepository


class ProgramNotInstalledCriteria(AbstractExecutionCriteria):
    def __init__(self, name: str, version: str, publisher: str):
        self.name = name
        self.version = version
        self.publisher = publisher

    def should_execute(self, context: TaskExecutionContext) -> bool:
        repo = WindowsInstallsRepository()
        for install in repo.get_all_installs():
            if install.name == self.name and \
                    install.version == self.version and \
                    install.publisher == self.publisher:
                return False
        return True

    def get_display_name(self):
        return f"Program {self.name} {self.version} by {self.publisher} not installed"
