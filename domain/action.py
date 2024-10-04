from domain.config import config
from domain.config.loader import AbstractTaskLoaderRepository
from domain.tasks.task import AbstractContextFactory


IsSuccessful = bool


def execute_playbook_file(context_factory: AbstractContextFactory,
                          loader_repo: AbstractTaskLoaderRepository,
                          path: str, file_encoding=None) -> IsSuccessful:
    playbook = config.load_playbook_from_file(context_factory, loader_repo,
                                              path, encoding=file_encoding)
    return playbook.run()
