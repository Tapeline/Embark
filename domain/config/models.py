import pydantic
from pydantic import BaseModel

from domain.config.exceptions import InvalidConfigException


class PlaybookModel(BaseModel):
    name: str
    tasks: list[dict]


class TaskConfig:
    def __init__(self, task_name: str, target_type: str, target_data: dict):
        self.task_name = task_name
        self.target_type = target_type
        self.target_data = target_data


class PlaybookConfig:
    def __init__(self, name: str, tasks: list[TaskConfig]):
        self.name = name
        self.tasks: list[TaskConfig] = tasks


def get_task_from_dict(task_dict: dict) -> TaskConfig:
    if not isinstance(task_dict.get("name"), str):
        raise InvalidConfigException("Name field in task not found")
    if len(task_dict) != 2:
        raise InvalidConfigException("Task object should have 2 fields")
    for k, v in task_dict.items():
        if k not in {"name"}:
            if not isinstance(v, dict):
                raise InvalidConfigException("Target must be an object")
            return TaskConfig(task_dict["name"], k, v)
    raise InvalidConfigException("Target object not found")


def load_playbook_config(playbook_obj) -> PlaybookConfig:
    if not isinstance(playbook_obj, dict):
        raise InvalidConfigException("Playbook must be an object")
    playbook_model = None
    try:
        playbook_model = PlaybookModel(**playbook_obj)
    except pydantic.ValidationError as e:
        raise InvalidConfigException("Invalid playbook configuration") from e
    tasks = list(map(get_task_from_dict, playbook_model.tasks))
    return PlaybookConfig(playbook_model.name, tasks)
