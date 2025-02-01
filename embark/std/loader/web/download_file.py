"""Provides loader and tools for ``std.download``."""

from pydantic import BaseModel

from embark.use_case.config.loader import AbstractTaskLoader
from embark.domain.tasks.task import Task, AbstractContextFactory
from embark.std.criteria.file_criteria import FileDoesNotExistCriteria
from embark.std.target.web_tasks import DownloadFileTarget


class TaskModel(BaseModel):
    """Pydantic model of task config."""

    overwrite: bool = False
    timeout_s: int = 10
    url: str
    dst: str


class DownloadFileTaskLoader(AbstractTaskLoader):
    """Task loader impl for ``std.download``."""

    name = "std.download"

    def load_task(
            self,
            context_factory: AbstractContextFactory,
            task_name: str,
            task_config: dict
    ) -> Task:
        model = TaskModel(**task_config)

        criteria = None
        if not model.overwrite:
            criteria = FileDoesNotExistCriteria(model.dst)

        return Task(
            context_factory,
            task_name,
            criteria=criteria,
            requirements=[],
            target=DownloadFileTarget(
                model.url,
                model.dst,
                model.timeout_s
            )
        )
