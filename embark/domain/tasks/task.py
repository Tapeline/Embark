# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
"""
Provides objects for task execution
"""

from abc import ABC, abstractmethod
from typing import Sequence, TYPE_CHECKING

from embark.domain.playbook_logger import AbstractPlaybookLogger, AbstractTaskLogger
from embark.domain.utils import Interface

if TYPE_CHECKING:
    from embark.domain.execution.playbook import Playbook


class AbstractPlaybookExecutionContext(ABC):
    """
    Context of current playbook
    """
    @property
    @abstractmethod
    def playbook(self) -> "Playbook":
        raise NotImplementedError

    @abstractmethod
    def ask_should_proceed(self, text: str) -> bool:
        """Blocking function which prompts user if he wants to proceed"""
        raise NotImplementedError

    @abstractmethod
    def file_path(self, path) -> str:
        """Resolve file path (with placeholders)"""
        raise NotImplementedError

    @abstractmethod
    def create_logger(self) -> AbstractPlaybookLogger:
        raise NotImplementedError

    def variables[T](self, obj: T) -> T:
        return self.playbook.variables.format_object(obj)

    def set_variable(self, name: str, obj) -> None:
        self.playbook.variables.vars[name] = obj


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
        self.name = name
        self.criteria = criteria or NoExecutionCriteria()
        self.requirements = requirements
        self.target = target
        self.context_factory = context_factory
        self.logger: AbstractTaskLogger | None = None

    def get_display_name(self):
        return self.name

    def _check_requirements(self, context, task_context):
        # pylint: disable=import-outside-toplevel
        from embark.domain.tasks.exception import RequirementCannotBeMetException
        try:
            for requirement in self.requirements:
                requirement.ensure_requirement_met(task_context)
            return True
        except RequirementCannotBeMetException as e:
            self.logger.task_ended(
                is_successful=False,
                error_message="Cannot execute task, because requirements cannot be met"
            )
            should_proceed = context.ask_should_proceed(
                "Task failed to execute. Proceed playbook?"
            )
            if should_proceed:
                self.logger.warning("Cancelled, playbook continues")
                return True
            self.logger.error("Cannot proceed. Playbook cancelled")
            raise e

    def execute(
            self,
            context: AbstractPlaybookExecutionContext
    ):
        """Execute this task"""
        task_context = self.context_factory.create_task_context(context, self)
        self.logger = context.playbook.logger.create_child_task_logger(self)
        should_execute = self.criteria.should_execute(task_context)
        if not should_execute:
            self.logger.task_skipped()
            return
        self.logger.task_started()
        should_proceed = self._check_requirements(context, task_context)
        if not should_proceed:
            return False
        # pylint: disable=import-outside-toplevel
        from embark.domain.tasks.exception import TaskExecutionException
        cancel = False
        try:
            success = self.target.execute(task_context)
            if not success:
                self.logger.task_ended(
                    is_successful=False,
                    error_message="Task was not executed successfully"
                )
                should_proceed = context.ask_should_proceed("Proceed playbook?")
                if should_proceed:
                    self.logger.warning("Cancelled, playbook continues")
                    return
                self.logger.error("Cannot proceed. Playbook cancelled")
                cancel = True
        except TaskExecutionException as e:
            self.logger.task_ended(
                is_successful=False,
                error_message="Unknown exception occurred: %s" % str(e)
            )
            should_proceed = context.ask_should_proceed(
                f"Task failed to execute:\n{str(e)}.\nProceed playbook?"
            )
            if should_proceed:
                self.logger.warning("Cancelled, playbook continues")
                return
            self.logger.error("Cannot proceed. Playbook cancelled")
            raise e
        if cancel:
            raise TaskExecutionException(task_context, "Cancel")
        self.logger.task_ended(is_successful=True)
