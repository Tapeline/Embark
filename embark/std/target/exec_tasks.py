"""
Provides targets and tools for executing various commands
"""

import subprocess

from embark.domain.tasks.task import AbstractExecutionTarget, TaskExecutionContext


class RunCommandTarget(AbstractExecutionTarget):
    """Target for command execution"""
    def __init__(self, cmd: str):
        self.cmd = cmd

    def execute(self, context: TaskExecutionContext) -> bool:
        return subprocess.call(self.cmd) == 0

    def get_display_name(self) -> str:
        return f"Run {self.cmd}"
