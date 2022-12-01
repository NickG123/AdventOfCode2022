"""Day 01."""
from heapq import nlargest
from pathlib import Path
from typing import Callable, Iterator, TypeVar

T = TypeVar("T")
S = TypeVar("S")


def read_lines(path: Path) -> Iterator[str]:
    """Read lines from a file, stripping newlines."""
    with path.open() as fin:
        for line in fin:
            yield line.strip()


def read_groups(
    it: Iterator[T], separator: T, transformer: Callable[[T], S]
) -> Iterator[list[S]]:
    """Split an iterator into groups based on a separator."""
    result: list[S] = []
    for item in it:
        if item == separator:
            if not result:
                return
            yield result
            result = []
        else:
            result.append(transformer(item))


def run() -> None:
    """Solution for Day 01."""
    groups = read_groups(read_lines(Path("input")), "", int)
    result = nlargest(3, [sum(x) for x in groups])
    print(result[0])
    print(sum(result))


if __name__ == "__main__":
    run()
