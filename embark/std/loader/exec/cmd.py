"""Provides loader and tools for `std.cmd`."""

from typing import Any

from pydantic import BaseModel

from embark.domain.execution.context import AbstractContextFactory
from embark.domain.tasks.task import Task
from embark.std.requirement.privileges import AdminPrivilegesRequirement
from embark.std.target.exec_tasks import RunCommandTarget
from embark.use_case.config.loader import AbstractTaskLoader


class TaskModel(BaseModel):
    """Pydantic model of task config."""

    cmd: str
    admin: bool = False


class CmdTaskLoader(AbstractTaskLoader):
    """Task loader impl for ``std.cmd``."""

    name = "std.cmd"

    def load_task(
            self,
            context_factory: AbstractContextFactory,
            task_name: str,
            task_config: dict[Any, Any]
    ) -> Task:
        """Load task."""
        model = TaskModel(**task_config)

        criteria = None

        requirements = []
        if model.admin:
            requirements.append(AdminPrivilegesRequirement())

        target = RunCommandTarget(model.cmd)

        return Task(
            context_factory,
            task_name,
            criteria,
            requirements,
            target
        )
