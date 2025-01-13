"""Provides objects for task execution."""

import logging
from abc import ABC, abstractmethod
from typing import Sequence

from embark import log_config
from embark.domain.execution.context import (
    TaskExecutionContext,
    AbstractContextFactory,
    AbstractPlaybookExecutionContext,
)
from embark.domain.interfaces import Nameable
from embark.domain.tasks.exception import (
    TaskExecutionException,
    RequirementCannotBeMetException,
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


class Task(Nameable):
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
        self.logger = logging.getLogger(name)
        log_config.setup_default_handlers(self.logger)
        self.context_factory = context_factory
        self.name = name
        self.criteria = criteria or NoExecutionCriteria()
        self.requirements = requirements
        self.target = target

    def get_display_name(self):
        return self.name

    def execute(self, context: AbstractPlaybookExecutionContext) -> bool:
        """Execute this task"""
        task_context = self.context_factory.create_task_context(context, self)
        should_execute = self.criteria.should_execute(task_context)
        if not should_execute:
            self.logger.info("Skipping task")
            return True
        self.logger.info("Executing task")
        should_proceed = self._check_requirements(context, task_context)
        if not should_proceed:
            return False
        is_successful, is_cancelled = self._try_to_execute_target(
            context,
            task_context,
        )
        if not is_successful:
            return False
        if is_cancelled:
            raise TaskExecutionException(task_context, "Cancel")
        self.logger.info("Task successful")
        return True

    def _check_requirements(
            self,
            context: AbstractPlaybookExecutionContext,
            task_context: TaskExecutionContext,
    ) -> bool:
        """Check task requirements."""
        try:
            for requirement in self.requirements:
                requirement.ensure_requirement_met(task_context)
            return True
        except RequirementCannotBeMetException as e:
            self.logger.error(
                "Cannot execute task, because requirements cannot be met"
            )
            should_proceed = context.ask_should_proceed(
                "Task failed to execute. Proceed playbook?"
            )
            if should_proceed:
                self.logger.warning("Cancelled, playbook continues")
                return True
            self.logger.error("Cannot proceed. Playbook cancelled")
            raise e

    def _try_to_execute_target(
            self,
            context: AbstractPlaybookExecutionContext,
            task_context: TaskExecutionContext,
    ) -> tuple[bool, bool]:
        """Try to execute target."""
        cancel = False
        try:
            success = self.target.execute(task_context)
            if not success:
                self.logger.error("Task was not executed successfully")
                should_proceed = context.ask_should_proceed(
                    "Proceed playbook?"
                )
                if should_proceed:
                    self.logger.warning("Cancelled, playbook continues")
                    return True, cancel
                self.logger.error("Cannot proceed. Playbook cancelled")
                cancel = True
        except TaskExecutionException as e:
            self.logger.exception("Unknown exception occurred: %s", str(e))
            should_proceed = context.ask_should_proceed(
                f"Task failed to execute:\n{str(e)}.\nProceed playbook?"
            )
            if should_proceed:
                self.logger.warning("Cancelled, playbook continues")
                return True, cancel
            self.logger.error("Cannot proceed. Playbook cancelled")
            raise e
        return True, False
