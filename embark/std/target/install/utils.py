"""
Provides utils for installations
"""

import subprocess


def get_current_sid():
    """Get current Windows user SID"""
    sid = [
        c
        for c in subprocess.check_output('whoami /User')
        .decode(errors="ignore").split('\r\n')
        if "S-1-5-" in c
    ][0]
    sid = sid[sid.index("S-1-5-"):]
    return sid


def determine_quiet_uninstall_command(uninstall: str,
                                      quiet_uninstall: str | None) -> str | None:
    """
    Tries to determine quiet uninstallation command
    from regular uninstallation command.
    At the moment supports MSI, NSIS and Inno Setup uninstallers
    """
    if quiet_uninstall is not None and "msiexec" not in uninstall.lower():
        return quiet_uninstall
    if "msiexec" in uninstall.lower():
        if "/x" not in uninstall.lower():
            index = uninstall.lower().find("/i")
            uninstall = uninstall[:index] + "/X" + uninstall[index+2:]
        quiet_uninstall = uninstall + " /passive /norestart"
        return quiet_uninstall
    # pylint: disable=broad-exception-caught
    try:
        uninstall_path = uninstall
        if uninstall.startswith('"'):
            uninstall_path = uninstall[1:-1]
        if _is_inno_setup(uninstall_path):
            return f"{uninstall} /VERYSILENT /SUPPRESSMSGBOXES /NORESTART"
        if _is_nullsoft_installer(uninstall_path):
            return f"{uninstall} /S"
    except Exception:
        return quiet_uninstall
    return quiet_uninstall


def _is_inno_setup(installer: str) -> bool:
    """
    Check if exe was packed with Inno Setup by looking
    for "Inno Setup" string marker in exe
    """
    with open(installer, "rb") as f:
        data = f.read()
        return b"Inno Setup" in data


def _is_nullsoft_installer(installer: str) -> bool:
    """
    Check if exe was packed with NSIS by looking
    for "Nullsoft Install System" string marker in exe
    """
    with open(installer, "rb") as f:
        data = f.read()
        return b"Nullsoft Install System" in data


def determine_quiet_install_command(installer: str, admin: bool = False) -> str | None:
    """
    Tries to determine quiet installation command
    from regular installation command.
    At the moment supports MSI, NSIS and Inno Setup uninstallers
    """
    if installer.endswith(".msi"):
        return f"msiexec {('/A' if admin else '/I')} \"{installer}\" /passive /norestart"
    if _is_inno_setup(installer):
        return f"{installer} /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-"
    if _is_nullsoft_installer(installer):
        return f"{installer} /S"
    return None
