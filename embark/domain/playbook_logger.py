from abc import ABC, abstractmethod


class AbstractLogger(ABC):
    @abstractmethod
    def info(self, message, *args):
        raise NotImplementedError

    @abstractmethod
    def warning(self, message, *args):
        raise NotImplementedError

    @abstractmethod
    def error(self, message, *args):
        raise NotImplementedError

    @abstractmethod
    def exception(self, message, *args):
        raise NotImplementedError


class AbstractTaskLogger(AbstractLogger, ABC):
    @abstractmethod
    def task_started(self):
        raise NotImplementedError

    @abstractmethod
    def task_skipped(self):
        raise NotImplementedError

    @abstractmethod
    def task_ended(self, is_successful: bool, error_message: str | None = None):
        raise NotImplementedError


class AbstractPlaybookLogger(AbstractLogger, ABC):
    @abstractmethod
    def playbook_started(self):
        raise NotImplementedError

    @abstractmethod
    def playbook_ended(self, is_successful: bool, error_message: str | None = None):
        raise NotImplementedError

    @abstractmethod
    def create_child_task_logger(self, task) -> AbstractTaskLogger:
        raise NotImplementedError
