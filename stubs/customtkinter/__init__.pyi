from tkinter.constants import *

from _typeshed import Incomplete

from .windows import CTk as CTk
from .windows import CTkInputDialog as CTkInputDialog
from .windows import CTkToplevel as CTkToplevel
from .windows.widgets import CTkButton as CTkButton
from .windows.widgets import CTkCheckBox as CTkCheckBox
from .windows.widgets import CTkComboBox as CTkComboBox
from .windows.widgets import CTkEntry as CTkEntry
from .windows.widgets import CTkFrame as CTkFrame
from .windows.widgets import CTkLabel as CTkLabel
from .windows.widgets import CTkOptionMenu as CTkOptionMenu
from .windows.widgets import CTkProgressBar as CTkProgressBar
from .windows.widgets import CTkRadioButton as CTkRadioButton
from .windows.widgets import CTkScrollableFrame as CTkScrollableFrame
from .windows.widgets import CTkScrollbar as CTkScrollbar
from .windows.widgets import CTkSegmentedButton as CTkSegmentedButton
from .windows.widgets import CTkSlider as CTkSlider
from .windows.widgets import CTkSwitch as CTkSwitch
from .windows.widgets import CTkTabview as CTkTabview
from .windows.widgets import CTkTextbox as CTkTextbox
from .windows.widgets.core_rendering import CTkCanvas as CTkCanvas
from .windows.widgets.core_rendering import DrawEngine as DrawEngine
from .windows.widgets.core_widget_classes import CTkBaseClass as CTkBaseClass
from .windows.widgets.font import CTkFont as CTkFont
from .windows.widgets.font import FontManager as FontManager
from .windows.widgets.image import CTkImage as CTkImage

__version__: str
_: Incomplete

def set_appearance_mode(mode_string: str): ...
def get_appearance_mode() -> str: ...
def set_default_color_theme(color_string: str): ...
def set_widget_scaling(scaling_value: float): ...
def set_window_scaling(scaling_value: float): ...
def deactivate_automatic_dpi_awareness() -> None: ...
def set_ctk_parent_class(ctk_parent_class) -> None: ...
