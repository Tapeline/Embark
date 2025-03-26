"""Provides tools for loading entities from DTO."""

import logging
import os

from embark import log_config
from embark.domain.execution.context import AbstractContextFactory
from embark.domain.execution.playbook import Playbook
from embark.domain.execution.variables import VariablesEnv
from embark.domain.tasks.task import Task
from embark.use_case.config.exceptions import LoaderNotFoundException
from embark.use_case.config.loader import (
    AbstractTaskLoader,
    AbstractTaskLoaderRepository,
)
from embark.use_case.models import PlaybookConfig, TaskConfig


def load_playbook_from_config(  # noqa: WPS210
        context_factory: AbstractContextFactory,
        loader_repo: AbstractTaskLoaderRepository,
        playbook_config: PlaybookConfig,
) -> Playbook:
    """Loads playbook from config which was created from yaml file."""
    logger = logging.getLogger("playbook_loader")
    log_config.setup_default_handlers(logger)
    variables = VariablesEnv(playbook_config.variables, dict(os.environ))
    tasks = []
    for task in playbook_config.tasks:
        loaded_task, loader = _load_task(
            task,
            loader_repo,
            context_factory,
            variables
        )
        if task is None:
            logger.warning(
                "Task loader %s returned None instead of Task",
                loader.name
            )
        else:
            tasks.append(loaded_task)
    return Playbook(
        context_factory,
        playbook_config.name,
        tasks,
        variables=variables
    )


def _load_task(
        task: TaskConfig,
        loader_repo: AbstractTaskLoaderRepository,
        context_factory: AbstractContextFactory,
        variables: VariablesEnv,
) -> tuple[Task, AbstractTaskLoader]:
    """Load task from config."""
    loader = loader_repo.get_task_loader(task.target_type)
    if loader is None:
        raise LoaderNotFoundException(task.target_type)
    formatted_name = variables.format(task.task_name)
    formatted_data = variables.format_object(task.target_data)
    return loader.load_task(
        context_factory,
        formatted_name,
        formatted_data
    ), loader
