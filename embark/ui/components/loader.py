from enum import Enum
from tkinter import Widget
from types import MappingProxyType
from typing import Final

from customtkinter import CTkImage, CTkLabel
from PIL import Image

from embark.resources import get_resource


class LoaderState(Enum):
    """State of loader."""

    UNKNOWN = 0
    LOADING = 1
    SKIPPED = 2
    FAILED = 3
    OK = 4


_LOADER_ANIMATIONS: Final = MappingProxyType({
    LoaderState.UNKNOWN: [
        CTkImage(
            light_image=Image.open(
                get_resource("embark/ui/res/icon_unknown.png")
            )
        )
    ],
    LoaderState.LOADING: [
        CTkImage(
            light_image=Image.open(
                get_resource("embark/ui/res/icon_wait_0.png")
            )
        ),
        CTkImage(
            light_image=Image.open(
                get_resource("embark/ui/res/icon_wait_1.png")
            )
        ),
        CTkImage(
            light_image=Image.open(
                get_resource("embark/ui/res/icon_wait_2.png")
            )
        ),
        CTkImage(
            light_image=Image.open(
                get_resource("embark/ui/res/icon_wait_3.png")
            )
        )
    ],
    LoaderState.SKIPPED: [
        CTkImage(
            light_image=Image.open(
                get_resource("embark/ui/res/icon_skip.png")
            )
        )
    ],
    LoaderState.FAILED: [
        CTkImage(
            light_image=Image.open(
                get_resource("embark/ui/res/icon_err.png")
            )
        )
    ],
    LoaderState.OK: [
        CTkImage(
            light_image=Image.open(
                get_resource("embark/ui/res/icon_ok.png")
            )
        )
    ],
})


class LoaderIcon(CTkLabel):
    """Component for displaying states."""

    _animate_delay_ms: int = 200

    def __init__(self, parent: Widget) -> None:
        """Create component."""
        self._state = LoaderState.UNKNOWN
        self._current = 0
        self._current_anim = _LOADER_ANIMATIONS[self._state]
        super().__init__(
            parent,
            image=self._current_anim[self._current],
            text=""
        )
        self.after(self._animate_delay_ms, self._animate)

    @property
    def state(self) -> LoaderState:
        """Get loader state."""
        return self._state

    @state.setter
    def state(self, new_state: LoaderState) -> None:
        """Set loader state."""
        self._current = 0
        self._state = new_state
        self._update()

    def _update(self) -> None:
        self._current_anim = _LOADER_ANIMATIONS[self._state]
        self.configure(
            image=self._current_anim[self._current],
            require_redraw=True
        )

    def _animate(self) -> None:
        if self._current + 1 >= len(self._current_anim):
            self._current = 0
        else:
            self._current += 1
        self._update()
        self.after(self._animate_delay_ms, self._animate)
