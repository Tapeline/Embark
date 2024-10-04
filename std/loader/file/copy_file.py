from pydantic import BaseModel

from domain.config.loader import AbstractTaskLoader
from domain.tasks.task import Task
from std.criteria.file_criteria import FileDoesNotExistCriteria
from std.requirement.privileges import AdminPrivilegesRequirement
from std.target.file_tasks import CopyFileTarget


class TaskModel(BaseModel):
    admin: bool = False
    overwrite: bool = False
    src: str
    dst: str


class CopyFileTaskLoader(AbstractTaskLoader):
    name = "std.copy"

    def load_task(self, context_factory, task_name: str, task_config: dict) -> Task:
        model = TaskModel(**task_config)

        criteria = None
        if not model.overwrite:
            criteria = FileDoesNotExistCriteria(model.dst)

        requirements = []
        if model.admin:
            requirements.append(AdminPrivilegesRequirement())

        target = CopyFileTarget(model.src, model.dst)

        return Task(context_factory, task_name, criteria, requirements, target)
