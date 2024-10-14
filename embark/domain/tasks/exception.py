"""
Provides exceptions which can occur during playbook execution
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from embark.domain.tasks.task import TaskExecutionContext
    from embark.domain.tasks.task import AbstractExecutionRequirement


class TaskExecutionException(Exception):
    """Base class for execution exceptions"""
    def __init__(self, task_context: "TaskExecutionContext", message: str):
        super().__init__()
        self.task_context = task_context
        self.add_note(message)


class RequirementCannotBeMetException(TaskExecutionException):
    """Thrown when we tried, but anyway the requirement cannot be met"""
    def __init__(self,
                 requirement: "AbstractExecutionRequirement",
                 task_context: "TaskExecutionContext",
                 message: str = "Requirement cannot be met"):
        super().__init__(task_context, message)
        self.add_note(f"Requirement: {requirement.get_display_name()}")
