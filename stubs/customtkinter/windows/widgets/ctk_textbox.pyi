from typing import Callable

from _typeshed import Incomplete

from .core_rendering import CTkCanvas as CTkCanvas
from .core_rendering import DrawEngine as DrawEngine
from .core_widget_classes import CTkBaseClass as CTkBaseClass
from .ctk_scrollbar import CTkScrollbar as CTkScrollbar
from .font import CTkFont as CTkFont
from .theme import ThemeManager as ThemeManager
from .utility import check_kwargs_empty as check_kwargs_empty
from .utility import pop_from_dict_by_set as pop_from_dict_by_set

class CTkTextbox(CTkBaseClass):
    def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: int | None = None, border_width: int | None = None, border_spacing: int = 3, bg_color: str | tuple[str, str] = "transparent", fg_color: str | tuple[str, str] | None = None, border_color: str | tuple[str, str] | None = None, text_color: str | str | None = None, scrollbar_button_color: str | tuple[str, str] | None = None, scrollbar_button_hover_color: str | tuple[str, str] | None = None, font: tuple | CTkFont | None = None, activate_scrollbars: bool = True, **kwargs) -> None: ...
    def destroy(self) -> None: ...
    def configure(self, require_redraw: bool = False, **kwargs) -> None: ...
    def cget(self, attribute_name: str) -> any: ...
    def bind(self, sequence: str = None, command: Callable = None, add: str | bool = True): ...
    def unbind(self, sequence: str = None, funcid: str = None): ...
    def focus(self): ...
    def focus_set(self): ...
    def focus_force(self): ...
    def insert(self, index, text, tags: Incomplete | None = None): ...
    def get(self, index1, index2: Incomplete | None = None): ...
    def bbox(self, index): ...
    def compare(self, index, op, index2): ...
    def delete(self, index1, index2: Incomplete | None = None): ...
    def dlineinfo(self, index): ...
    def edit_modified(self, arg: Incomplete | None = None): ...
    def edit_redo(self): ...
    def edit_reset(self): ...
    def edit_separator(self): ...
    def edit_undo(self): ...
    def image_create(self, index, **kwargs) -> None: ...
    def image_cget(self, index, option) -> None: ...
    def image_configure(self, index) -> None: ...
    def image_names(self) -> None: ...
    def index(self, i): ...
    def mark_gravity(self, mark, gravity: Incomplete | None = None): ...
    def mark_names(self): ...
    def mark_next(self, index): ...
    def mark_previous(self, index): ...
    def mark_set(self, mark, index): ...
    def mark_unset(self, mark): ...
    def scan_dragto(self, x, y): ...
    def scan_mark(self, x, y): ...
    def search(self, pattern, index, *args, **kwargs): ...
    def see(self, index): ...
    def tag_add(self, tagName, index1, index2: Incomplete | None = None): ...
    def tag_bind(self, tagName, sequence, func, add: Incomplete | None = None): ...
    def tag_cget(self, tagName, option): ...
    def tag_config(self, tagName, **kwargs): ...
    def tag_delete(self, *tagName): ...
    def tag_lower(self, tagName, belowThis: Incomplete | None = None): ...
    def tag_names(self, index: Incomplete | None = None): ...
    def tag_nextrange(self, tagName, index1, index2: Incomplete | None = None): ...
    def tag_prevrange(self, tagName, index1, index2: Incomplete | None = None): ...
    def tag_raise(self, tagName, aboveThis: Incomplete | None = None): ...
    def tag_ranges(self, tagName): ...
    def tag_remove(self, tagName, index1, index2: Incomplete | None = None): ...
    def tag_unbind(self, tagName, sequence, funcid: Incomplete | None = None): ...
    def window_cget(self, index, option) -> None: ...
    def window_configure(self, index, option) -> None: ...
    def window_create(self, index, **kwargs) -> None: ...
    def window_names(self) -> None: ...
    def xview(self, *args): ...
    def xview_moveto(self, fraction): ...
    def xview_scroll(self, n, what): ...
    def yview(self, *args): ...
    def yview_moveto(self, fraction): ...
    def yview_scroll(self, n, what): ...
