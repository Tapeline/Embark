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


class AbstractExecutionTarget(Nameable, ABC):
    """Represents a target (action) which must be executed."""

    @abstractmethod
    def execute(self, context: TaskExecutionContext) -> None:
        """Execute action."""


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
        raise AssertionError("Playbook context should not be None")

    @property
    def task_context(self) -> TaskExecutionContext:
        if self._task_context is not None:
            return self._task_context
        raise AssertionError("Task context should not be None")

    @property
    def logger(self) -> AbstractTaskLogger:
        if self._logger is not None:
            return self._logger
        raise AssertionError("Logger should not be None")

    def get_display_name(self):
        return self.name

    def execute(self, context: AbstractPlaybookExecutionContext) -> None:
        """Execute this task"""
        self._playbook_context = context
        self._task_context = self.context_factory.create_task_context(
            self.playbook_context, self
        )
        self._logger = context.playbook.logger.create_child_task_logger(self)
        should_execute = self.criteria.should_execute(self.task_context)
        if not should_execute:
            self.logger.task_skipped()
            return
        self.logger.task_started()
        try:
            self._check_requirements_and_execute()
        except TaskExecutionException as exc:
            self.logger.task_ended(is_successful=False)
            if exc.proceed:
                self.logger.exception(
                    "Exception occurred while task execution: \n%s\n"
                    "Playbook continues",
                    exc.message
                )
            else:
                raise

    def _check_requirements_and_execute(self) -> None:
        """Check task requirements and execute if possible."""
        self._check_requirements()
        self.logger.info("Executing task")
        self._try_to_execute_target()
        self.logger.task_ended(is_successful=True)

    def _check_requirements(self) -> None:
        """Check task requirements."""
        try:  # noqa: WPS229
            for requirement in self.requirements:
                requirement.ensure_requirement_met(self.task_context)
            return  # noqa: TRY300
        except RequirementCannotBeMetException as exc:
            self.logger.task_ended(
                is_successful=False,
                error_message=(
                    "Cannot execute task, because requirements cannot be met"
                )
            )
            should_proceed = self.playbook_context.ask_should_proceed(
                f"Task failed to execute: "
                f"{exc.message}.\n"
                f"Proceed playbook?"
            )
            if should_proceed:
                self.logger.warning("Cancelled, playbook continues")
                raise TaskExecutionException(
                    self.task_context, exc.message, proceed=True
                ) from exc
            self.logger.error("Cannot proceed. Playbook cancelled")
            raise

    def _try_to_execute_target(self) -> None:
        """Try to execute target."""
        try:
            self.target.execute(self.task_context)
        except TaskExecutionException as exc:
            err_msg = (
                f"Task was not executed successfully due to:\n"
                f"{exc!s}"
            )
            self.logger.task_ended(
                is_successful=False,
                error_message=err_msg
            )
            should_proceed = self.playbook_context.ask_should_proceed(
                f"{err_msg}.\nProceed playbook?"
            )
            if should_proceed:
                self.logger.warning("Cancelled, playbook continues")
                exc.proceed = True
            self.logger.error("Cannot proceed. Playbook cancelled")
            raise
