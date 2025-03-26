from functools import partial
from types import MappingProxyType
from typing import Final

from customtkinter import CTkFont

LOG_FONT: Final = partial(CTkFont, "Consolas", 14, "normal")
CONSOLE_FONT: Final = partial(CTkFont, "Consolas", 14, "normal")
HEADER_FONT: Final = partial(CTkFont, "TkDefaultFont", 16, "bold")
SUBHEADER_FONT: Final = partial(CTkFont, "TkDefaultFont", 14, "normal")

COPYRIGHT_TEXT: Final = "© Tapeline 2024-2025"

UTIL_WIN_SIZE: Final = (500, 600)
MAIN_WIN_SIZE: Final = (1000, 600)

PAD4: Final = MappingProxyType({"padx": 4, "pady": 4})
PAD8: Final = MappingProxyType({"padx": 8, "pady": 8})
PAD12_8: Final = MappingProxyType({"padx": 12, "pady": 8})
PAD16: Final = MappingProxyType({"padx": 16, "pady": 16})
