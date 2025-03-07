"""Provides targets and tools for installation management."""

import os
import re
from dataclasses import dataclass

from embark.domain.interfacing.installs_provider import InstallationsInterface
from embark.domain.tasks.task import (
    AbstractExecutionTarget,
    TaskExecutionContext,
)
from embark.platform_impl.windows.exceptions import (
    CannotInstallException,
    CannotInstallQuietlyException,
    CannotUninstallException,
    CannotUninstallQuietlyException,
)
from embark.platform_impl.windows.installs_provider import WindowsInstallation
from embark.platform_impl.windows.utils import (
    determine_quiet_uninstall_command,
)


@dataclass
class InstallTargetParams:
    """DTO."""

    name: str
    version: str | None
    publisher: str | None
    installer: str
    msi_admin: bool = False
    cmd_install: str | None = None
    cmd_uninstall: str | None = None
    lookup_paths: list[str] | None = None
    no_remove: bool = False


# TODO: refactor class in future
class InstallTarget(AbstractExecutionTarget):  # noqa: WPS214
    """Target for installing."""

    def __init__(self, params: InstallTargetParams) -> None:
        """Create target."""
        self.params = params

    def execute(self, context: TaskExecutionContext) -> bool:
        logger = context.task.logger
        params = self._create_params(context)
        repo = context.playbook_context.os_provider.get_install_interface()
        if not params.no_remove:
            success = self._remove_existing_if_present(params, repo, logger)
            if not success:
                return False
        return self._install(params, repo, logger)

    def get_display_name(self) -> str:
        return f"Install {self.params.name} {self.params.version}"

    def _create_params(
            self,
            context: TaskExecutionContext
    ) -> InstallTargetParams:
        """Re-create params with account of variables."""
        return InstallTargetParams(
            **context.playbook_context.playbook.variables.format_object(
                self.params.__dict__
            )
        )

    def _remove_existing_if_present(
            self,
            params: InstallTargetParams,
            repo: InstallationsInterface,
            logger
    ) -> bool:
        """Remove existing installation if present."""
        old_installation = None
        logger.info("Preferring path lookup")
        matched_path = self._try_to_match_lookup_path(params)
        if matched_path is not None:
            old_installation = self._get_installation_by_path(
                params,
                logger,
                matched_path,
                old_installation
            )
        if old_installation is None:
            logger.info("Searching registry")
            old_installation = self._get_existing_installation(params, repo)
        if old_installation is None:
            logger.info("Old installation not found")
            return True
        logger.info("Found old installation, removing")
        return self._uninstall(params, repo, logger, old_installation)

    def _try_to_match_lookup_path(  # noqa: WPS231
            self,
            params: InstallTargetParams
    ) -> str | None:
        """Get uninstaller by lookup path."""
        matched_path = None
        if params.lookup_paths is None:
            return None
        for path in params.lookup_paths:
            for name in os.listdir(path):
                if re.match(params.name, name) is not None:
                    matched_path = os.path.join(path, name)
                    break
            if matched_path is not None:
                break
        return matched_path

    def _get_installation_by_path(
            self,
            params: InstallTargetParams,
            logger,
            matched_path: str,
            old_installation
    ):
        # pylint: disable=missing-function-docstring
        logger.info("Path matched: %s", matched_path)
        uninstaller = None
        for name in os.listdir(matched_path):
            if "unins" in name:
                uninstaller = os.path.join(matched_path, name)
                break
        if uninstaller is not None:
            old_installation = WindowsInstallation(
                name=params.name,
                version="",
                publisher="",
                uninstaller=uninstaller,
                quiet_uninstaller=determine_quiet_uninstall_command(
                    uninstaller, None
                )
            )
            logger.info("Uninstaller found")
        return old_installation

    def _get_existing_installation(self, params, repo):
        """Seek for existing installations of any version"""
        return next(
            (
                install for install in repo.get_all_installs()
                if install.matches(
                    params.name,
                    params.publisher,
                    ignore_version=True
                )
            ),
            None
        )

    def _uninstall(
            self,
            params,
            repo,
            logger,
            old_installation: WindowsInstallation
    ) -> bool:
        """Uninstall old installation"""
        logger.info("Uninstalling %s", old_installation)
        if params.cmd_uninstall is None:
            try:
                repo.uninstall_quietly(old_installation)
            except CannotUninstallQuietlyException:
                logger.error(
                    "Quiet uninstall failed. Trying regular uninstall"
                )
                logger.warning("User action required!")
                try:  # noqa: WPS505
                    repo.uninstall(old_installation)
                except CannotUninstallException:
                    logger.error("Uninstall failed")
                    return False
        else:
            cmd_uninstall = params.cmd_uninstall.replace(
                "$$uninstaller$$",
                old_installation.uninstaller or ""
            )
            if not repo.os_interface.run(cmd_uninstall).is_successful:
                logger.error("Uninstall failed")
                return False
        return True

    def _install(self, params, repo, logger) -> bool:
        """Install program"""
        logger.info("Installing %s", params.version)
        if params.cmd_install is None:
            try:
                repo.install_quietly(
                    params.installer,
                    admin=params.msi_admin
                )
            except CannotInstallQuietlyException:
                logger.error("Quiet install failed. Trying regular install")
                logger.warning("User action required!")
                try:  # noqa: WPS505
                    repo.install(params.installer, admin=params.msi_admin)
                except CannotInstallException:
                    logger.error("Install failed")
                    return False
        else:
            cmd_install = params.cmd_install.replace(
                "$$installer$$",
                params.installer
            )
            return repo.os_interface.run_console(cmd_install).is_successful
        return True
