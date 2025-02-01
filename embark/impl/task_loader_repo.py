"""Implementation of task loader repo."""

import logging
import os
from importlib import util as import_util

from embark import log_config
from embark.use_case.config.loader import (
    AbstractTaskLoaderRepository,
    AbstractTaskLoader,
)
from embark.impl import pip_pkg
from embark.std.loader.echo_loader import EchoTaskLoader
from embark.std.loader.file.copy_file import CopyFileTaskLoader
from embark.std.loader.install.install import InstallTaskLoader
from embark.std.loader.exec.cmd import CmdTaskLoader
from embark.std.loader.web.download_file import DownloadFileTaskLoader


class TaskLoaderRepository(AbstractTaskLoaderRepository):
    """Task loader repo implementation."""

    loaders: list[AbstractTaskLoader] = []

    def __init__(self) -> None:
        """Create loader repo"""
        super().__init__()
        self.logger = logging.getLogger("task_loader")
        log_config.setup_default_handlers(self.logger)

    def get_task_loader(self, loader_name: str) -> AbstractTaskLoader | None:
        for loader in self.loaders:
            if loader.name == loader_name:
                return loader
        return self.lookup_loader_file(loader_name)

    def lookup_loader_file(
            self,
            loader_name: str
    ) -> AbstractTaskLoader | None:
        """Try to load a custom loader from a .py file."""
        loader_path = "{0}.py".format(loader_name.replace(".", "/"))
        self._install_loader_requirements_if_needed(loader_path)
        module = self._load_py_module(loader_path)
        if module is None:
            return None
        is_valid = self._validate_loader_module(module, loader_name)
        if not is_valid:
            return None
        return module.__embark_loader__

    def _load_py_module(self, filename: str):
        """Load python module."""
        if not os.path.exists(filename):
            return None
        spec = import_util.spec_from_file_location(filename, filename)
        if spec is None:
            return None
        module = import_util.module_from_spec(spec)
        if spec.loader is None:
            return None
        spec.loader.exec_module(module)
        return module

    def _install_loader_requirements_if_needed(self, filename: str) -> None:
        """Install pip requirements."""
        requirements_file = f"{filename}.requirements"
        if not os.path.exists(requirements_file):
            return
        self.logger.info(
            "Installing pip requirements of %s",
            requirements_file
        )
        return_code = pip_pkg.install_requirements(requirements_file)
        if return_code != 0:
            self.logger.error("Pip install of %s failed!", requirements_file)

    def _validate_loader_module(self, module, loader_name: str) -> bool:
        """Check that loader module provides loader."""
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


# TODO: add on class extension
TaskLoaderRepository.loaders.append(DownloadFileTaskLoader())
TaskLoaderRepository.loaders.append(CopyFileTaskLoader())
TaskLoaderRepository.loaders.append(InstallTaskLoader())
TaskLoaderRepository.loaders.append(CmdTaskLoader())
TaskLoaderRepository.loaders.append(EchoTaskLoader())
