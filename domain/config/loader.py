from abc import ABC, abstractmethod

from domain.config.exceptions import LoaderNotFoundException
from domain.config.models import PlaybookConfig
from domain.execution.playbook import Playbook
from domain.tasks.task import Task, AbstractContextFactory


class AbstractTaskLoader(ABC):
    name: str

    @abstractmethod
    def load_task(self, task_name: str, task_config: dict) -> Task:
        raise NotImplementedError


class AbstractTaskLoaderRepository(ABC):
    @abstractmethod
    def get_task_loader(self, loader_name: str) -> AbstractTaskLoader | None:
        raise NotImplementedError


def load_playbook_from_config(context_factory: AbstractContextFactory,
                              loader_repo: AbstractTaskLoaderRepository,
                              playbook_config: PlaybookConfig) -> Playbook:
    tasks = []
    for task in playbook_config.tasks:
        loader = loader_repo.get_task_loader(task.target_type)
        if loader is None:
            raise LoaderNotFoundException(task.target_type)
        tasks.append(loader.load_task(task.task_name, task.target_data))
    return Playbook(context_factory, playbook_config.name, tasks)
