"""
Provides objects for executing playbook
"""

import io
import logging
import traceback

from embark import log_config
from embark.domain.tasks.exception import TaskExecutionException
from embark.domain.tasks.task import Task, AbstractContextFactory


IsSuccessful = bool


class Playbook:
    """
    Playbook object which can be executed
    """
    def __init__(self,
                 context_factory: AbstractContextFactory,
                 name: str,
                 tasks: list[Task]):
        self.logger = logging.getLogger(name)
        log_config.setup_default_handlers(self.logger)
        self.tasks = tasks
        self.context_factory = context_factory
        self.context = context_factory.create_playbook_context(self)

    def run_tasks(self):
        """Run all tasks sequentially"""
        self.logger.info("Starting playbook")
        for task in self.tasks:
            task.execute(self.context)
        self.logger.info("Playbook successfully ended")

    def run(self) -> IsSuccessful:
        """Run all tasks and catch exceptions"""
        try:
            self.run_tasks()
            return True
        except TaskExecutionException as e:
            str_ex = io.StringIO()
            traceback.print_exception(e, limit=0, file=str_ex)
            content = str_ex.getvalue()
            str_ex.close()
            self.logger.error("Playbook failed: \n%s", content)
            self.logger.error("Playbook exited with error")
            return False
