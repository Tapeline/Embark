"""Contains criteria related to logic operations."""

from embark.domain.execution.context import TaskExecutionContext
from embark.domain.tasks.task import AbstractExecutionCriteria


class AndCriteria(AbstractExecutionCriteria):
    """Logical AND criteria."""

    def __init__(self, *criteria: AbstractExecutionCriteria | None) -> None:
        """Create criteria."""
        self.criteria = [crit for crit in criteria if crit is not None]

    def should_execute(self, context: TaskExecutionContext) -> bool:
        """Check criteria."""
        return all(
            criteria.should_execute(context)
            for criteria in self.criteria
        )

    def get_display_name(self) -> str:
        """Get human-readable name."""
        return " and ".join(
            f"({criteria.get_display_name()})"
            for criteria in self.criteria
        )


class OrCriteria(AbstractExecutionCriteria):
    """Logical OR criteria."""

    def __init__(self, *criteria: AbstractExecutionCriteria) -> None:
        """Create criteria."""
        self.criteria = [crit for crit in criteria if crit is not None]

    def should_execute(self, context: TaskExecutionContext) -> bool:
        """Check criteria."""
        return any(
            criteria.should_execute(context)
            for criteria in self.criteria
        )

    def get_display_name(self) -> str:
        """Get human-readable name."""
        return " or ".join(
            f"({criteria.get_display_name()})"
            for criteria in self.criteria
        )
