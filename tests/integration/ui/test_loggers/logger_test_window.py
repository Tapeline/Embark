import threading

import customtkinter
from customtkinter import CTk

from embark.ui.components import logger_base
from embark.ui.components.loader import LoaderIcon
from embark.ui.components.playbook_logger import GUIPlaybookLoggerComponent
from tests.integration.ui.test_loggers.playbook_fixtures import (
    create_playbook
)


class LoggerTestWindowA(CTk):
    """Testing components."""

    def __init__(self) -> None:
        """Create window."""
        super().__init__()
        LoaderIcon.no_anim = True
        self.title("Logger test")
        self.logger = GUIPlaybookLoggerComponent(self)
        self.playbook = create_playbook(self.logger)
        self.logger.pack(fill="both", expand=True)
        self.geometry("800x800")

    def run(self) -> None:
        """Run test scenario."""
        self.logger.notify_started(self.playbook)

        task_a = self.logger.create_task_logger(self.playbook.tasks[0])
        task_a.inform("Information message %s", "Test")
        task_a.warning("Warning message %s", "Test")
        task_a.error("Error message %s", "Test")
        task_a.exception("Exception message %s", "Test")
        task_a.start_progress("0", "Test progress")
        task_a.set_progress("0", 0.75)
        task_a.notify_ended(is_successful=True)

        task_b = self.logger.create_task_logger(self.playbook.tasks[1])
        task_b.start_progress("1", "Test progress")
        task_b.finish_progress("1")
        task_b.notify_skipped()

        task_c = self.logger.create_task_logger(self.playbook.tasks[2])
        task_c.notify_ended(is_successful=False, error_message="Error!")

        task_d = self.logger.create_task_logger(self.playbook.tasks[3])
        task_d.notify_started()

        self.logger.notify_ended(is_successful=True)
        self.mainloop()


if __name__ == '__main__':  # pragma: no cover
    logger_base.test_mode = True
    customtkinter.set_appearance_mode("light")
    win = LoggerTestWindowA()
    win.run()
