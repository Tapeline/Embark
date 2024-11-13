"""
Provides custom UI components
"""

import tkinter


class Button(tkinter.Button):
    """Custom button"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(bg="#365880", fg="#bbbbbb", relief=tkinter.FLAT)
