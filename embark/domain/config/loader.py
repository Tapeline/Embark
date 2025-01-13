"""Provides classes for task loading and functions for config loading"""

from abc import ABC, abstractmethod

from embark.domain.tasks.task import Task, AbstractContextFactory


class AbstractTaskLoader(ABC):
    """
    ABC for task loader.

    Task loader loads a task (specifically execution criteria,
    execution requirements and execution target) from a dict
    which was loaded from yaml.
    """

    name: str

    @abstractmethod
    def load_task(
            self,
            context_factory: AbstractContextFactory,
            task_name: str,
            task_config: dict
    ) -> Task:
        """
        Loads a task from yaml.

        Args:
            context_factory: context factory
            task_name: task name (like ``std.copy``)
            task_config: task configuration json

        Returns:
            Loaded task entity

        Example:
            - name: Task Name
              std.my_task_id:
                key1: value
                key2: value
            {key1: value, key2: value} will be provided as task_config
            and "Task Name" will be provided as task_name
        """
        raise NotImplementedError


class AbstractTaskLoaderRepository(ABC):
    """
    ABC for task loader repos.

    ABC instead of regular repo with list is used for
    cases if implementation wants to get task loader from
    external modules (e.g. from custom python files)
    """

    @abstractmethod
    def get_task_loader(self, loader_name: str) -> AbstractTaskLoader | None:
        """
        Get loader with provided name.

        Args:
            loader_name: name of task loader

        Example:
            - name: Test Task
              std.copy:
                ...
            std.copy here is the loader_name
        """
        raise NotImplementedError
