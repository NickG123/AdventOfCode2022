"""Day 01."""
from heapq import nlargest
from io import FileIO
from types import resolve_bases
from typing import Callable, Iterator, TypeVar

from result import Result

T = TypeVar("T")
S = TypeVar("S")


def read_lines(file: FileIO) -> Iterator[str]:
    """Read lines from a file, stripping newlines."""
    for line in file:
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


def run(file: FileIO) -> resolve_bases:
    """Solution for Day 01."""
    groups = read_groups(read_lines(file), "", int)
    result = nlargest(3, [sum(x) for x in groups])
    return Result(result[0], sum(result))
