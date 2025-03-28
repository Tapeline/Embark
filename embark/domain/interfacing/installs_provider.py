import re
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING, Self

from attrs import frozen

if TYPE_CHECKING:
    from embark.domain.interfacing.os_provider import OSInterface


@frozen
class Installation:
    """Represents a software installation in the system."""

    name: str
    version: str
    publisher: str
    major_version: int | None = None
    minor_version: int | None = None

    def matches(
            self,
            name: str | None,
            publisher: str | None,
            version: str | None = None,
            *,
            ignore_version: bool = False
    ) -> bool:
        """Check if this installation matches the parameters."""
        return (
            re.fullmatch(name or "", self.name) is not None  # noqa: WPS222
            and (
                publisher == self.publisher or
                re.fullmatch(publisher or "", self.publisher or "")
                or self.publisher is None
            )
            and (self.version == version or ignore_version)
        )

    def __str__(self) -> str:
        """Convert to readable representation."""
        return f"{self.publisher}/{self.name}:{self.version}"


class InstallationsInterface[Install_T: Installation](ABC):
    """Provides methods for working with installations."""

    def __init__(self, os_interface: "OSInterface[Self]") -> None:
        """Create interface."""
        self.os_interface = os_interface

    @abstractmethod
    def get_all_installs(self) -> Sequence[Install_T]:
        """List all installations."""

    @abstractmethod
    def uninstall_quietly(self, installation: Install_T) -> None:
        """Try to uninstall existing installation quietly."""

    @abstractmethod
    def uninstall(self, installation: Install_T) -> None:
        """Try to uninstall existing installation."""

    @abstractmethod
    def install_quietly(
            self,
            installer_path: str,
            *,
            admin: bool = False
    ) -> None:
        """Try to install quietly."""

    @abstractmethod
    def install(self, installer_path: str, *, admin: bool = False) -> None:
        """Try to install."""
