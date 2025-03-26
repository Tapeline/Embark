"""Provides objects for executing playbook."""

import io
import os
import traceback

from attrs import frozen

from embark.domain.execution.context import AbstractContextFactory
from embark.domain.execution.variables import VariablesEnv
from embark.domain.tasks.exception import TaskExecutionException
from embark.domain.tasks.task import (
    Task,
    TaskReport,
    TaskStatus,
)


@frozen
class PlaybookReport:
    """Contains report about playbook execution status."""

    tasks: list[TaskReport]
    is_successful: bool

    def __str__(self) -> str:
        """String repr of playbook report."""
        return "Success: {}\n{}".format(
            self.is_successful,
            "\n".join(map(str, self.tasks))
        )


class Playbook:  # noqa: WPS230
    """Playbook object which can be executed."""

    def __init__(
            self,
            context_factory: AbstractContextFactory,
            name: str,
            tasks: list[Task],
            variables: VariablesEnv | None = None
    ) -> None:
        """Create playbook entity."""
        self.name = name
        self.tasks = tasks
        self.context_factory = context_factory
        self.variables: VariablesEnv = (
            variables or VariablesEnv({}, dict(os.environ))
        )
        self.context = context_factory.create_playbook_context(self)
        self.logger = self.context.create_logger()
        self.reports: list[TaskReport] = []

    def run(self) -> PlaybookReport:
        """Run all tasks and catch exceptions."""
        try:
            self.run_tasks()
        except TaskExecutionException as exception:
            str_ex = io.StringIO()
            traceback.print_exception(exception, limit=0, file=str_ex)
            exception_content = str_ex.getvalue()
            str_ex.close()
            self.logger.playbook_ended(
                is_successful=False,
                error_message=(
                        f"Playbook failed: \n{exception_content}" +
                        "\nPlaybook exited with error"
                ),
            )
        return self._gen_report()

    def run_tasks(self) -> None:
        """Run all tasks sequentially."""
        self.logger.playbook_started()
        for task in self.tasks:
            self._try_to_execute(task)
        self.logger.playbook_ended(is_successful=True)

    def _try_to_execute(self, task: Task) -> None:
        try:  # noqa: WPS229
            report = task.execute(self.context)
            self.reports.append(report)
        except TaskExecutionException:
            self.reports.append(TaskReport(task, TaskStatus.FAILED))
            raise
        except Exception as exc:
            self.reports.append(TaskReport(task, TaskStatus.FAILED))
            err_msg = (
                f"Task had an unhandled exception:\n"
                f"{exc!s}"
            )
            should_proceed = self.context.ask_should_proceed(
                f"{err_msg}.\nProceed playbook?"
            )
            if should_proceed:
                self.logger.warning("Cancelled, playbook continues")
            self.logger.error("Cannot proceed. Playbook cancelled")
            raise TaskExecutionException(
                self.context_factory.create_task_context(self.context, task),
                str(exc)
            ) from exc

    def _gen_report(self) -> PlaybookReport:
        return PlaybookReport(
            self.reports,
            is_successful=all(
                report.status.is_ok for report in self.reports
            )
        )
