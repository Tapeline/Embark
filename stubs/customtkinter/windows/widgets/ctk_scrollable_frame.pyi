import tkinter
from typing import Any

from _typeshed import Incomplete
from typing_extensions import Literal

from .appearance_mode import (
    CTkAppearanceModeBaseClass as CTkAppearanceModeBaseClass,
)
from .core_widget_classes import CTkBaseClass as CTkBaseClass
from .ctk_frame import CTkFrame as CTkFrame
from .ctk_label import CTkLabel as CTkLabel
from .ctk_scrollbar import CTkScrollbar as CTkScrollbar
from .font import CTkFont as CTkFont
from .scaling import CTkScalingBaseClass as CTkScalingBaseClass
from .theme import ThemeManager as ThemeManager

class CTkScrollableFrame(tkinter.Frame, CTkAppearanceModeBaseClass, CTkScalingBaseClass):
    def __init__(self, master: Any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | tuple[str, str] = "transparent", fg_color: str | tuple[str, str] | None = None, border_color: str | tuple[str, str] | None = None, scrollbar_fg_color: str | tuple[str, str] | None = None, scrollbar_button_color: str | tuple[str, str] | None = None, scrollbar_button_hover_color: str | tuple[str, str] | None = None, label_fg_color: str | tuple[str, str] | None = None, label_text_color: str | tuple[str, str] | None = None, label_text: str = "", label_font: tuple | CTkFont | None = None, label_anchor: str = "center", orientation: Literal["vertical", "horizontal"] = "vertical") -> None: ...
    def destroy(self) -> None: ...
    def configure(self, **kwargs) -> None: ...
    def cget(self, attribute_name: str): ...
    def check_if_master_is_canvas(self, widget): ...
    def pack(self, **kwargs) -> None: ...
    def place(self, **kwargs) -> None: ...
    def grid(self, **kwargs) -> None: ...
    def pack_forget(self) -> None: ...
    def place_forget(self, **kwargs) -> None: ...
    def grid_forget(self, **kwargs) -> None: ...
    def grid_remove(self, **kwargs) -> None: ...
    def grid_propagate(self, **kwargs) -> None: ...
    def grid_info(self, **kwargs): ...
    def lift(self, aboveThis: Incomplete | None = None) -> None: ...
    def lower(self, belowThis: Incomplete | None = None) -> None: ...
