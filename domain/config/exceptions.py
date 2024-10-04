class ConfigLoadingException(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.add_note(message)


class TaskLoadingException(ConfigLoadingException):
    pass


class InvalidConfigException(ConfigLoadingException):
    pass


class LoaderNotFoundException(ConfigLoadingException):
    def __init__(self, loader_name: str):
        super().__init__(f"Task loader {loader_name} not found")

