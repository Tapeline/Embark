"""
Provides function for loading yaml playbook
"""
import yaml

from domain.config import loader, models
from domain.config.loader import AbstractTaskLoaderRepository
from domain.execution.playbook import Playbook
from domain.tasks.task import AbstractContextFactory


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
    playbook_config = models.load_playbook_config(data)
    return loader.load_playbook_from_config(context_factory, loader_repo, playbook_config)
