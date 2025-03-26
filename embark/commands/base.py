from abc import ABC, abstractmethod
from argparse import Namespace
from typing import Any, final

from attrs import frozen

from embark.domain.interfacing.installs_provider import InstallationsInterface
from embark.domain.interfacing.os_provider import OSInterface


@final
@frozen
class NoArgs:
    """Blank args class."""


class AbstractCommand[_ArgsT](ABC):
    """ABC for all commands."""

    _args_type: type[_ArgsT]

    def __init__(
            self,
            os_interface: OSInterface[InstallationsInterface[Any]]
    ) -> None:
        """Create command and link os interface."""
        self.os_interface = os_interface

    def __call__(self, args: Namespace) -> int:
        """Parse arguments into the generic namespace."""
        args_dict = vars(args)  # noqa: WPS421
        if "func" in args_dict:
            args_dict.pop("func")
        cmd_args = self._args_type(**args_dict)
        return self._run(cmd_args)

    @abstractmethod
    def _run(self, args: _ArgsT) -> int:
        """Run the command."""
        raise NotImplementedError
