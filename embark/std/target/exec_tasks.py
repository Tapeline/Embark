"""Provides targets and tools for executing various commands."""
from embark.domain.tasks.exception import TaskExecutionException
from embark.domain.tasks.task import (
    AbstractExecutionTarget,
    TaskExecutionContext,
)


class RunCommandTarget(AbstractExecutionTarget):
    """Target for command execution."""

    def __init__(self, cmd: str) -> None:
        """Create target."""
        self.cmd = cmd

    def execute(self, context: TaskExecutionContext) -> None:
        cmd = context.playbook_context.playbook.variables.format(self.cmd)
        run_result = context.playbook_context.os_provider.run_console(cmd)
        if not run_result.is_successful:
            raise TaskExecutionException(
                context,
                f"Process failed with exit code: {run_result.return_code}\n"
                f"Full output:\n"
                f"--- stdout ---\n"
                f"{run_result.stdout}\n"
                f"--- stderr ---\n"
                f"{run_result.stderr}"
            )

    def get_display_name(self) -> str:
        return f"Run {self.cmd}"
