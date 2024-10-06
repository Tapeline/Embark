# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
"""
Provides targets and tools for installation management
"""

import subprocess

from domain.tasks.task import AbstractExecutionTarget, TaskExecutionContext
from std.target.install.installs_repo import (WindowsInstallsRepository,
                                              CannotUninstallQuietlyException,
                                              CannotUninstallException,
                                              CannotInstallQuietlyException,
                                              CannotInstallException)


class InstallTarget(AbstractExecutionTarget):
    """Target for installing"""
    def __init__(self,
                 name: str,
                 version: str,
                 publisher: str,
                 installer: str,
                 msi_admin: bool = False,
                 cmd_install: str | None = None,
                 cmd_uninstall: str | None = None):
        self.name = name
        self.version = version
        self.publisher = publisher
        self.installer = installer
        self.msi_admin = msi_admin
        self.cmd_install = cmd_install
        self.cmd_uninstall = cmd_uninstall

    def execute(self, context: TaskExecutionContext) -> bool:
        logger = context.task.logger
        repo = WindowsInstallsRepository()
        old_installation = self._get_existing_installation(repo)
        if old_installation is not None:
            logger.info("Found old installation, removing")
            success = self._uninstall(repo, logger, old_installation)
            if not success:
                return False
        success = self._install(repo, logger)
        if not success:
            return False
        return True

    def _install(self, repo, logger):
        """Install program"""
        logger.info("Installing %s", self.version)
        success = False
        if self.cmd_install is not None:
            success = subprocess.call(self.cmd_install) == 0
        else:
            try:
                success = repo.install_quietly(self.installer, self.msi_admin)
            except CannotInstallQuietlyException:
                logger.error("Quiet install failed. Trying regular install")
                logger.warning("User action required!")
                try:
                    success = repo.install(self.installer, self.msi_admin)
                except CannotInstallException:
                    logger.error("Install failed")
                    return False
        if not success:
            logger.error("Install failed")
            return False
        return True

    def _get_existing_installation(self, repo):
        """Seek for existing installations of any version"""
        for install in repo.get_all_installs():
            if install.name == self.name and install.publisher == self.publisher:
                return install
        return None

    def _uninstall(self, repo, logger, old_installation):
        """Uninstall old installation"""
        logger.info("Uninstalling %s", old_installation)
        success = False
        if self.cmd_uninstall is not None:
            success = subprocess.call(self.cmd_uninstall) == 0
        else:
            try:
                success = repo.uninstall_quietly(old_installation)
            except CannotUninstallQuietlyException:
                logger.error("Quiet uninstall failed. Trying regular uninstall")
                logger.warning("User action required!")
                try:
                    success = repo.uninstall(old_installation)
                except CannotUninstallException:
                    logger.error("Uninstall failed")
                    return False
        if not success:
            logger.error("Uninstall failed")
            return False
        return True

    def get_display_name(self) -> str:
        return f"Install {self.name} {self.version}"
