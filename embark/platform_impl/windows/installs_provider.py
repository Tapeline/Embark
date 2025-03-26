import winreg
from collections.abc import Sequence

from embark.domain.interfacing.installs_provider import InstallationsInterface
from embark.platform_impl.windows.exceptions import (
    CannotInstallQuietlyException,
    CannotUninstallException,
    CannotUninstallQuietlyException,
    InstallationCommandNotProvidedException,
)
from embark.platform_impl.windows.install_loader import (
    WindowsInstallation,
    get_installation_from_registry,
)
from embark.platform_impl.windows.utils import determine_quiet_install_command


class WindowsInstallationsInterface(
    InstallationsInterface[WindowsInstallation]
):
    """Implementation of Windows software installer interactions."""

    def uninstall_quietly(self, installation: WindowsInstallation) -> None:
        """Uninstall software quietly."""
        if installation.quiet_uninstaller is None:
            raise InstallationCommandNotProvidedException
        result = self.os_interface.run(installation.quiet_uninstaller)
        if not result.is_successful:
            raise CannotUninstallQuietlyException

    def uninstall(self, installation: WindowsInstallation) -> None:
        """Uninstall software."""
        if installation.uninstaller is None:
            raise InstallationCommandNotProvidedException
        result = self.os_interface.run(installation.uninstaller)
        if not result.is_successful:
            raise CannotUninstallException

    def install_quietly(
            self, installer_path: str, *, admin: bool = False
    ) -> None:
        """Install software quietly."""
        cmd = determine_quiet_install_command(installer_path, admin=admin)
        if cmd is None:
            raise InstallationCommandNotProvidedException
        result = self.os_interface.run(cmd)
        if not result.is_successful:
            raise CannotInstallQuietlyException

    def install(self, installer_path: str, *, admin: bool = False) -> None:
        """Install software."""
        cmd = installer_path
        if installer_path.endswith(".msi"):
            cmd = f"msiexec {('/a' if admin else '/i')} {installer_path}"
        result = self.os_interface.run(cmd)
        if not result.is_successful:
            raise CannotInstallQuietlyException

    def get_all_installs(self) -> Sequence[WindowsInstallation]:
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

    def _get_all_installs_on_path(  # noqa: WPS210, WPS231
            self,
            path: str,
            base: int = winreg.HKEY_LOCAL_MACHINE,
    ) -> list[WindowsInstallation]:
        """Gets all installs in registry folder."""
        try:  # noqa: WPS229
            reg = winreg.ConnectRegistry(None, base)
            key = winreg.OpenKey(reg, path)
            installs = []
            for index in range(winreg.QueryInfoKey(key)[0]):
                software_key_name = winreg.EnumKey(key, index)
                install = get_installation_from_registry(
                    base, f"{path}\\{software_key_name}"
                )
                if install.name is None:
                    continue
                installs.append(install)
            return installs  # noqa: TRY300
        except FileNotFoundError:
            return []
