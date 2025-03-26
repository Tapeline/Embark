from .ctk_toplevel import CTkToplevel as CTkToplevel
from .widgets import CTkButton as CTkButton
from .widgets import CTkEntry as CTkEntry
from .widgets import CTkLabel as CTkLabel
from .widgets.font import CTkFont as CTkFont
from .widgets.theme import ThemeManager as ThemeManager

class CTkInputDialog(CTkToplevel):
    def __init__(self, fg_color: str | tuple[str, str] | None = None, text_color: str | tuple[str, str] | None = None, button_fg_color: str | tuple[str, str] | None = None, button_hover_color: str | tuple[str, str] | None = None, button_text_color: str | tuple[str, str] | None = None, entry_fg_color: str | tuple[str, str] | None = None, entry_border_color: str | tuple[str, str] | None = None, entry_text_color: str | tuple[str, str] | None = None, title: str = "CTkDialog", font: tuple | CTkFont | None = None, text: str = "CTkDialog") -> None: ...
    def get_input(self): ...
