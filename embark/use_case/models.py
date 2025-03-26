"""Provides DTOs and function for loading config from dict."""
from typing import Any

import pydantic
from attrs import frozen

from embark.use_case.config.exceptions import InvalidConfigException


class PlaybookModel(pydantic.BaseModel):
    """Pydantic model for playbook."""

    name: str
    variables: dict[Any, Any] = {}
    tasks: list[dict[Any, Any]]


@frozen
class TaskConfig:
    """Task DTO."""

    task_name: str
    target_type: str
    target_data: dict[Any, Any]


@frozen
class PlaybookConfig:
    """Playbook DTO."""

    name: str
    variables: dict[Any, Any]
    tasks: list[TaskConfig]


def get_task_from_dict(  # noqa: WPS231, WPS238
        task_dict: dict[Any, Any]
) -> TaskConfig:
    """Create task DTO from dict and also perform validation."""
    if not isinstance(task_dict.get("name"), str):
        raise InvalidConfigException("Name field in task not found")
    if len(task_dict) != 2:
        raise InvalidConfigException("Task object should have 2 fields")
    for entry_name, entry_value in task_dict.items():
        if entry_name != "name":
            if not isinstance(entry_value, dict):
                raise InvalidConfigException("Target must be an object")
            return TaskConfig(task_dict["name"], entry_name, entry_value)
    raise InvalidConfigException("Target object not found")


def load_playbook_config(playbook_obj: dict[Any, Any]) -> PlaybookConfig:
    """Load playbook DTO from dict and also perform validation."""
    if not isinstance(playbook_obj, dict):
        raise InvalidConfigException("Playbook must be an object")
    playbook_model = None
    try:
        playbook_model = PlaybookModel(**playbook_obj)
    except pydantic.ValidationError as exc:
        raise InvalidConfigException(
            "Invalid playbook configuration"
        ) from exc
    tasks = list(map(get_task_from_dict, playbook_model.tasks))
    return PlaybookConfig(
        playbook_model.name,
        playbook_model.variables,
        tasks
    )
