from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Iterator


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
