"""Provides common interfaces."""

from abc import abstractmethod
from typing import Protocol


class Nameable(Protocol):
    """Interface which supports getting name."""

    @abstractmethod
    def get_display_name(self) -> str:
        """Should return display name. Not a unique id."""
