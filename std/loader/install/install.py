from typing import Optional

from pydantic import BaseModel

from domain.config.loader import AbstractTaskLoader
from domain.tasks.task import Task
from std.criteria.file_criteria import FileDoesNotExistCriteria
from std.criteria.install_criteria import ProgramNotInstalledCriteria
from std.requirement.privileges import AdminPrivilegesRequirement
from std.target.file_tasks import CopyFileTarget
from std.target.install.install_tasks import InstallTarget


class TaskModel(BaseModel):
    name: str
    publisher: str
    version: str
    installer: str
    msi_admin: bool = False
    cmd_install: Optional[str] = None
    cmd_uninstall: Optional[str] = None


class InstallTaskLoader(AbstractTaskLoader):
    name = "std.install"

    def load_task(self, context_factory, task_name: str, task_config: dict) -> Task:
        model = TaskModel(**task_config)

        criteria = ProgramNotInstalledCriteria(model.name, model.version, model.publisher)

        requirements = [AdminPrivilegesRequirement()]

        target = InstallTarget(
            model.name,
            model.version,
            model.publisher,
            model.installer,
            model.msi_admin,
            model.cmd_install,
            model.cmd_uninstall
        )

        return Task(context_factory, task_name, criteria, requirements, target)
