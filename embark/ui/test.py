from attrs import frozen

from embark.ui.logger_frame.frame import LoggerFrame

@frozen
class MockTask:
    name: str

    def get_display_name(self):
        return self.name


def main():
    logger = LoggerFrame("UTF-8", ".")
    logger._logger_frame.notify_started(MockTask("My playbook"))
    logger._logger_frame.inform("Hello from playbook!")
    t1 = MockTask("Test task")
    tl1 = logger._logger_frame.create_task_logger(t1)
    tl1.inform("Hello!")
    tl1.notify_skipped()
    t1 = MockTask("Test task")
    tl1 = logger._logger_frame.create_task_logger(t1)
    tl1.inform("Hello!")
    tl1.notify_ended(is_successful=False, error_message="error!")
    t1 = MockTask("Test task")
    tl1 = logger._logger_frame.create_task_logger(t1)
    tl1.inform("Hello!")
    tl1.notify_ended(is_successful=True)
    t1 = MockTask("Test task")
    tl1 = logger._logger_frame.create_task_logger(t1)
    tl1.inform("Hello!")
    tl1.notify_started()
    logger.mainloop()


if __name__ == '__main__':
    main()
