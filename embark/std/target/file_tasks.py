"""Provides targets and tools for file management."""

import os.path
import shutil

from embark.domain.tasks.task import AbstractExecutionTarget, TaskExecutionContext


class CopyFileTarget(AbstractExecutionTarget):
    """Target for file copying."""

    def __init__(self, src_file: str, dst_file: str) -> None:
        """Create target."""
        self.src_file = src_file
        self.dst_file = dst_file

    def execute(self, context: TaskExecutionContext) -> bool:
        src = context.playbook_context.playbook.variables.format(self.src_file)
        dst = context.playbook_context.playbook.variables.format(self.dst_file)
        src = context.playbook_context.file_path(src)
        dst = context.playbook_context.file_path(dst)
        try:
            shutil.copy(src, dst)
        except FileNotFoundError as exc:
            context.task.logger.exception("File not found", exc)
            return False
        return os.path.exists(dst)

    def get_display_name(self) -> str:
        return f"Copy {self.src_file} -> {self.dst_file}"
