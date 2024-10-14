# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
"""
Provides targets and tools for installation management
"""
import os
import re
import subprocess

from embark.domain.tasks.task import AbstractExecutionTarget, TaskExecutionContext
from embark.std.target.install.installs_repo import (WindowsInstallsRepository,
                                              CannotUninstallQuietlyException,
                                              CannotUninstallException,
                                              CannotInstallQuietlyException,
                                              CannotInstallException, WindowsInstallation,
                                              determine_quiet_uninstall_command)


class InstallTarget(AbstractExecutionTarget):
    """Target for installing"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self,
                 name: str,
                 version: str | None,
                 publisher: str | None,
                 installer: str,
                 msi_admin: bool = False,
                 cmd_install: str | None = None,
                 cmd_uninstall: str | None = None,
                 lookup_paths: list[str] | None = None,
                 no_remove: bool = False):
        self.name = name
        self.version = version
        self.publisher = publisher
        self.installer = installer
        self.msi_admin = msi_admin
        self.cmd_install = cmd_install
        self.cmd_uninstall = cmd_uninstall
        self.lookup_paths = lookup_paths
        self.no_remove = no_remove

    def execute(self, context: TaskExecutionContext) -> bool:
        logger = context.task.logger
        repo = WindowsInstallsRepository()
        if not self.no_remove:
            success = self._remove_existing_if_present(repo, logger)
            if not success:
                return False
        return self._install(repo, logger)

    def _remove_existing_if_present(self, repo, logger) -> bool:
        old_installation = None
        if self.lookup_paths is not None:
            logger.info("Preferring path lookup")
            matched_path = None
            for path in self.lookup_paths:
                for name in os.listdir(path):
                    if re.match(self.name, name) is not None:
                        matched_path = os.path.join(path, name)
                        break
                if matched_path is not None:
                    break
            if matched_path is not None:
                logger.info("Path matched: %s", matched_path)
                uninstaller = None
                for name in os.listdir(matched_path):
                    if "unins" in name:
                        uninstaller = os.path.join(matched_path, name)
                        break
                if uninstaller is not None:
                    old_installation = WindowsInstallation(
                        name=self.name,
                        version="",
                        publisher="",
                        uninstaller=uninstaller,
                        quiet_uninstaller=determine_quiet_uninstall_command(
                            uninstaller, None
                        )
                    )
                    logger.info("Uninstaller found")
        if old_installation is None:
            logger.info("Searching registry")
            old_installation = self._get_existing_installation(repo)
        if old_installation is not None:
            logger.info("Found old installation, removing")
            success = self._uninstall(repo, logger, old_installation)
            if not success:
                return False
        else:
            logger.info("Old installation not found")
        return True

    def _install(self, repo, logger):
        """Install program"""
        logger.info("Installing %s", self.version)
        success = False
        if self.cmd_install is not None:
            cmd_install = self.cmd_install.replace("$$installer$$",
                                                   self.installer)
            success = subprocess.call(cmd_install) == 0
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
            if (re.fullmatch(self.name, install.name) is not None
                    and (install.publisher == self.publisher or install.publisher is None)):
                return install
        return None

    def _uninstall(self, repo, logger, old_installation: WindowsInstallation):
        """Uninstall old installation"""
        logger.info("Uninstalling %s", old_installation)
        success = False
        if self.cmd_uninstall is not None:
            cmd_uninstall = self.cmd_uninstall.replace("$$uninstaller$$",
                                                     old_installation.uninstaller or "")
            success = subprocess.call(cmd_uninstall) == 0
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
