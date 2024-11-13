# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
"""
Provides tools for managing installations
"""

import subprocess
import winreg
from abc import ABC, abstractmethod
from typing import Sequence

from embark.std.target.install.utils import (determine_quiet_install_command,
                                             determine_quiet_uninstall_command)


class AbstractInstallation(ABC):
    """
    ABC for installation.
    Maybe other OSes apart from Windows will be supported in future
    """

    def __init__(
            self,
            *,
            name: str,
            version: str,
            publisher: str,
            major_version: int | None = None,
            minor_version: int | None = None
    ):
        self.name = name
        self.version = version
        self.publisher = publisher
        self.major_version = major_version
        self.minor_version = minor_version


class CannotUninstallException(Exception):
    """Thrown when uninstall cannot be performed"""


class CannotUninstallQuietlyException(CannotUninstallException):
    """Thrown when silent uninstall cannot be performed"""


class CannotInstallException(Exception):
    """Thrown when install cannot be performed"""


class CannotInstallQuietlyException(CannotInstallException):
    """Thrown when silent install cannot be performed"""


class AbstractInstallsRepository[T: AbstractInstallation](ABC):
    """
    ABC for installs repo.
    Maybe other OSes apart from Windows will be supported in future
    """

    @abstractmethod
    def get_all_installs(self) -> Sequence[T]:
        """List all installations"""
        raise NotImplementedError

    @abstractmethod
    def uninstall_quietly(self, installation: T) -> bool:
        """Try to uninstall existing installation quietly"""
        raise NotImplementedError

    @abstractmethod
    def uninstall(self, installation: T) -> bool:
        """Try to uninstall existing installation"""
        raise NotImplementedError

    @abstractmethod
    def install_quietly(self, installer_path: str, admin: bool = False) -> bool:
        """Try to install quietly"""
        raise NotImplementedError

    @abstractmethod
    def install(self, installer_path: str, admin: bool = False) -> bool:
        """Try to install"""
        raise NotImplementedError


def _get_reg_value_or_none(key, name):
    """Wrapper for winreg function"""
    # pylint: disable=broad-exception-caught
    try:
        return winreg.QueryValueEx(key, name)[0]
    except Exception:
        return None


class WindowsInstallation(AbstractInstallation):
    """Impl of installation on Windows"""

    @staticmethod
    def from_registry_path(reg_path: str, reg_base: int):
        """Create from registry entry"""
        reg = winreg.ConnectRegistry(None, reg_base)
        software_key = winreg.OpenKey(reg, reg_path)
        software_name: str = _get_reg_value_or_none(
            software_key, "DisplayName")
        software_publisher: str = _get_reg_value_or_none(
            software_key, "Publisher")
        software_version = _get_reg_value_or_none(
            software_key, "Version")
        if software_version is None:
            software_version = _get_reg_value_or_none(
                software_key, "DisplayVersion")
        software_major_version: int | None = _get_reg_value_or_none(
            software_key, "VersionMajor")
        software_minor_version: int | None = _get_reg_value_or_none(
            software_key, "VersionMinor")
        software_uninstall: str | None = _get_reg_value_or_none(
            software_key, "UninstallString")
        software_quiet_uninstall: str | None = _get_reg_value_or_none(
            software_key, "QuietUninstallString")
        i = 0
        while True:
            try:
                key, value, _ = winreg.EnumValue(software_key, i)
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
                i += 1
            except OSError:
                break
        if software_uninstall is not None:
            software_uninstall = winreg.ExpandEnvironmentStrings(software_uninstall)
        if software_quiet_uninstall is not None:
            software_quiet_uninstall = winreg.ExpandEnvironmentStrings(software_quiet_uninstall)
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

    def __init__(
            self,
            *,
            name: str,
            version: str,
            publisher: str,
            major_version: int | None = None,
            minor_version: int | None = None,
            quiet_uninstaller: str | None = None,
            uninstaller: str | None = None
    ):
        super().__init__(
            name=name,
            version=version,
            publisher=publisher,
            major_version=major_version,
            minor_version=minor_version
        )
        self.quiet_uninstaller = quiet_uninstaller
        self.uninstaller = uninstaller

    def __repr__(self):
        return f"{self.name} {self.version}"


class WindowsInstallsRepository(AbstractInstallsRepository[WindowsInstallation]):
    """Impl of installation repo on Windows"""

    def _get_all_installs_on_path(self, path,
                                  base=winreg.HKEY_LOCAL_MACHINE) -> list[WindowsInstallation]:
        """Gets all installs in registry folder"""
        try:
            reg = winreg.ConnectRegistry(None, base)
            key = winreg.OpenKey(reg, path)
            installs = []
            for i in range(winreg.QueryInfoKey(key)[0]):
                software_key_name = winreg.EnumKey(key, i)
                install = WindowsInstallation.from_registry_path(
                    f"{path}\\{software_key_name}", base
                )
                if install.name is None:
                    continue
                installs.append(install)
            return installs
        except FileNotFoundError:
            return []

    def get_all_installs(self) -> Sequence[AbstractInstallation]:
        """
        Get all existing installations.
        Windows installations are located under different paths:
        - HKLM/SOFTWARE/WOW6432Node/Microsoft/Windows/CurrentVersion/Uninstall
        - HKLM/SOFTWARE/Microsoft/Windows/CurrentVersion/Uninstall
        - HKCU/SOFTWARE/Microsoft/Windows/CurrentVersion/Uninstall
        """
        return self._get_all_installs_on_path(
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ) + self._get_all_installs_on_path(
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        ) + self._get_all_installs_on_path(
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            base=winreg.HKEY_CURRENT_USER
        )

    def uninstall_quietly(
            self,
            installation: WindowsInstallation
    ) -> bool:
        if installation.quiet_uninstaller is None:
            raise CannotUninstallQuietlyException
        ret_code = subprocess.call(installation.quiet_uninstaller)
        return ret_code == 0

    def uninstall(
            self,
            installation: WindowsInstallation
    ) -> bool:
        if installation.uninstaller is None:
            raise CannotUninstallException
        ret_code = subprocess.call(installation.uninstaller)
        return ret_code == 0

    def install_quietly(self, installer_path: str, admin: bool = False) -> bool:
        cmd = determine_quiet_install_command(installer_path, admin)
        if cmd is None:
            raise CannotInstallQuietlyException
        return subprocess.call(cmd) == 0

    def install(self, installer_path: str, admin: bool = False) -> bool:
        cmd = installer_path
        if installer_path.endswith(".msi"):
            cmd = f"msiexec {('/a' if admin else '/i')} {installer_path}"
        return subprocess.call(cmd) == 0
