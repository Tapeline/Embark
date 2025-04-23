poetry run pyinstaller ^
    --onedir ^
    --noconfirm ^
    --add-data "icon.ico;." ^
    --add-data "embark/ui/res;embark/ui/res" ^
    --paths .\.venv\Lib\site-packages ^
    --hiddenimport tkinter.ttk ^
    --hiddenimport tkkthemes ^
    --clean ^
    --name embark ^
    --uac-admin ^
    --icon icon.ico ^
    embark/main.py
