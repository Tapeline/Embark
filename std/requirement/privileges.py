import ctypes
import os

from elevate import elevate

from domain.tasks.exception import RequirementCannotBeMetException
from domain.tasks.task import AbstractExecutionRequirement, TaskExecutionContext


def _is_admin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


class AdminPrivilegesRequirement(AbstractExecutionRequirement):
    def ensure_requirement_met(self, context: TaskExecutionContext) -> None:
        if _is_admin():
            return
        elevate(show_console=False)
        if not _is_admin():
            raise RequirementCannotBeMetException(self, context)

    def get_display_name(self) -> str:
        return "Admin privilege"
