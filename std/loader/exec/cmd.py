# pylint: disable=too-few-public-methods
"""
Provides loader and tools for `std.cmd`
"""

from pydantic import BaseModel

from domain.config.loader import AbstractTaskLoader
from domain.tasks.task import Task
from std.requirement.privileges import AdminPrivilegesRequirement
from std.target.exec_tasks import RunCommandTarget


class TaskModel(BaseModel):
    """Pydantic model of task config"""
    cmd: str
    admin: bool = False


class CmdTaskLoader(AbstractTaskLoader):
    """Task loader impl for `std.cmd`"""
    name = "std.cmd"

    def load_task(self, context_factory, task_name: str, task_config: dict) -> Task:
        model = TaskModel(**task_config)

        criteria = None

        requirements = []
        if model.admin:
            requirements.append(AdminPrivilegesRequirement())

        target = RunCommandTarget(model.cmd)

        return Task(context_factory, task_name, criteria, requirements, target)
