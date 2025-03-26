"""Contains generified actions."""

import logging
import os

from pydantic import ValidationError
from yaml import YAMLError

from embark.domain.execution.context import AbstractContextFactory
from embark.domain.execution.playbook import PlaybookReport
from embark.impl import config
from embark.output import write_err
from embark.use_case.config.exceptions import ConfigLoadingException
from embark.use_case.config.loader import AbstractTaskLoaderRepository


def execute_playbook_file(
        context_factory: AbstractContextFactory,
        loader_repo: AbstractTaskLoaderRepository,
        path: str,
        file_encoding: str | None = None
) -> PlaybookReport:
    """Execute a playbook."""
    try:
        playbook = config.load_playbook_from_file(
            context_factory,
            loader_repo,
            path,
            encoding=file_encoding
        )
    except ValidationError as exception:
        logging.getLogger("Config loader").error(str(exception))
        return PlaybookReport([], is_successful=False)
    except ConfigLoadingException as exception:
        logging.getLogger("Config loader").error(str(exception))
        return PlaybookReport([], is_successful=False)
    except YAMLError as exception:
        write_err("Error while parsing YAML file:")
        if (
                hasattr(exception, "problem_mark") and
                hasattr(exception, "context") and
                hasattr(exception, "problem")
        ):
            write_err(
                f"{exception.problem_mark}\n  "
                f"{exception.problem} {exception.context}\n"
                f"Please correct and retry."
            )
        else:
            write_err("Something went wrong while parsing yaml file")
        return PlaybookReport([], is_successful=False)
    os.chdir(os.path.dirname(os.path.abspath(path)))
    return playbook.run()
