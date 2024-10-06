"""
Provides targets and tools for file management
"""

import os.path
import shutil

from domain.tasks.task import AbstractExecutionTarget, TaskExecutionContext


class CopyFileTarget(AbstractExecutionTarget):
    """Target for file copying"""
    def __init__(self, src_file: str, dst_file: str):
        self.src_file = src_file
        self.dst_file = dst_file

    def execute(self, context: TaskExecutionContext) -> bool:
        src = context.playbook_context.file_path(self.src_file)
        dst = context.playbook_context.file_path(self.dst_file)
        shutil.copy(src, dst)
        return os.path.exists(self.dst_file)

    def get_display_name(self) -> str:
        return f"Copy {self.src_file} -> {self.dst_file}"
