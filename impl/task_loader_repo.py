# pylint: disable=too-few-public-methods
"""
Implementation of task loader repo
"""

from domain.config.loader import AbstractTaskLoaderRepository, AbstractTaskLoader
from std.loader.file.copy_file import CopyFileTaskLoader
from std.loader.install.install import InstallTaskLoader


class TaskLoaderRepository(AbstractTaskLoaderRepository):
    """Task loader repo implementation"""
    LOADERS: list[AbstractTaskLoader] = []

    def get_task_loader(self, loader_name: str) -> AbstractTaskLoader | None:
        for loader in self.LOADERS:
            if loader.name == loader_name:
                return loader
        return None


TaskLoaderRepository.LOADERS.append(CopyFileTaskLoader())
TaskLoaderRepository.LOADERS.append(InstallTaskLoader())
