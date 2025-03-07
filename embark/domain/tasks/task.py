"""Provides objects for task execution."""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from embark.domain.execution.context import (
    AbstractContextFactory,
    AbstractPlaybookExecutionContext,
    TaskExecutionContext,
)
from embark.domain.interfaces import Nameable
from embark.domain.playbook_logger import AbstractTaskLogger
from embark.domain.tasks.exception import (
    RequirementCannotBeMetException,
    TaskExecutionException,
)


class AbstractExecutionCriteria(Nameable, ABC):
    """A condition under which task should or should not be run."""

    @abstractmethod
    def should_execute(self, context: TaskExecutionContext) -> bool:
        """Determine if task should be executed."""
        raise NotImplementedError


class NoExecutionCriteria(AbstractExecutionCriteria):
    """Dummy criteria which is always true."""

    def should_execute(self, context: TaskExecutionContext) -> bool:
        return True

    def get_display_name(self) -> str:
        return "No criteria"


class AbstractExecutionRequirement(Nameable, ABC):
    """Represents a requirement which must be met to execute the task."""

    @abstractmethod
    def ensure_requirement_met(self, context: TaskExecutionContext) -> None:
        """
        Check if requirement is met and if not - request user action.

        Args:
            context: task execution context

        Throws:
            RequirementCannotBeMetException: if requirement cannot be met

        """
        raise NotImplementedError


class AbstractExecutionTarget(Nameable, ABC):
    """Represents a target (action) which must be executed."""

    @abstractmethod
    def execute(self, context: TaskExecutionContext) -> bool:
        """Execute action."""
        raise NotImplementedError


class Task(Nameable):  # noqa: WPS214
    """Represents playbook task."""

    def __init__(
            self,
            context_factory: AbstractContextFactory,
            name: str,
            criteria: AbstractExecutionCriteria | None,
            requirements: Sequence[AbstractExecutionRequirement],
            target: AbstractExecutionTarget
    ) -> None:
        """Create task entity."""
        self.name = name
        self.criteria = criteria or NoExecutionCriteria()
        self.requirements = requirements
        self.target = target
        self.context_factory = context_factory
        self._playbook_context: AbstractPlaybookExecutionContext | None = None
        self._task_context: TaskExecutionContext | None = None
        self._logger: AbstractTaskLogger | None = None

    @property
    def playbook_context(self) -> AbstractPlaybookExecutionContext:
        if self._playbook_context is not None:
            return self._playbook_context
        raise ValueError("Playbook context is None", self)

    @property
    def task_context(self) -> TaskExecutionContext:
        if self._task_context is not None:
            return self._task_context
        raise ValueError("Task context is None", self)

    @property
    def logger(self) -> AbstractTaskLogger:
        if self._logger is not None:
            return self._logger
        raise ValueError("Logger is None", self)

    def get_display_name(self):
        return self.name

    def execute(self, context: AbstractPlaybookExecutionContext) -> bool:
        """Execute this task"""
        self._playbook_context = context
        self._task_context = self.context_factory.create_task_context(
            self.playbook_context, self
        )
        self._logger = context.playbook.logger.create_child_task_logger(self)
        should_execute = self.criteria.should_execute(self.task_context)
        if not should_execute:
            self.logger.task_skipped()
            return True
        self.logger.task_started()
        should_proceed = self._check_requirements()
        if not should_proceed:
            return False
        self.logger.info("Executing task")
        should_proceed = self._check_requirements()
        if not should_proceed:
            return False
        is_successful, is_cancelled = self._try_to_execute_target()
        if not is_successful:
            return False
        if is_cancelled:
            raise TaskExecutionException(self.task_context, "Cancel")
        self.logger.task_ended(is_successful=True)
        return True

    def _check_requirements(self) -> bool:
        """Check task requirements."""
        try:  # noqa: WPS229
            for requirement in self.requirements:
                requirement.ensure_requirement_met(self.task_context)
            return True  # noqa: TRY300
        except RequirementCannotBeMetException:
            self.logger.task_ended(
                is_successful=False,
                error_message=(
                    "Cannot execute task, because requirements cannot be met"
                )
            )
            should_proceed = self.playbook_context.ask_should_proceed(
                "Task failed to execute. Proceed playbook?"
            )
            if should_proceed:
                self.logger.warning("Cancelled, playbook continues")
                return True
            self.logger.error("Cannot proceed. Playbook cancelled")
            raise

    def _try_to_execute_target(self) -> tuple[bool, bool]:
        """Try to execute target."""
        cancel = False
        # TODO: refactor
        try:  # noqa: WPS229
            success = self.target.execute(self.task_context)
            if not success:
                self.logger.task_ended(
                    is_successful=False,
                    error_message="Task was not executed successfully"
                )
                should_proceed = self.playbook_context.ask_should_proceed(
                    "Proceed playbook?"
                )
                if should_proceed:
                    self.logger.warning("Cancelled, playbook continues")
                    return True, cancel
                self.logger.error("Cannot proceed. Playbook cancelled")
                cancel = True
        except TaskExecutionException as exc:
            self.logger.task_ended(
                is_successful=False,
                error_message=f"Unknown exception occurred: {exc!s}"
            )
            should_proceed = self.playbook_context.ask_should_proceed(
                f"Task failed to execute:\n{exc!s}.\nProceed playbook?"
            )
            if should_proceed:
                self.logger.warning("Cancelled, playbook continues")
                return True, cancel
            self.logger.error("Cannot proceed. Playbook cancelled")
            raise
        return True, False
