"""
Application declaration
"""
from embark.domain.interfacing.os_provider import OSInterface

# pylint: disable=too-few-public-methods
from embark.impl import action
from embark.impl.context_factory import CLIContextFactory
from embark.impl.task_loader_repo import TaskLoaderRepository


class Application:
    """App class"""

    def __init__(
            self,
            os_interface: OSInterface,
            config_file: str,
            file_encoding=None
    ) -> None:
        self.config_file = config_file
        self.context_factory = CLIContextFactory(os_interface)
        self.loader_repo = TaskLoaderRepository()
        self.file_encoding = file_encoding

    def run(self) -> int:
        """Run Embark app"""
        is_successful = action.execute_playbook_file(
            self.context_factory, self.loader_repo,
            self.config_file, self.file_encoding
        )
        return 0 if is_successful else 1
