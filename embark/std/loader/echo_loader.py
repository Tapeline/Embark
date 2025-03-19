"""Loader for std.echo."""

from pydantic import BaseModel

from embark.domain.tasks.task import (
    AbstractExecutionTarget,
    Task,
    TaskExecutionContext,
)
from embark.output import write_out
from embark.use_case.config.loader import AbstractTaskLoader


class TaskModel(BaseModel):
    """Pydantic model."""

    message: str


class EchoTaskLoader(AbstractTaskLoader):
    """std.echo loader."""

    name = "std.echo"

    def load_task(
            self,
            context_factory,
            task_name: str,
            task_config: dict
    ) -> Task:
        model = TaskModel(**task_config)
        return Task(
            context_factory,
            task_name,
            criteria=None,
            requirements=[],
            target=PrintMessageTarget(model.message),
        )


class PrintMessageTarget(AbstractExecutionTarget):
    """Echo target."""

    def __init__(self, message: str) -> None:
        """Create target."""
        self.message = message

    def execute(self, context: TaskExecutionContext) -> None:
        write_out(self.message)

    def get_display_name(self) -> str:
        return "Print task"
