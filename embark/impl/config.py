"""Provides function for loading yaml playbook."""
from pathlib import Path

import yaml

from embark.domain.execution.playbook import Playbook
from embark.domain.tasks.task import AbstractContextFactory
from embark.use_case import models, playbook_loader
from embark.use_case.config.loader import AbstractTaskLoaderRepository


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
    with open(path, encoding=encoding) as config_file:
        config_data = yaml.safe_load(config_file)
    variables = _load_variables(encoding, path)
    playbook_config = models.load_playbook_config(config_data)
    playbook_config.variables = variables | playbook_config.variables
    return playbook_loader.load_playbook_from_config(
        context_factory,
        loader_repo,
        playbook_config,
    )


def _load_variables(encoding: str | None, path: str) -> dict[str, str]:
    var_path = Path(path).parent.joinpath(".variables.yml")
    variables = {}
    if var_path.exists():
        with open(
            str(var_path.absolute()),
            encoding=encoding
        ) as var_file:
            variables = yaml.safe_load(var_file)
    return variables
