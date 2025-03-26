import tkinter
from typing import Any, Callable

from typing_extensions import Literal

from .core_rendering import CTkCanvas as CTkCanvas
from .core_rendering import DrawEngine as DrawEngine
from .core_widget_classes import CTkBaseClass as CTkBaseClass
from .theme import ThemeManager as ThemeManager

class CTkProgressBar(CTkBaseClass):
    def __init__(self, master: Any, width: int | None = None, height: int | None = None, corner_radius: int | None = None, border_width: int | None = None, bg_color: str | tuple[str, str] = "transparent", fg_color: str | tuple[str, str] | None = None, border_color: str | tuple[str, str] | None = None, progress_color: str | tuple[str, str] | None = None, variable: tkinter.Variable | None = None, orientation: str = "horizontal", mode: Literal["determinate", "indeterminate"] = "determinate", determinate_speed: float = 1, indeterminate_speed: float = 1, **kwargs) -> None: ...
    def destroy(self) -> None: ...
    def configure(self, require_redraw: bool = False, **kwargs) -> None: ...
    def cget(self, attribute_name: str) -> any: ...
    def set(self, value, from_variable_callback: bool = False) -> None: ...
    def get(self) -> float: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def step(self) -> None: ...
    def bind(self, sequence: str = None, command: Callable = None, add: str | bool = True): ...
    def unbind(self, sequence: str = None, funcid: str = None): ...
    def focus(self): ...
    def focus_set(self): ...
    def focus_force(self): ...
