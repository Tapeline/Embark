"""
Provides configuration loading exception
"""


class ConfigLoadingException(Exception):
    """Thrown when config cannot be loaded"""
    def __init__(self, message: str):
        super().__init__()
        self.add_note(message)


class TaskLoadingException(ConfigLoadingException):
    """Thrown when task loader cannot load a task"""


class InvalidConfigException(ConfigLoadingException):
    """Thrown when config format is invalid"""


class LoaderNotFoundException(ConfigLoadingException):
    """Thrown when task loader is not found"""
    def __init__(self, loader_name: str):
        super().__init__(f"Task loader {loader_name} not found")
