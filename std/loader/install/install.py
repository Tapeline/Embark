# pylint: disable=too-few-public-methods
"""
Provides loader and tools for `std.install`
"""

from typing import Optional

from pydantic import BaseModel

from domain.config.loader import AbstractTaskLoader
from domain.tasks.task import Task
from std.criteria.install_criteria import ProgramNotInstalledCriteria
from std.requirement.privileges import AdminPrivilegesRequirement
from std.target.install.install_tasks import InstallTarget


class TaskModel(BaseModel):
    """Pydantic model for task config"""
    name: str
    publisher: str
    version: str
    installer: str
    msi_admin: bool = False
    cmd_install: Optional[str] = None
    cmd_uninstall: Optional[str] = None


class InstallTaskLoader(AbstractTaskLoader):
    """Task loader impl for `std.install`"""
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
