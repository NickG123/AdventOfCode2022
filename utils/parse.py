"""Helper functions for parsing input."""
from typing import Callable, Iterator, TextIO, TypeVar

T = TypeVar("T")
S = TypeVar("S")


def read_lines(file: TextIO) -> Iterator[str]:
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
