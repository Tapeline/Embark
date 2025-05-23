"""Provides exceptions which can occur during playbook execution."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from embark.domain.execution.context import TaskExecutionContext
    from embark.domain.tasks.task import AbstractExecutionRequirement


class TaskExecutionException(Exception):
    """Base class for execution exceptions."""

    def __init__(
            self,
            task_context: "TaskExecutionContext",
            message: str,
            *,
            proceed: bool = False
    ) -> None:
        """Create exception."""
        super().__init__()
        self.task_context = task_context
        self.proceed = proceed
        self.message = message
        self.add_note(message)

    def __str__(self) -> str:
        """Get message."""
        return self.message


class RequirementCannotBeMetException(TaskExecutionException):
    """Thrown when we tried, but anyway the requirement cannot be met."""

    def __init__(
            self,
            requirement: "AbstractExecutionRequirement",
            task_context: "TaskExecutionContext",
            message: str = "Requirement cannot be met"
    ) -> None:
        """Create exception."""
        super().__init__(task_context, message)
        self.add_note(f"Requirement: {requirement.get_display_name()}")
