"""Contains generified actions."""

import logging
import sys

from pydantic import ValidationError
from yaml import YAMLError

from embark.impl import config
from embark.domain.config.exceptions import ConfigLoadingException
from embark.domain.config.loader import AbstractTaskLoaderRepository
from embark.domain.tasks.task import AbstractContextFactory


type IsSuccessful = bool


def execute_playbook_file(
        context_factory: AbstractContextFactory,
        loader_repo: AbstractTaskLoaderRepository,
        path: str,
        file_encoding: str | None = None
) -> IsSuccessful:
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
        return False
    except ConfigLoadingException as exception:
        logging.getLogger("Config loader").error(str(exception))
        return False
    except YAMLError as exception:
        print("Error while parsing YAML file:", file=sys.stderr)
        if (
                hasattr(exception, 'problem_mark') and
                hasattr(exception, 'context') and
                hasattr(exception, 'problem')
        ):
            if exception.context is not None:
                print(f"{exception.problem_mark}\n  "
                      f"{exception.problem} {exception.context}"
                      f"\nPlease correct and retry.", file=sys.stderr)
            else:
                print(f"{exception.problem_mark}\n  {exception.problem}"
                      f"\nPlease correct and retry.", file=sys.stderr)
        else:
            print(
                "Something went wrong while parsing yaml file",
                file=sys.stderr
            )
        return False
    return playbook.run()
