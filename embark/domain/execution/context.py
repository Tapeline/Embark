"""Provides files related to context."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from embark.domain.interfacing.os_provider import OSInterface
from embark.domain.playbook_logger import AbstractPlaybookLogger

if TYPE_CHECKING:
    from embark.domain.execution.playbook import Playbook
    from embark.domain.tasks.task import Task


class AbstractPlaybookExecutionContext(ABC):
    """Context of current playbook."""

    @property
    @abstractmethod
    def playbook(self) -> "Playbook":
        """Get the playbook."""

    @abstractmethod
    def ask_should_proceed(self, text: str) -> bool:
        """Blocking function which prompts user if he wants to proceed."""

    @abstractmethod
    def file_path(self, path) -> str:
        """Resolve file path (with placeholders)."""

    @abstractmethod
    def create_logger(self) -> AbstractPlaybookLogger:
        """Create logger for this playbook."""

    def variables[T](self, target_obj: T) -> T:  # noqa: WPS111
        """Format object with variables."""
        return self.playbook.variables.format_object(target_obj)

    def set_variable(self, name: str, obj: Any) -> None:
        """Set variable for playbook."""
        self.playbook.variables.vars[name] = obj

    @property
    @abstractmethod
    def os_provider(self) -> OSInterface:
        """Get OS interface."""


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

    @abstractmethod
    def create_playbook_context(
            self,
            playbook: "Playbook"
    ) -> AbstractPlaybookExecutionContext:
        """Create context for provided playbook."""

    @abstractmethod
    def create_task_context(
            self,
            playbook_context: AbstractPlaybookExecutionContext,
            task: "Task"
    ) -> TaskExecutionContext:
        """Create context for provided task."""
