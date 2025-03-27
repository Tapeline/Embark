import os

import customtkinter

from embark.ui.components import logger_base
from embark.ui.frames.logger_frame.frame import LoggerFrame

if __name__ == '__main__':
    os.environ["UI_LOCALE"] = "en"
    logger_base.test_mode = True
    customtkinter.set_appearance_mode("light")
    win = LoggerFrame("UTF-8", "tests/fixtures/test_echo.yml")
    win.run()
