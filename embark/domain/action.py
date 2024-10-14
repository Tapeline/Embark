"""
Contains generified actions
"""

import logging
import sys

from pydantic import ValidationError
from yaml import YAMLError

from embark.domain.config import config
from embark.domain.config.loader import AbstractTaskLoaderRepository
from embark.domain.tasks.task import AbstractContextFactory


IsSuccessful = bool


def execute_playbook_file(context_factory: AbstractContextFactory,
                          loader_repo: AbstractTaskLoaderRepository,
                          path: str, file_encoding=None) -> IsSuccessful:
    """
    Execute a playbook. Context factory and loader repo concrete
    implementation should be provided in order for generified actions to work
    """
    try:
        playbook = config.load_playbook_from_file(context_factory, loader_repo,
                                                  path, encoding=file_encoding)
    except ValidationError as e:
        logging.getLogger("Config loader").error(str(e))
        return False
    except YAMLError as e:
        print("Error while parsing YAML file:", file=sys.stderr)
        if hasattr(e, 'problem_mark') and hasattr(e, 'context') and hasattr(e, 'problem'):
            if e.context is not None:
                print(f"{e.problem_mark}\n  {e.problem} {e.context}"
                      f"\nPlease correct and retry.", file=sys.stderr)
            else:
                print(f"{e.problem_mark}\n  {e.problem}"
                      f"\nPlease correct and retry.", file=sys.stderr)
        else:
            print("Something went wrong while parsing yaml file", file=sys.stderr)
        return False
    return playbook.run()
