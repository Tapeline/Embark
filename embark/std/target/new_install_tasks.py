import os
import re
from contextlib import suppress
from dataclasses import dataclass

from returns.maybe import Maybe
from returns.result import safe

from embark.domain.execution.context import TaskExecutionContext
from embark.domain.tasks.exception import TaskExecutionException
from embark.domain.tasks.task import AbstractExecutionTarget
from embark.platform_impl.windows.exceptions import (
    CannotInstallException,
    CannotInstallQuietlyException,
    CannotUninstallException,
    CannotUninstallQuietlyException,
)
from embark.platform_impl.windows.install_loader import WindowsInstallation
from embark.platform_impl.windows.utils import (
    determine_quiet_uninstall_command,
)
from embark.common.func import (
    first_or_none, do_if_or_else,
)


@dataclass
class InstallTaskData:
    """Context."""

    name: str
    version: str | None
    publisher: str | None
    installer: str
    msi_admin: bool = False
    cmd_install: str | None = None
    cmd_uninstall: str | None = None
    lookup_paths: list[str] | None = None
    no_remove: bool = False

    old_installation: WindowsInstallation | None = None


def _find_by_path(
        ctx: TaskExecutionContext,
        data: InstallTaskData,
) -> Maybe[WindowsInstallation]:
    old_installation = Maybe.from_value(first_or_none(
        first_or_none(
            os.path.join(path, name)
            for name in os.listdir(path)
            if re.match(data.name, name)
        ) for path in data.lookup_paths
    )).bind_optional(lambda matched_path: first_or_none(
        os.path.join(matched_path, name)
        for name in os.listdir(matched_path)
        if "unins" in name
    )).bind_optional(lambda uninstaller: WindowsInstallation(
        name=data.name,
        version="",
        publisher="",
        uninstaller=uninstaller,
        quiet_uninstaller=determine_quiet_uninstall_command(
            uninstaller, None
        )
    )).unwrap()
    if old_installation:
        ctx.task.logger.info("Uninstaller found")
        return Some(old_installation)
    return Nothing


def _find_in_registry(
        ctx: TaskExecutionContext,
        data: InstallTaskData,
) -> WindowsInstallation | None:
    ctx.task.logger.info("Searching registry")
    repo = ctx.playbook_context.os_provider.get_install_interface()
    old_installation = data.old_installation or first_or_none(
        install for install in repo.get_all_installs()
        if install.matches(
            data.name,
            data.publisher,
            ignore_version=True
        )
    )
    return old_installation


@safe
def _regular_uninstall(
        old_installation: WindowsInstallation,
        ctx: TaskExecutionContext,
        data: InstallTaskData
) -> None:
    ctx.task.logger.info("Uninstalling %s", old_installation)
    repo = ctx.playbook_context.os_provider.get_install_interface()
    ctx.task.logger.info(
        "Trying quiet uninstall. Full command: \n%s",
        old_installation.quiet_uninstaller
    )
    with suppress(CannotUninstallQuietlyException):
        repo.uninstall_quietly(old_installation)
        return
    ctx.task.logger.error(
        "Quiet uninstall failed. Trying regular uninstall. "
        "Full command: \n%s",
        old_installation.uninstaller
    )
    ctx.task.logger.warning("User action required!")
    try:
        repo.uninstall(old_installation)
    except CannotUninstallException as exc:
        raise TaskExecutionException(
            ctx, f"Uninstall failed. Detail: \n{exc!s}"
        ) from exc


@safe
def _cmd_uninstall(
        ctx: TaskExecutionContext,
        data: InstallTaskData,
) -> None:
    cmd_uninstall = data.cmd_uninstall.replace(
        "$$uninstaller$$", data.old_installation.uninstaller or ""
    )
    ctx.task.logger.info(
        "Trying custom uninstall command: \n%s", cmd_uninstall
    )
    repo = ctx.playbook_context.os_provider.get_install_interface()
    result = repo.os_interface.run(cmd_uninstall)
    if not result.is_successful:
        raise TaskExecutionException(
            ctx, f"Uninstall failed, return code: {result.return_code}"
        )


def _regular_install(
        ctx: TaskExecutionContext,
        data: InstallTaskData
) -> None:
    ctx.task.logger.info("Installing %s", data.version)
    ctx.task.logger.info(
        "Trying quiet install. Full command: \n%s",
        data.installer
    )
    repo = ctx.playbook_context.os_provider.get_install_interface()
    with suppress(CannotInstallQuietlyException):
        repo.install_quietly(data.installer, admin=data.msi_admin)
        return
    ctx.task.logger.error(
        "Quiet install failed. Trying regular install. "
        "Full command: \n%s",
        data.installer
    )
    ctx.task.logger.warning("User action required!")
    try:
        repo.install(data.installer, admin=data.msi_admin)
    except CannotInstallException as exc:
        raise TaskExecutionException(
            ctx, f"Install failed. Detail: \n{exc!s}"
        ) from exc


def _cmd_install(
        ctx: TaskExecutionContext,
        data: InstallTaskData
) -> None:
    cmd_install = data.cmd_install.replace("$$installer$$", data.installer)
    ctx.task.logger.info(
        "Trying custom install command: \n%s", cmd_install
    )
    repo = ctx.playbook_context.os_provider.get_install_interface()
    result = repo.os_interface.run(cmd_install)
    if not result.is_successful:
        raise TaskExecutionException(
            ctx,  f"Install failed, return code: {result.return_code}"
        )



class _InstallMap(TargetFSMExecutionMap[InstallTaskData]):
    entrypoint = empty_target_state()
    router = Router(
        entrypoint.success(
            _find_by_path,
            "F.container.lookup_paths is not None"
        ),
        entrypoint.success(_find_in_registry),
        _find_by_path.success(_find_in_registry),
        _find_in_registry.success(
            _regular_uninstall,
            "F.container.old_installation is not None",
            "F.container.cmd_uninstall is None"
        ),
        _find_in_registry.success(
            _cmd_uninstall,
            "F.container.cmd_uninstall is not None"
        ),
        _find_in_registry.success(_any_install),
        _cmd_uninstall.success(_any_install),
        _regular_uninstall.success(_any_install),
        _any_install.success(
            _cmd_install,
            "F.container.cmd_install is not None"
        ),
        _any_install.success(_regular_install)
    )
    endpoints = (_regular_install, _cmd_install)


class InstallTarget(AbstractExecutionTarget):
    """Target for installing."""

    def __init__(self, params: InstallTaskData) -> None:
        """Create target."""
        self.params = params

    def execute(self, context: TaskExecutionContext) -> None:
        old_installation = Maybe.from_optional(
            _find_by_path(context, self.params).or_else_call(
                lambda: _find_in_registry(context, self.params)
            )
        )
        old_installation.map(do_if_or_else(
            self.params.cmd_uninstall is not None,
            true=lambda inst: _cmd_uninstall(context, self.params),
            false=lambda inst: _regular_uninstall(
                old_installation, context, self.params
            ),
        ))
        if self.params.cmd_install is not None:
            _cmd_install(context, self.params)
        else:
            _regular_install(context, self.params)


    def get_display_name(self) -> str:
        """Get human-readable name."""
        return f"Install {self.container.name} {self.container.version}"
