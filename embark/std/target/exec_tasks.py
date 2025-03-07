"""Provides targets and tools for executing various commands."""


from embark.domain.tasks.task import (
    AbstractExecutionTarget,
    TaskExecutionContext,
)


class RunCommandTarget(AbstractExecutionTarget):
    """Target for command execution."""

    def __init__(self, cmd: str) -> None:
        """Create target."""
        self.cmd = cmd

    def execute(self, context: TaskExecutionContext) -> bool:
        cmd = context.playbook_context.playbook.variables.format(self.cmd)
        run_result = context.playbook_context.os_provider.run(cmd)
        return run_result.is_successful

    def get_display_name(self) -> str:
        return f"Run {self.cmd}"
