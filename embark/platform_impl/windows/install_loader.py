# This file should be kept as small as possible, because all
# WPS checks are disabled here

import winreg

from attrs import frozen

from embark.domain.interfacing.installs_provider import Installation
from embark.platform_impl.windows.utils import (
    determine_quiet_uninstall_command,
)


@frozen
class WindowsInstallation(Installation):
    uninstaller: str | None = None
    quiet_uninstaller: str | None = None


def get_installation_from_registry(
        reg_base: int, reg_path: str
) -> WindowsInstallation:
    """Create from registry entry."""
    reg = winreg.ConnectRegistry(None, reg_base)
    software_key = winreg.OpenKey(reg, reg_path)
    software_name: str = _get_reg_value_or_none(
        software_key, "DisplayName"
    )
    software_publisher: str = _get_reg_value_or_none(
        software_key, "Publisher"
    )
    software_version = _get_reg_value_or_none(
        software_key, "Version"
    )
    if software_version is None:
        software_version = _get_reg_value_or_none(
            software_key, "DisplayVersion"
        )
    software_major_version: int | None = _get_reg_value_or_none(
        software_key, "VersionMajor"
    )
    software_minor_version: int | None = _get_reg_value_or_none(
        software_key, "VersionMinor"
    )
    software_uninstall: str | None = _get_reg_value_or_none(
        software_key, "UninstallString"
    )
    software_quiet_uninstall: str | None = _get_reg_value_or_none(
        software_key, "QuietUninstallString"
    )
    index = 0
    while True:
        try:  # noqa: WPS229
            key, value, _ = winreg.EnumValue(software_key, index)
            if software_uninstall is None and \
                    "Uninstall" in key and \
                    "Quiet" not in key and \
                    "Silent" not in key:
                software_uninstall = value
            if software_quiet_uninstall is None and \
                    "Uninstall" in key and \
                    "Quiet" in key and \
                    "Silent" in key:
                software_quiet_uninstall = value
            index += 1
        except OSError:
            break
    if software_uninstall is not None:
        software_uninstall = winreg.ExpandEnvironmentStrings(
            software_uninstall
        )
    if software_quiet_uninstall is not None:
        software_quiet_uninstall = winreg.ExpandEnvironmentStrings(
            software_quiet_uninstall
        )
    if software_uninstall is not None:
        software_quiet_uninstall = determine_quiet_uninstall_command(
            software_uninstall, software_quiet_uninstall
        )
    return WindowsInstallation(
        name=software_name,
        version=str(software_version),
        major_version=software_major_version,
        minor_version=software_minor_version,
        publisher=software_publisher,
        quiet_uninstaller=software_quiet_uninstall,
        uninstaller=software_uninstall
    )


def _get_reg_value_or_none(key, name):
    """Wrapper for winreg function"""
    try:
        return winreg.QueryValueEx(key, name)[0]
    except Exception:
        return None
