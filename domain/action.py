import logging

from pydantic import ValidationError

from domain.config import config
from domain.config.loader import AbstractTaskLoaderRepository
from domain.tasks.task import AbstractContextFactory


IsSuccessful = bool


def execute_playbook_file(context_factory: AbstractContextFactory,
                          loader_repo: AbstractTaskLoaderRepository,
                          path: str, file_encoding=None) -> IsSuccessful:
    try:
        playbook = config.load_playbook_from_file(context_factory, loader_repo,
                                                  path, encoding=file_encoding)
    except ValidationError as e:
        logging.getLogger("Config loader").error(str(e))
        return False
    return playbook.run()
