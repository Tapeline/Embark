cleanbuild: clean build


clean:
	rm -r build
	rm -r dist
	mkdir build
	mkdir dist


build:
	build.bat


test:
	poetry run coverage run -m pytest tests


lint:
	poetry run mypy embark
	poetry run ruff check
	poetry run lint-imports
	poetry run flake8 embark tests


all: test lint cleanbuild
