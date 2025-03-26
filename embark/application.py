"""Application declaration."""

from pathlib import Path

from embark.domain.interfacing.os_provider import OSInterface
from embark.impl import action
from embark.impl.context_factory import CLIContextFactory
from embark.impl.task_loader_repo import TaskLoaderRepository
from embark.output import write_err


class Application:
    """App class."""

    def __init__(
            self,
            os_interface: OSInterface,
            config_file: str,
            file_encoding: str | None = None
    ) -> None:
        """Create application."""
        self.config_file = config_file
        self.context_factory = CLIContextFactory(os_interface)
        self.loader_repo = TaskLoaderRepository()
        self.file_encoding = file_encoding

    def run(self, *, save_report: bool = False) -> int:
        """Run Embark app."""
        report = action.execute_playbook_file(
            self.context_factory, self.loader_repo,
            self.config_file, self.file_encoding
        )
        if not report.is_successful:
            write_err(str(report))
        if save_report:
            Path("embark_report.tmp").write_text(str(report))
        return 0 if report.is_successful else 1
