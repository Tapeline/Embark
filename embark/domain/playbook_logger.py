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

    @abstractmethod
    def start_progress(self, uid: str, title: str):
        raise NotImplementedError

    @abstractmethod
    def set_progress(self, uid: str, progress: float):
        """
        Set progress bar
        :param uid: progress id
        :param progress: [0;1]
        """
        raise NotImplementedError

    @abstractmethod
    def finish_progress(self, uid: str):
        raise NotImplementedError


class AbstractTaskLogger(AbstractLogger, ABC):
    @abstractmethod
    def task_started(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def task_skipped(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def task_ended(
            self,
            is_successful: bool,
            error_message: str | None = None
    ) -> None:
        raise NotImplementedError


class AbstractPlaybookLogger(AbstractLogger, ABC):
    @abstractmethod
    def playbook_started(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def playbook_ended(
            self,
            is_successful: bool,
            error_message: str | None = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_child_task_logger(self, task) -> AbstractTaskLogger:
        raise NotImplementedError
