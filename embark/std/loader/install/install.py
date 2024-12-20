# pylint: disable=too-few-public-methods
"""
Provides loader and tools for `std.install`
"""

from typing import Optional

from pydantic import BaseModel

from embark.domain.config.exceptions import InvalidConfigException
from embark.domain.config.loader import AbstractTaskLoader
from embark.domain.tasks.task import Task
from embark.std.criteria.install_criteria import ProgramNotInstalledCriteria
from embark.std.requirement.privileges import AdminPrivilegesRequirement
from embark.std.target.install.install_tasks import InstallTarget, InstallTargetParams


class TaskModel(BaseModel):
    """Pydantic model for task config"""
    name: str
    publisher: Optional[str] = None
    version: Optional[str] = None
    installer: str
    msi_admin: bool = False
    cmd_install: Optional[str] = None
    cmd_uninstall: Optional[str] = None
    lookup_paths: Optional[list[str]] = None
    no_remove: bool = False
    ignore_version: bool = False


class InstallTaskLoader(AbstractTaskLoader):
    """Task loader impl for `std.install`"""
    name = "std.install"

    def load_task(self, context_factory, task_name: str, task_config: dict) -> Task:
        model = TaskModel(**task_config)
        if (model.publisher is None or model.version is None) and model.lookup_paths is None:
            raise InvalidConfigException(
                "Either publisher and version should be provided or lookup_paths"
            )

        criteria = ProgramNotInstalledCriteria(
            model.name, model.version, model.publisher,
            ignore_version=model.ignore_version
        )

        requirements = [AdminPrivilegesRequirement()]

        target = InstallTarget(
            InstallTargetParams(
                model.name,
                model.version,
                model.publisher,
                model.installer,
                model.msi_admin,
                model.cmd_install,
                model.cmd_uninstall,
                model.lookup_paths,
                model.no_remove
            )
        )

        return Task(context_factory, task_name, criteria, requirements, target)
