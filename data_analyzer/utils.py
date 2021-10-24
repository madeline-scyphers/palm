from typing import Iterator

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


def get_factors_rev(n: int) -> Iterator[int]:
    for i in range(int(n**0.5) + 1, 1, -1):
        if n % i == 0:
            for num in [i, n//i]:
                yield num
