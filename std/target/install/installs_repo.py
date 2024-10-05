import os.path
import subprocess
import winreg
from abc import ABC, abstractmethod
from typing import Any

import peid


class AbstractInstallation(ABC):
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
    pass


class CannotUninstallQuietlyException(CannotUninstallException):
    pass


class CannotInstallException(Exception):
    pass


class CannotInstallQuietlyException(CannotInstallException):
    pass


class AbstractInstallsRepository(ABC):
    @abstractmethod
    def get_all_installs(self) -> list[AbstractInstallation]:
        raise NotImplementedError

    @abstractmethod
    def uninstall_quietly(self, installation: AbstractInstallation) -> bool:
        raise NotImplementedError

    @abstractmethod
    def uninstall(self, installation: AbstractInstallation) -> bool:
        raise NotImplementedError

    @abstractmethod
    def install_quietly(self, installer_path: str, admin: bool = False) -> bool:
        raise NotImplementedError

    @abstractmethod
    def install(self, installer_path: str, admin: bool = False) -> bool:
        raise NotImplementedError


def determine_quiet_uninstall_command(uninstall: str,
                                      quiet_uninstall: str | None) -> str | None:
    if quiet_uninstall is not None:
        return quiet_uninstall
    if "msiexec" in uninstall.lower():
        # index = uninstall.lower().find("msiexec.exe ") + len("msiexec.exe ")
        # if index == -1:
        #     index = uninstall.lower().find("msiexec ") + len("msiexec ")
        # quiet_uninstall = uninstall[:index] + "/qn " + uninstall[index:]
        quiet_uninstall = uninstall + " /qn"
        return quiet_uninstall
    try:
        uninstall_path = uninstall
        if uninstall.startswith('"'):
            uninstall_path = uninstall[1:-1]
        if _is_inno_setup(uninstall_path):
            return f"{uninstall} /VERYSILENT /SUPPRESSMSGBOXES /NORESTART"
        if _is_nullsoft_installer(uninstall_path):
            return f"{uninstall} /S"
    except:
        return quiet_uninstall
    return quiet_uninstall


def _is_inno_setup(installer: str) -> bool:
    with open(installer, "rb") as f:
        data = f.read()
        return b"Inno Setup" in data


def _is_nullsoft_installer(installer: str) -> bool:
    with open(installer, "rb") as f:
        data = f.read()
        return b"Nullsoft Install System" in data


def determine_quiet_install_command(installer: str, admin: bool = False) -> str | None:
    if installer.endswith(".msi"):
        return f"msiexec {('/a' if admin else '/i')} {installer} /qn"
    if _is_inno_setup(installer):
        return f"{installer} /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-"
    if _is_nullsoft_installer(installer):
        return f"{installer} /S"
    return None


def _get_reg_value_or_none(key, name) -> Any | None:
    try:
        return winreg.QueryValueEx(key, name)[0]
    except Exception:
        return None


class WindowsInstallation(AbstractInstallation):
    @staticmethod
    def from_registry_path(reg_path: str):
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        software_key = winreg.OpenKey(reg, reg_path)
        software_name: str = _get_reg_value_or_none(
            software_key, "DisplayName")
        software_publisher: str = _get_reg_value_or_none(
            software_key, "Publisher")
        software_version: str = _get_reg_value_or_none(
            software_key, "Version")
        if software_version is None:
            software_version = _get_reg_value_or_none(
                software_key, "DisplayVersion")
        software_major_version: int = _get_reg_value_or_none(
            software_key, "VersionMajor")
        software_minor_version: int = _get_reg_value_or_none(
            software_key, "VersionMinor")
        software_uninstall: str = _get_reg_value_or_none(
            software_key, "UninstallString")
        software_quiet_uninstall: str = _get_reg_value_or_none(
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
        # TODO: expand env string here
        if software_quiet_uninstall is None and software_uninstall is not None:
            software_quiet_uninstall = determine_quiet_uninstall_command(
                software_uninstall, software_quiet_uninstall
            )
        return WindowsInstallation(
            name=software_name,
            version=software_version,
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


class WindowsInstallsRepository(AbstractInstallsRepository):
    def _get_all_installs_on_path(self, path) -> list[WindowsInstallation]:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg, path)
        installs = []
        for i in range(winreg.QueryInfoKey(key)[0]):
            software_key_name = winreg.EnumKey(key, i)
            install = WindowsInstallation.from_registry_path(f"{path}\\{software_key_name}")
            if install.name is None or install.version is None:
                continue
            installs.append(install)
        return installs

    def get_all_installs(self) -> list[AbstractInstallation]:
        return self._get_all_installs_on_path(
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ) + self._get_all_installs_on_path(
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        )

    def uninstall_quietly(self, installation: WindowsInstallation) -> bool:
        if installation.quiet_uninstaller is None:
            raise CannotUninstallQuietlyException
        ret_code = subprocess.call(installation.quiet_uninstaller)
        return ret_code == 0

    def uninstall(self, installation: WindowsInstallation) -> bool:
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
