"""
Provides function for loading yaml playbook
"""
import os.path
from pathlib import Path

import yaml

from embark.domain.config import loader, models
from embark.domain.config.loader import AbstractTaskLoaderRepository
from embark.domain.execution.playbook import Playbook
from embark.domain.tasks.task import AbstractContextFactory


def load_playbook_from_file(context_factory: AbstractContextFactory,
                            loader_repo: AbstractTaskLoaderRepository,
                            path: str, encoding=None) -> Playbook:
    """
    Load playbook from yaml file.
    Context factory and loader repo concrete implementation
    should be provided in order for generified actions to work
    """
    with open(path, "r", encoding=encoding) as f:
        data = yaml.safe_load(f)
    var_path = Path(path).parent.joinpath(".variables.yml")
    variables = {}
    if var_path.exists():
        with open(str(var_path.absolute()), "r", encoding=encoding) as f:
            variables = yaml.safe_load(f)
    playbook_config = models.load_playbook_config(data)
    playbook_config.variables.update(variables)
    return loader.load_playbook_from_config(context_factory, loader_repo, playbook_config)
