rm -r build
rm -r dist
pyinstaller --onefile --paths .\.venv\Lib\site-packages --clean --name embark --uac-admin main.py
