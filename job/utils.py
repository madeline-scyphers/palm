from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Iterator


def factors(nr) -> list[int]:
    i = 2
    factors = []
    while i <= nr:
        if (nr % i) == 0:
            factors.append(i)
            nr = nr / i
        else:
            i = i + 1
    return factors


def get_factors_rev(n: int, explude_one=False) -> Iterator[int]:
    end = 0
    if explude_one:
        end = 1
    for i in range(int(n**0.5) + 1, end, -1):
        if n % i == 0:
            for num in [i, n // i]:
                yield num


def make_dirs(paths: Iterable[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


# def safe_open(path, mode="w"):
#     ''' Open "path" for writing, creating any parent directories as needed.
#     '''
#     os.makedirs(os.path.dirname(path), exist_ok=True)
#     return open(path, mode)
