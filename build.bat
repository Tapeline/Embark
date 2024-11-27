pyinstaller ^
    --onefile ^
    --add-data "icon.ico;." ^
    --paths .\.venv\Lib\site-packages ^
    --clean ^
    --name embark ^
    --uac-admin ^
    --icon icon.ico ^
    embark/main.py
