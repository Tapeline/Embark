from domain.config import loader, models
from domain.config.loader import AbstractTaskLoaderRepository
from domain.execution.playbook import Playbook
import yaml

from domain.tasks.task import AbstractContextFactory


def load_playbook_from_file(context_factory: AbstractContextFactory,
                            loader_repo: AbstractTaskLoaderRepository,
                            path: str, encoding=None) -> Playbook:
    with open(path, "r", encoding=encoding) as f:
        data = yaml.safe_load(f)
        # TODO: check for possible exceptions on yaml load
    playbook_config = models.load_playbook_config(data)
    return loader.load_playbook_from_config(context_factory, loader_repo, playbook_config)
