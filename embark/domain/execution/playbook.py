"""Provides objects for executing playbook."""

import io
import os
import traceback

from embark.domain.execution.variables import VariablesEnv
from embark.domain.tasks.exception import TaskExecutionException
from embark.domain.tasks.task import AbstractContextFactory, Task

type IsSuccessful = bool


class Playbook:
    """Playbook object which can be executed."""

    def __init__(
            self,
            context_factory: AbstractContextFactory,
            name: str,
            tasks: list[Task],
            variables: VariablesEnv | None = None
    ) -> None:
        """Create playbook entity."""
        self.name = name
        self.tasks = tasks
        self.context_factory = context_factory
        self.variables: VariablesEnv = (
                variables or VariablesEnv({}, os.environ)
        )
        self.context = context_factory.create_playbook_context(self)
        self.logger = self.context.create_logger()

    def run_tasks(self) -> None:
        """Run all tasks sequentially."""
        self.logger.playbook_started()
        for task in self.tasks:
            task.execute(self.context)
        self.logger.playbook_ended(is_successful=True)

    def run(self) -> IsSuccessful:
        """Run all tasks and catch exceptions."""
        try:  # noqa: WPS229 (too long try)
            self.run_tasks()
            return True  # noqa: TRY300
        except TaskExecutionException as exception:
            str_ex = io.StringIO()
            traceback.print_exception(exception, limit=0, file=str_ex)
            exception_content = str_ex.getvalue()
            str_ex.close()
            self.logger.playbook_ended(
                is_successful=False,
                error_message=(
                        f"Playbook failed: \n{exception_content}" +
                        "\nPlaybook exited with error"
                ),
            )
            return False
