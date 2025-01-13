"""Provides files related to context."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from embark.domain.execution.playbook import Playbook
    from embark.domain.tasks.task import Task


class AbstractPlaybookExecutionContext(ABC):
    """Context of current playbook."""

    @property
    @abstractmethod
    def playbook(self) -> "Playbook":
        """Get the playbook."""
        raise NotImplementedError

    @abstractmethod
    def ask_should_proceed(self, text: str) -> bool:
        """Blocking function which prompts user if he wants to proceed."""
        raise NotImplementedError

    @abstractmethod
    def file_path(self, path) -> str:
        """Resolve file path (with placeholders)."""
        raise NotImplementedError

    def variables[T](self, target_obj: T) -> T:  # noqa: WPS111
        """Format object with variables."""
        return self.playbook.variables.format_object(target_obj)

    def set_variable(self, name: str, obj: Any) -> None:
        """Set variable for playbook."""
        self.playbook.variables.vars[name] = obj


class TaskExecutionContext:
    """Context of current task."""

    def __init__(
            self,
            playbook_context: AbstractPlaybookExecutionContext,
            task: "Task"
    ) -> None:
        """Create task execution context."""
        self.playbook_context = playbook_context
        self.task = task


class AbstractContextFactory(ABC):
    """Factory for contexts."""

    def create_playbook_context(
            self,
            playbook: "Playbook"
    ) -> AbstractPlaybookExecutionContext:
        """Create context for provided playbook."""
        raise NotImplementedError

    def create_task_context(
            self,
            playbook_context: AbstractPlaybookExecutionContext,
            task: "Task"
    ) -> TaskExecutionContext:
        """Create context for provided task."""
        raise NotImplementedError
