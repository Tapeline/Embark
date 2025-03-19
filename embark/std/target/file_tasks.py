"""Provides targets and tools for file management."""

import shutil

from embark.domain.tasks.exception import TaskExecutionException
from embark.domain.tasks.task import (
    AbstractExecutionTarget,
    TaskExecutionContext,
)


class CopyFileTarget(AbstractExecutionTarget):
    """Target for file copying."""

    def __init__(self, src_file: str, dst_file: str) -> None:
        """Create target."""
        self.src_file = src_file
        self.dst_file = dst_file

    def execute(self, context: TaskExecutionContext) -> None:
        src = context.playbook_context.playbook.variables.format(self.src_file)
        dst = context.playbook_context.playbook.variables.format(self.dst_file)
        src = context.playbook_context.file_path(src)
        dst = context.playbook_context.file_path(dst)
        try:
            shutil.copy(src, dst)
        except Exception as exc:
            context.task.logger.exception("File copy error", exc)
            raise TaskExecutionException(
                context, "Failed to copy file"
            ) from exc

    def get_display_name(self) -> str:
        return f"Copy {self.src_file} -> {self.dst_file}"
