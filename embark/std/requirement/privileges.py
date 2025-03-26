"""Provides requirements and tools which account privileges."""

import ctypes
import os
from typing import cast

from embark.domain.execution.context import TaskExecutionContext
from embark.domain.tasks.exception import RequirementCannotBeMetException
from embark.domain.tasks.task import AbstractExecutionRequirement


def _is_admin() -> bool:
    """Check if running as admin."""
    if hasattr(os, "getuid"):
        return cast(bool, os.getuid()) == 0
    return cast(bool, ctypes.windll.shell32.IsUserAnAdmin()) != 0


class AdminPrivilegesRequirement(AbstractExecutionRequirement):
    """Require running as admin."""

    def ensure_requirement_met(self, context: TaskExecutionContext) -> None:
        """Check requirement."""
        if not _is_admin():
            raise RequirementCannotBeMetException(self, context)

    def get_display_name(self) -> str:
        """Get human-readable name."""
        return "Admin privilege"
