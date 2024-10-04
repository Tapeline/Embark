from domain import action
from impl.context_factory import ContextFactory
from impl.task_loader_repo import TaskLoaderRepository


class Application:
    def __init__(self, config_file: str, file_encoding=None):
        self.config_file = config_file
        self.context_factory = ContextFactory()
        self.loader_repo = TaskLoaderRepository()
        self.file_encoding = file_encoding

    def run(self) -> int:
        is_successful = action.execute_playbook_file(
            self.context_factory, self.loader_repo,
            self.config_file, self.file_encoding
        )
        return 0 if is_successful else 1
