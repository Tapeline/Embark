from typing import Final
from inject import inject

math: Final = {
    "pi": 3.14,
    "e": 2.71
}


with inject(math):
    print(pi)

