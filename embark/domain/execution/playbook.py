"""
Provides objects for executing playbook
"""

import io
import os
import traceback

from embark.domain.config.variables import VariablesEnv
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
                 tasks: list[Task],
                 variables: VariablesEnv | None = None):
        self.name = name
        self.tasks = tasks
        self.context_factory = context_factory
        self.variables: VariablesEnv = variables or VariablesEnv({}, os.environ)
        self.context = context_factory.create_playbook_context(self)
        self.logger = self.context.create_logger()

    def run_tasks(self):
        """Run all tasks sequentially"""
        self.logger.playbook_started()
        for task in self.tasks:
            task.execute(self.context)
        self.logger.playbook_ended(is_successful=True)

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
            self.logger.playbook_ended(
                is_successful=False,
                error_message="Playbook failed: \n%s" % content + "\nPlaybook exited with error"
            )
            return False
