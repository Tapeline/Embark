from embark.domain.tasks.task import AbstractExecutionCriteria, TaskExecutionContext


class AndCriteria(AbstractExecutionCriteria):
    """Logical AND criteria"""

    def __init__(self, *criteria):
        self.criteria = criteria

    def should_execute(self, context: TaskExecutionContext) -> bool:
        return all(criteria.should_execute(context) for criteria in self.criteria)

    def get_display_name(self):
        return " and ".join(f"({criteria.get_display_name()})" for criteria in self.criteria)


class OrCriteria(AbstractExecutionCriteria):
    """Logical OR criteria"""

    def __init__(self, *criteria):
        self.criteria = criteria

    def should_execute(self, context: TaskExecutionContext) -> bool:
        return any(criteria.should_execute(context) for criteria in self.criteria)

    def get_display_name(self):
        return " or ".join(f"({criteria.get_display_name()})" for criteria in self.criteria)
