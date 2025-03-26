"""Provides loader and tools for ``std.install``."""

from typing import Any, Optional, Self

from pydantic import BaseModel, model_validator

from embark.domain.execution.context import AbstractContextFactory
from embark.domain.tasks.task import Task
from embark.std.criteria.install_criteria import ProgramNotInstalledCriteria
from embark.std.requirement.privileges import AdminPrivilegesRequirement
from embark.std.target.install_tasks import InstallTarget, InstallTargetParams
from embark.use_case.config.loader import AbstractTaskLoader


class TaskModel(BaseModel):
    """Pydantic model for task config."""

    name: str
    publisher: Optional[str] = None
    version: Optional[str] = None
    installer: str
    msi_admin: bool = False
    cmd_install: Optional[str] = None
    cmd_uninstall: Optional[str] = None
    lookup_paths: Optional[list[str]] = None
    no_remove: bool = False
    ignore_version: bool = False

    @model_validator(mode="after")
    def check_install_can_be_found(self) -> Self:
        """Check that enough info provided to find the installation."""
        if (
            (self.publisher is None or self.version is None)
            and self.lookup_paths is None
        ):
            raise ValueError(
                "Either publisher and version "
                "should be provided or lookup_paths"
            )
        return self


class InstallTaskLoader(AbstractTaskLoader):
    """Task loader impl for ``std.install``."""

    name = "std.install"

    def load_task(
            self,
            context_factory: AbstractContextFactory,
            task_name: str,
            task_config: dict[Any, Any]
    ) -> Task:
        """Load task."""
        model = TaskModel(**task_config)

        criteria = ProgramNotInstalledCriteria(
            model.name, model.version, model.publisher,
            ignore_version=model.ignore_version
        )

        requirements = [AdminPrivilegesRequirement()]

        target = InstallTarget(
            InstallTargetParams(
                model.name,
                model.version,
                model.publisher,
                model.installer,
                model.msi_admin,
                model.cmd_install,
                model.cmd_uninstall,
                model.lookup_paths,
                model.no_remove
            )
        )

        return Task(
            context_factory,
            task_name,
            criteria,
            requirements,
            target
        )
