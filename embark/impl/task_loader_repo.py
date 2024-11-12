# pylint: disable=too-few-public-methods
"""
Implementation of task loader repo
"""
import importlib.util
import logging
import os.path

from embark import log_config
from embark.domain.config.loader import AbstractTaskLoaderRepository, AbstractTaskLoader
from embark.impl import pip_pkg
from embark.std.loader.file.copy_file import CopyFileTaskLoader
from embark.std.loader.install.install import InstallTaskLoader
from embark.std.loader.exec.cmd import CmdTaskLoader
from embark.std.loader.web.download_file import DownloadFileTaskLoader


class TaskLoaderRepository(AbstractTaskLoaderRepository):
    """Task loader repo implementation"""
    LOADERS: list[AbstractTaskLoader] = []

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("task_loader")
        log_config.setup_default_handlers(self.logger)

    def get_task_loader(self, loader_name: str) -> AbstractTaskLoader | None:
        for loader in self.LOADERS:
            if loader.name == loader_name:
                return loader
        return self.lookup_loader_file(loader_name)

    def lookup_loader_file(self, loader_name: str) -> AbstractTaskLoader | None:
        """Try to load a custom loader from a .py file"""
        loader_path = loader_name.replace(".", "/") + ".py"
        self._install_loader_requirements_if_needed(loader_path)
        module = self._load_py_module(loader_path)
        if module is None:
            return None
        is_valid = self._validate_loader_module(module, loader_name)
        if not is_valid:
            return None
        return module.__embark_loader__

    def _load_py_module(self, filename):
        if not os.path.exists(filename):
            return None
        spec = importlib.util.spec_from_file_location(filename, filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _install_loader_requirements_if_needed(self, filename):
        requirements_file = f"{filename}.requirements"
        if not os.path.exists(requirements_file):
            return
        self.logger.info("Installing pip requirements of %s", requirements_file)
        return_code = pip_pkg.install_requirements(requirements_file)
        if return_code != 0:
            self.logger.error("Pip install of %s failed!", requirements_file)

    def _validate_loader_module(self, module, loader_name):
        if not hasattr(module, "__embark_loader__"):
            self.logger.warning(
                "Tried to import module %s, but file "
                "does not contain __embark_loader__", loader_name
            )
            return False
        if not isinstance(module.__embark_loader__, AbstractTaskLoader):
            self.logger.warning(
                "Tried to import module %s, but __embark_loader__ "
                "is not an AbstractTaskLoader", loader_name
            )
            return False
        return True


TaskLoaderRepository.LOADERS.append(DownloadFileTaskLoader())
TaskLoaderRepository.LOADERS.append(CopyFileTaskLoader())
TaskLoaderRepository.LOADERS.append(InstallTaskLoader())
TaskLoaderRepository.LOADERS.append(CmdTaskLoader())
