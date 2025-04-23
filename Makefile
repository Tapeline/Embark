clean:
	del /S /q dist
	del /S /q build


build:
	build.bat


build-onedir:
	build-onedir.bat
	del /S /q dist\\embark-unpacked.zip
	powershell Compress-Archive dist/embark dist/embark-unpacked.zip


test:
	poetry run coverage run -m pytest tests


lint:
	poetry run mypy embark
	poetry run ruff check
	poetry run lint-imports
	poetry run flake8 embark tests


all: test lint clean build


.PHONY: all test clean lint build build-onedir
