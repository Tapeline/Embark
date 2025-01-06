"""Loader for std.echo."""

from pydantic import BaseModel

from embark.domain.config.loader import AbstractTaskLoader
from embark.domain.tasks.task import (Task, AbstractExecutionTarget,
                                      TaskExecutionContext)


class TaskModel(BaseModel):
    """Pydantic model."""

    message: str


class EchoTaskLoader(AbstractTaskLoader):
    """std.echo loader."""

    name = "std.echo"

    def load_task(self, context_factory, task_name: str, task_config: dict) -> Task:
        model = TaskModel(**task_config)

        criteria = None
        requirements = []
        target = PrintMessageTarget(model.message)

        return Task(context_factory, task_name, criteria, requirements, target)


class PrintMessageTarget(AbstractExecutionTarget):
    """Echo target."""

    def __init__(self, message: str) -> None:
        """Create target."""
        self.message = message

    def execute(self, context: TaskExecutionContext) -> bool:
        print(self.message)
        return True

    def get_display_name(self) -> str:
        return "Print task"
