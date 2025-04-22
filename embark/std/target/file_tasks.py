"""Provides targets and tools for file management."""

import shutil

from embark.domain.execution.context import TaskExecutionContext
from embark.domain.tasks.exception import TaskExecutionException
from embark.domain.tasks.task import AbstractExecutionTarget


class CopyFileTarget(AbstractExecutionTarget):
    """Target for file copying."""

    def __init__(self, src_file: str, dst_file: str) -> None:
        """Create target."""
        self.src_file = src_file
        self.dst_file = dst_file

    def execute(self, context: TaskExecutionContext) -> None:
        """Run target."""
        formatter = context.playbook_context.playbook.variables.format
        src = context.playbook_context.file_path(formatter(self.src_file))
        dst = context.playbook_context.file_path(formatter(self.dst_file))
        try:
            shutil.copy(src, dst)
        except Exception as exc:
            context.task.logger.exception("File copy error")
            raise TaskExecutionException(
                context, "Failed to copy file"
            ) from exc

    def get_display_name(self) -> str:
        """Get human-readable name."""
        return f"Copy {self.src_file} -> {self.dst_file}"
