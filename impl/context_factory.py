import time

from domain.tasks.task import AbstractContextFactory, TaskExecutionContext, AbstractPlaybookExecutionContext


class PlaybookExecutionContext(AbstractPlaybookExecutionContext):
    def __init__(self, playbook):
        self.playbook = playbook

    def ask_should_proceed(self, text: str) -> bool:
        time.sleep(0.2)
        print(text)
        answer = input("y/n> ")
        return answer.lower() == "y"

    def file_path(self, path) -> str:
        return path


class ContextFactory(AbstractContextFactory):
    def create_playbook_context(self, playbook) -> AbstractPlaybookExecutionContext:
        return PlaybookExecutionContext(playbook)

    def create_task_context(self, playbook_context, task) -> TaskExecutionContext:
        return TaskExecutionContext(playbook_context, task)
