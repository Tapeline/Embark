"""Provides function for loading yaml playbook."""
from pathlib import Path

import yaml

from embark.domain.execution.context import AbstractContextFactory
from embark.domain.execution.playbook import Playbook
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
    loader_repo.set_playbook_root(str(Path(path).absolute().parent))
    variables = _load_variables(encoding, path)
    playbook_config = models.load_playbook_config(config_data)
    playbook_config = models.PlaybookConfig(
        playbook_config.name,
        variables | playbook_config.variables,
        playbook_config.tasks
    )
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
