from embark.domain.execution.context import TaskExecutionContext
from embark.domain.execution.playbook import Playbook
from embark.domain.tasks.task import AbstractExecutionTarget, Task
from embark.platform_impl.windows.os_provider import WindowsInterface
from embark.ui.components.playbook_logger import GUIPlaybookLoggerComponent
from embark.ui.frames.logger_frame.context_factory import GUIContextFactory


class _DummyExecutionTarget(AbstractExecutionTarget):
    def execute(self, context: TaskExecutionContext) -> None:
        raise AssertionError("Should never happen.")

    def get_display_name(self) -> str:
        return "Dummy"


def create_playbook(logger: GUIPlaybookLoggerComponent) -> Playbook:
    """Create test playbook."""
    context_factory = GUIContextFactory(logger, WindowsInterface())
    return Playbook(
        context_factory,
        "Test playbook",
        [
            Task(
                context_factory,
                name="A",
                criteria=None,
                requirements=[],
                target=_DummyExecutionTarget()
            ),
            Task(
                context_factory,
                name="B",
                criteria=None,
                requirements=[],
                target=_DummyExecutionTarget()
            ),
            Task(
                context_factory,
                name="C",
                criteria=None,
                requirements=[],
                target=_DummyExecutionTarget()
            ),
            Task(
                context_factory,
                name="D",
                criteria=None,
                requirements=[],
                target=_DummyExecutionTarget()
            )
        ],
    )
