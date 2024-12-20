pyinstaller ^
    --onefile ^
    --add-data "icon.ico;." ^
    --paths .\.venv\Lib\site-packages ^
    --hiddenimport tkinter.ttk ^
    --hiddenimport tkkthemes ^
    --clean ^
    --name embark ^
    --uac-admin ^
    --icon icon.ico ^
    embark/main.py
