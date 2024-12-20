# pylint: disable=too-few-public-methods
"""
Provides loader and tools for `std.copy`
"""

from pydantic import BaseModel

from embark.domain.config.loader import AbstractTaskLoader
from embark.domain.tasks.task import Task
from embark.std.criteria.file_criteria import FileDoesNotExistCriteria, FileExistsCriteria
from embark.std.criteria.logic_criteria import AndCriteria
from embark.std.requirement.privileges import AdminPrivilegesRequirement
from embark.std.target.file_tasks import CopyFileTarget


class TaskModel(BaseModel):
    """Pydantic model of task config"""
    admin: bool = False
    overwrite: bool = False
    src: str
    dst: str
    skip_if_missing: bool = False


class CopyFileTaskLoader(AbstractTaskLoader):
    """Task loader impl for `std.copy`"""
    name = "std.copy"

    def load_task(self, context_factory, task_name: str, task_config: dict) -> Task:
        model = TaskModel(**task_config)

        criteria = None
        if not model.overwrite:
            criteria = FileDoesNotExistCriteria(model.dst)
        if model.skip_if_missing:
            criteria = AndCriteria(FileExistsCriteria(model.src), criteria)

        requirements = []
        if model.admin:
            requirements.append(AdminPrivilegesRequirement())

        target = CopyFileTarget(model.src, model.dst)

        return Task(context_factory, task_name, criteria, requirements, target)
