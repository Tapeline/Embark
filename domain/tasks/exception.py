from domain.tasks.task import TaskExecutionContext, AbstractExecutionRequirement


class TaskExecutionException(Exception):
    def __init__(self, task_context: TaskExecutionContext, message: str):
        super().__init__()
        self.task_context = task_context
        self.add_note(message)


class RequirementCannotBeMetException(TaskExecutionException):
    def __init__(self,
                 requirement: AbstractExecutionRequirement,
                 task_context: TaskExecutionContext,
                 message: str = "Requirement cannot be met"):
        super().__init__(task_context, message)
        self.add_note(f"Requirement: {requirement.get_display_name()}")
