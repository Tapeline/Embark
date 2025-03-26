"""Provides loader and tools for ``std.copy``."""
from typing import Any

from pydantic import BaseModel

from embark.domain.execution.context import AbstractContextFactory
from embark.domain.tasks.task import AbstractExecutionCriteria, Task
from embark.std.criteria.file_criteria import (
    FileDoesNotExistCriteria,
    FileExistsCriteria,
)
from embark.std.criteria.logic_criteria import AndCriteria
from embark.std.requirement.privileges import AdminPrivilegesRequirement
from embark.std.target.file_tasks import CopyFileTarget
from embark.use_case.config.loader import AbstractTaskLoader


class TaskModel(BaseModel):
    """Pydantic model of task config."""

    admin: bool = False
    overwrite: bool = False
    src: str
    dst: str
    skip_if_missing: bool = False


class CopyFileTaskLoader(AbstractTaskLoader):
    """Task loader impl for ``std.copy``."""

    name = "std.copy"

    def load_task(
            self,
            context_factory: AbstractContextFactory,
            task_name: str,
            task_config: dict[Any, Any]
    ) -> Task:
        """Load task."""
        model = TaskModel(**task_config)

        criteria: AbstractExecutionCriteria | None = None
        if not model.overwrite:
            criteria = FileDoesNotExistCriteria(model.dst)
        if model.skip_if_missing:
            criteria = AndCriteria(FileExistsCriteria(model.src), criteria)

        requirements = []
        if model.admin:
            requirements.append(AdminPrivilegesRequirement())

        target = CopyFileTarget(model.src, model.dst)

        return Task(
            context_factory,
            task_name,
            criteria,
            requirements,
            target
        )
