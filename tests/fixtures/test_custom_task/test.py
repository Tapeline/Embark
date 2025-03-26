from pathlib import Path

from pydantic import BaseModel

from embark.domain.tasks.task import (
    AbstractExecutionTarget,
    Task,
    TaskExecutionContext,
)
from embark.use_case.config.loader import AbstractTaskLoader


class TestTaskParams(BaseModel):
    """Params for test loader."""

    message: str
    file: str


class TaskLoader(AbstractTaskLoader):
    """Test loader."""

    name = "test_custom_task.test"

    def load_task(
            self, context_factory, task_name: str, task_config: dict
    ) -> Task:
        """Load task."""
        criteria = None
        requirements = []
        target = TestTarget(TestTaskParams(**task_config))
        return Task(
            context_factory, task_name, criteria, requirements, target
        )


class TestTarget(AbstractExecutionTarget):
    """Test."""

    def __init__(self, params: TestTaskParams):
        """Create target."""
        self.params = params

    def execute(self, context: TaskExecutionContext) -> bool:
        """Run target."""
        Path(self.params.file).write_text(self.params.message)
        return True

    def get_display_name(self) -> str:
        """Get display name of task."""
        return "Test task"


__embark_loader__ = TaskLoader()
