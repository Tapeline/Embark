<img width="100%" src=".assets/embark-plate.png"/>

![only for windows](https://img.shields.io/badge/os-windows-blue)
![python 3.12+](https://img.shields.io/badge/python-3.12+-blue)
[![License](https://img.shields.io/badge/license-GNU%20GPLv3-green)](./LICENSE)

[![codecov](https://codecov.io/gh/Tapeline/Embark/branch/master/graph/badge.svg)](https://codecov.io/gh/Tapeline/Embark)
[![import-linter](https://img.shields.io/badge/import%20linter-checked-green)](https://github.com/seddonym/import-linter)
[![ruff](https://img.shields.io/badge/style-ruff-41B5BE?style=flat)](https://github.com/astral-sh/ruff)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
![type checked: mypy](https://img.shields.io/badge/mypy-type%20checked-green)

[![test](https://github.com/Tapeline/Embark/actions/workflows/test.yml/badge.svg?branch=master&event=push)](https://github.com/Tapeline/Embark/actions/workflows/test.yml)
[![test](https://github.com/Tapeline/Embark/actions/workflows/docs.yml/badge.svg?branch=master&event=push)](https://github.com/Tapeline/Embark/actions/workflows/docs.yml)


Automate initial setup of Windows workstations

---

<!-- TOC -->
  * [Description](#description)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Planned features](#planned-features)
  * [Tech stack](#tech-stack)
  * [Developer](#developer)
  * [License](#license)
<!-- TOC -->

---

## Description

Embark is a solution for automatic workstation setup 
(installing software, copying needed files, setting the
environment, etc.)

It could be useful if such setup should be performed on
many workstations, eliminating manual actions and thus
preventing many errors and reducing the amount of work

## Installation
> **Notice!** <br/>
> Embark is only avalilable on Windows!

No need to install, Embark is a standalone portable

## Usage
Please refer to the [documentation](https://tapeline.github.io/Embark/docs/en)

## Planned features
- [ ] `pywinauto` support
- [ ] More testing

## Tech stack
![Pydantic](https://img.shields.io/badge/-Pydantic-464646?logo=Pydantic)
![Pydantic](https://img.shields.io/badge/-requests-464646?logo=Python)
![Pydantic](https://img.shields.io/badge/UI-customtkinter-464646?logo=Python)

## Developer
Project is being developed by [@Tapeline](https://github.com/Tapeline)

## License
This work is licensed under GNU General Public License v3.0