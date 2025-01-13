"""Provides function for loading yaml playbook."""

from pathlib import Path

import yaml

from embark.domain.config.loader import AbstractTaskLoaderRepository
from embark.domain.execution.playbook import Playbook
from embark.domain.tasks.task import AbstractContextFactory
from embark.use_case import models, playbook_loader


def load_playbook_from_file(
        context_factory: AbstractContextFactory,
        loader_repo: AbstractTaskLoaderRepository,
        path: str,
        encoding: str | None = None,
) -> Playbook:
    """
    Load playbook from yaml file.

    Args:
        context_factory: playbook and task context factory
        loader_repo: repository of task loaders
        path: playbook file path
        encoding: playbook encoding name

    Returns:
        loaded playbook entity.
    """
    with open(path, "r", encoding=encoding) as config_file:
        data = yaml.safe_load(config_file)
    var_path = Path(path).parent.joinpath(".variables.yml")
    variables = {}
    if var_path.exists():
        with open(str(var_path.absolute()), "r", encoding=encoding) as var_file:
            variables = yaml.safe_load(var_file)
    playbook_config = models.load_playbook_config(data)
    playbook_config.variables.update(variables)
    return playbook_loader.load_playbook_from_config(
        context_factory,
        loader_repo,
        playbook_config,
    )
