# pylint: disable=too-few-public-methods
"""
Implementation of task loader repo
"""

from embark.domain.config.loader import AbstractTaskLoaderRepository, AbstractTaskLoader
from embark.std.loader.file.copy_file import CopyFileTaskLoader
from embark.std.loader.install.install import InstallTaskLoader
from embark.std.loader.exec.cmd import CmdTaskLoader


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
TaskLoaderRepository.LOADERS.append(CmdTaskLoader())
