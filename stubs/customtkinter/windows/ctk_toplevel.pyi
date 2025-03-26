import tkinter

from _typeshed import Incomplete
from customtkinter.windows.widgets.utility.utility_functions import (
    check_kwargs_empty as check_kwargs_empty,
)
from customtkinter.windows.widgets.utility.utility_functions import (
    pop_from_dict_by_set as pop_from_dict_by_set,
)
from packaging import version as version

from .widgets.appearance_mode import (
    CTkAppearanceModeBaseClass as CTkAppearanceModeBaseClass,
)
from .widgets.scaling import CTkScalingBaseClass as CTkScalingBaseClass
from .widgets.theme import ThemeManager as ThemeManager

class CTkToplevel(tkinter.Toplevel, CTkAppearanceModeBaseClass, CTkScalingBaseClass):
    focused_widget_before_widthdraw: Incomplete
    def __init__(self, *args, fg_color: str | tuple[str, str] | None = None, **kwargs) -> None: ...
    def destroy(self) -> None: ...
    def block_update_dimensions_event(self) -> None: ...
    def unblock_update_dimensions_event(self) -> None: ...
    def geometry(self, geometry_string: str = None): ...
    def withdraw(self) -> None: ...
    def iconify(self) -> None: ...
    def resizable(self, width: bool = None, height: bool = None): ...
    def minsize(self, width: Incomplete | None = None, height: Incomplete | None = None) -> None: ...
    def maxsize(self, width: Incomplete | None = None, height: Incomplete | None = None) -> None: ...
    def configure(self, **kwargs) -> None: ...
    def cget(self, attribute_name: str) -> any: ...
    def wm_iconbitmap(self, bitmap: Incomplete | None = None, default: Incomplete | None = None) -> None: ...
