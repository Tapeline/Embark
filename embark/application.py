"""
Application declaration
"""
# pylint: disable=too-few-public-methods

import os

from embark.domain import action
from embark.impl.context_factory import CLIContextFactory
from embark.impl.task_loader_repo import TaskLoaderRepository


class Application:
    """App class"""

    def __init__(self, config_file: str, file_encoding=None):
        self.config_file = config_file
        self.context_factory = CLIContextFactory()
        self.loader_repo = TaskLoaderRepository()
        self.file_encoding = file_encoding

    def run(self) -> int:
        """Run Embark app"""
        os.chdir(os.path.dirname(os.path.abspath(self.config_file)))
        is_successful = action.execute_playbook_file(
            self.context_factory, self.loader_repo,
            self.config_file, self.file_encoding
        )
        return 0 if is_successful else 1
