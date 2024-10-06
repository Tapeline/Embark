# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
"""
Provides objects for task execution
"""

import logging
from abc import ABC, abstractmethod
from typing import Sequence

from domain.utils import Interface


class AbstractPlaybookExecutionContext(ABC):
    """
    Context of current playbook
    """
    @abstractmethod
    def ask_should_proceed(self, text: str) -> bool:
        """Blocking function which prompts user if he wants to proceed"""
        raise NotImplementedError

    @abstractmethod
    def file_path(self, path) -> str:
        """Resolve file path (with placeholders)"""
        raise NotImplementedError


class TaskExecutionContext:
    """
    Context of current task
    """
    def __init__(self,
                 playbook_context: AbstractPlaybookExecutionContext,
                 task: "Task"):
        self.playbook_context = playbook_context
        self.task = task


class AbstractContextFactory(ABC):
    """Factory for contexts"""

    def create_playbook_context(self, playbook) -> AbstractPlaybookExecutionContext:
        """Create context for provided playbook"""
        raise NotImplementedError

    def create_task_context(self, playbook_context, task) -> TaskExecutionContext:
        """Create context for provided task"""
        raise NotImplementedError


class Nameable(Interface):
    """Interface which supports getting name"""
    @abstractmethod
    def get_display_name(self) -> str:
        """
        Should return display name.
        Should not be used as a unique name at all costs
        """
        raise NotImplementedError


class AbstractExecutionCriteria(Nameable, ABC):
    """
    Represents a condition under which
    task should or should not be run
    """
    @abstractmethod
    def should_execute(self, context: TaskExecutionContext) -> bool:
        """Determine if task should be executed"""
        raise NotImplementedError


class NoExecutionCriteria(AbstractExecutionCriteria):
    """Dummy criteria which is always true"""
    def should_execute(self, context: TaskExecutionContext) -> bool:
        return True

    def get_display_name(self) -> str:
        return "No criteria"


class AbstractExecutionRequirement(Nameable, ABC):
    """
    Represents a requirement which
    must be met to execute the task.
    Throws RequirementCannotBeMetException if requirement cannot be met
    """
    @abstractmethod
    def ensure_requirement_met(self, context: TaskExecutionContext) -> None:
        """Check if requirement is met and if not - request user action"""
        raise NotImplementedError


class AbstractExecutionTarget(Nameable, ABC):
    """
    Represents a target (action) which must be executed
    """
    @abstractmethod
    def execute(self, context: TaskExecutionContext) -> bool:
        """Execute action"""
        raise NotImplementedError


class Task(Nameable):
    """Represents playbook task"""

    def __init__(self,
                 context_factory: AbstractContextFactory,
                 name: str,
                 criteria: AbstractExecutionCriteria | None,
                 requirements: Sequence[AbstractExecutionRequirement],
                 target: AbstractExecutionTarget):
        self.logger = logging.getLogger(name)
        self.context_factory = context_factory
        self.name = name
        self.criteria = criteria or NoExecutionCriteria()
        self.requirements = requirements
        self.target = target

    def get_display_name(self):
        return self.name

    def execute(self, context: AbstractPlaybookExecutionContext):
        """Execute this task"""
        task_context = self.context_factory.create_task_context(context, self)
        should_execute = self.criteria.should_execute(task_context)
        if not should_execute:
            self.logger.info("Skipping task")
            return
        self.logger.info("Executing task")
        # pylint: disable=import-outside-toplevel
        from domain.tasks.exception import RequirementCannotBeMetException
        try:
            for requirement in self.requirements:
                requirement.ensure_requirement_met(task_context)
        except RequirementCannotBeMetException as e:
            self.logger.error("Cannot execute task, because requirements cannot be met")
            should_proceed = context.ask_should_proceed(
                "Task failed to execute. Proceed playbook or abort?"
            )
            if should_proceed:
                self.logger.warning("Cancelled, playbook continues")
                return
            self.logger.error("Cannot proceed. Playbook cancelled")
            raise e
        from domain.tasks.exception import TaskExecutionException
        try:
            success = self.target.execute(task_context)
            if not success:
                self.logger.error("Task was not executed successfully")
                should_proceed = context.ask_should_proceed("Proceed playbook or abort?")
                if should_proceed:
                    self.logger.warning("Cancelled, playbook continues")
                    return
                self.logger.error("Cannot proceed. Playbook cancelled")
                raise TaskExecutionException(task_context, "Fail")
        except TaskExecutionException as e:
            self.logger.exception("Unknown exception occurred: %s", str(e))
            should_proceed = context.ask_should_proceed(
                f"Task failed to execute:\n{str(e)}.\nProceed playbook or abort?"
            )
            if should_proceed:
                self.logger.warning("Cancelled, playbook continues")
                return
            self.logger.error("Cannot proceed. Playbook cancelled")
            raise e
        self.logger.info("Task successful")
