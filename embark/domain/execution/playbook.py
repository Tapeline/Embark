"""Provides objects for executing playbook."""

import io
import logging
import os
import traceback

from embark import log_config
from embark.domain.execution.variables import VariablesEnv
from embark.domain.tasks.exception import TaskExecutionException
from embark.domain.tasks.task import Task, AbstractContextFactory


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
        self.logger = logging.getLogger(name)
        log_config.setup_default_handlers(self.logger)
        self.tasks = tasks
        self.context_factory = context_factory
        self.variables: VariablesEnv = (
                variables or VariablesEnv({}, os.environ)
        )
        self.context = context_factory.create_playbook_context(self)

    def run_tasks(self) -> None:
        """Run all tasks sequentially."""
        self.logger.info("Starting playbook")
        for task in self.tasks:
            task.execute(self.context)
        self.logger.info("Playbook successfully ended")

    def run(self) -> IsSuccessful:
        """Run all tasks and catch exceptions."""
        try:  # noqa: WPS229 (too long try)
            self.run_tasks()
            return True
        except TaskExecutionException as exception:
            str_ex = io.StringIO()
            traceback.print_exception(exception, limit=0, file=str_ex)
            exception_content = str_ex.getvalue()
            str_ex.close()
            self.logger.error("Playbook failed: \n%s", exception_content)
            self.logger.error("Playbook exited with error")
            return False
