import logging

from domain.tasks.exception import TaskExecutionException
from domain.tasks.task import Task, AbstractContextFactory


IsSuccessful = bool


class Playbook:
    def __init__(self,
                 context_factory: AbstractContextFactory,
                 name: str,
                 tasks: list[Task]):
        self.logger = logging.Logger(f"Playbook({name})")
        self.tasks = tasks
        self.context_factory = context_factory
        self.context = context_factory.create_playbook_context(self)

    def run_tasks(self):
        self.logger.info("Starting playbook")
        for task in self.tasks:
            task.execute(self.context)
        self.logger.info("Playbook successfully ended")

    def run(self) -> IsSuccessful:
        try:
            self.run_tasks()
            return True
        except TaskExecutionException as e:
            self.logger.exception("Playbook failed: %s", str(e))
            self.logger.error("Playbook exited with error")
            return False
