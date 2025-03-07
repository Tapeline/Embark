"""Provides criteria which account installed programs."""
from embark.domain.tasks.task import (
    AbstractExecutionCriteria,
    TaskExecutionContext,
)


class ProgramNotInstalledCriteria(AbstractExecutionCriteria):
    """Execute if specific version of specific program is not installed."""

    def __init__(
            self,
            name: str,
            version: str | None,
            publisher: str | None,
            *,
            ignore_version: bool = False
    ) -> None:
        """Create criteria."""
        self.name = name
        self.version = version
        self.publisher = publisher
        self.ignore_version = ignore_version

    def should_execute(self, context: TaskExecutionContext) -> bool:
        name = context.playbook_context.variables(self.name)
        version = context.playbook_context.variables(self.version)
        publisher = context.playbook_context.variables(self.publisher)
        repo = context.playbook_context.os_provider.get_install_interface()
        return not any(
            install.matches(
                name, version, publisher, ignore_version=self.ignore_version
            )
            for install in repo.get_all_installs()
        )

    def get_display_name(self) -> str:
        return (
            f"Program {self.name} {self.version} "
            f"by {self.publisher} not installed"
        )
