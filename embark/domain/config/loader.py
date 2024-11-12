# pylint: disable=too-few-public-methods
"""
Provides classes for task loading and functions for config loading
"""
import logging
import os
from abc import ABC, abstractmethod

from embark import log_config
from embark.domain.config.exceptions import LoaderNotFoundException
from embark.domain.config.models import PlaybookConfig
from embark.domain.config.variables import VariablesEnv
from embark.domain.execution.playbook import Playbook
from embark.domain.tasks.task import Task, AbstractContextFactory


class AbstractTaskLoader(ABC):
    """
    ABC for task loader.
    Task loader load a task (specifically execution criteria,
    execution requirements and execution target) from a dict
    which was loaded from yaml.
    """
    name: str

    @abstractmethod
    def load_task(self, context_factory, task_name: str, task_config: dict) -> Task:
        """
        Loads a task from yaml.
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
        Example:
            - name: Test Task
              std.copy:
                ...
            std.copy here is the loader_name
        """
        raise NotImplementedError


def load_playbook_from_config(context_factory: AbstractContextFactory,
                              loader_repo: AbstractTaskLoaderRepository,
                              playbook_config: PlaybookConfig) -> Playbook:
    """
    Loads playbook from config which was created from yaml file
    """
    logger = logging.getLogger("playbook_loader")
    log_config.setup_default_handlers(logger)
    variables = VariablesEnv(playbook_config.variables, os.environ)
    tasks = []
    for task in playbook_config.tasks:
        loader = loader_repo.get_task_loader(task.target_type)
        if loader is None:
            raise LoaderNotFoundException(task.target_type)
        formatted_name = variables.format(task.task_name)
        formatted_data = variables.format_object(task.target_data)
        task = loader.load_task(context_factory, formatted_name, formatted_data)
        if task is None:
            logger.warning("Task loader %s returned None instead of Task", loader.name)
        else:
            tasks.append(task)
    return Playbook(context_factory, playbook_config.name, tasks)
