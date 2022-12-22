"""Helper functions for iterables."""

import collections
from itertools import islice, zip_longest
from typing import Callable, Iterable, Iterator, Optional, TypeVar

T = TypeVar("T")


# Courtesy of https://docs.python.org/3/library/itertools.html
def grouper(
    iterable: Iterable[T],
    n: int,
    *,
    incomplete: str = "fill",
    fillvalue: Optional[T] = None,
) -> Iterable[Iterable[T]]:
    """Collect data into non-overlapping fixed-length chunks or blocks."""
    # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
    args = [iter(iterable)] * n
    if incomplete == "fill":
        return zip_longest(*args, fillvalue=fillvalue)
    if incomplete == "strict":
        return zip(*args, strict=True)
    if incomplete == "ignore":
        return zip(*args)
    else:
        raise ValueError("Expected fill, strict, or ignore")


# Also thank to https://docs.python.org/3/library/itertools.html
def sliding_window(iterable: Iterable[T], n: int) -> Iterable[tuple[T, ...]]:
    """Iterate over an iterable as a sliding window."""
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def read_iter_until(
    data: Iterator[T],
    terminators: Optional[set[T]] = None,
    pred: Optional[Callable[[T], bool]] = None,
) -> tuple[list[T], Optional[T]]:
    """Read an iterator until a terminator, returning the read string and the terminator."""
    result: list[T] = []
    for i in data:
        if terminators is not None and i in terminators:
            return result, i
        if pred is not None and pred(i):
            return result, i
        result.append(i)
    return result, None
