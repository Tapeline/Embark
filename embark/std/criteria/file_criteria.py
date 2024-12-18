"""
Provides criteria which account files
"""

import os.path

from embark.domain.tasks.task import AbstractExecutionCriteria, TaskExecutionContext


class FileCriteria(AbstractExecutionCriteria):
    """Generic file criteria which checks if file is present or not"""
    def __init__(self, file_path: str, should_exist: bool):
        self.file_path = file_path
        self.should_exist = should_exist

    def should_execute(self, context: TaskExecutionContext) -> bool:
        return os.path.exists(
            context.playbook_context.file_path(self.file_path)
        ) == self.should_exist

    def get_display_name(self):
        return f"File {self.file_path} {'exists' if self.should_exist else 'does not exist'}"


class FileExistsCriteria(FileCriteria):
    """Execute if file exists"""
    def __init__(self, file_path: str):
        super().__init__(file_path, should_exist=True)


class FileDoesNotExistCriteria(FileCriteria):
    """Execute if file does not exist"""
    def __init__(self, file_path: str):
        super().__init__(file_path, should_exist=False)
