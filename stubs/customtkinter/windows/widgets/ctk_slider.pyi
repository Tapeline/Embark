import tkinter
from typing import Any, Callable

from .core_rendering import CTkCanvas as CTkCanvas
from .core_rendering import DrawEngine as DrawEngine
from .core_widget_classes import CTkBaseClass as CTkBaseClass
from .theme import ThemeManager as ThemeManager

class CTkSlider(CTkBaseClass):
    def __init__(self, master: Any, width: int | None = None, height: int | None = None, corner_radius: int | None = None, button_corner_radius: int | None = None, border_width: int | None = None, button_length: int | None = None, bg_color: str | tuple[str, str] = "transparent", fg_color: str | tuple[str, str] | None = None, border_color: str | tuple[str, str] = "transparent", progress_color: str | tuple[str, str] | None = None, button_color: str | tuple[str, str] | None = None, button_hover_color: str | tuple[str, str] | None = None, from_: int = 0, to: int = 1, state: str = "normal", number_of_steps: int | None = None, hover: bool = True, command: Callable[[float], Any] | None = None, variable: tkinter.Variable | None = None, orientation: str = "horizontal", **kwargs) -> None: ...
    def destroy(self) -> None: ...
    def configure(self, require_redraw: bool = False, **kwargs) -> None: ...
    def cget(self, attribute_name: str) -> any: ...
    def get(self) -> float: ...
    def set(self, output_value, from_variable_callback: bool = False) -> None: ...
    def bind(self, sequence: str = None, command: Callable = None, add: str | bool = True): ...
    def unbind(self, sequence: str = None, funcid: str = None): ...
    def focus(self): ...
    def focus_set(self): ...
    def focus_force(self): ...
