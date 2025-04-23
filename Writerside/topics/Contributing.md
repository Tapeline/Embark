# Contributing

Embark is an open-source project, so contributions
are welcome!

> Note that Embark is a windows-only project, so
> its development should also be done on Windows.

## First steps
1. Fork the repo
2. Clone the fork
3. Commit changes
4. Create a pull request
5. You're awesome!


## Running the local copy
> Prerequisites: 
> - installed Python 3.13.2+
> - installed Make

Embark manages dependencies with Poetry. Just install Poetry, then all dependencies:
```shell
pip install poetry
poetry install
```

## Testing

Embark uses following testing and checking tools:
- pytest + pytest-cov
- mypy
- ruff
- wemake-python-styleguide
- import-linter

Testing should be done as follows:
```shell
make test 
make lint
```

## Building

To build Embark, use one of the following commands:
```shell
make build
make clean build
make build-onedir
make clean build-onedir
make clean build build-onedir
```

## Guidelines and standards

There should be 0 warnings and errors by any of tools listed above.

All global warning suppressions must be provided with
reasoning in a nearby comment.

The test coverage should not drop from its existing 
value: [![codecov](https://codecov.io/gh/Tapeline/Embark/branch/master/graph/badge.svg)](https://codecov.io/gh/Tapeline/Embark).
