"""Day 06."""

from typing import Iterable, TextIO

from result import Result
from utils.iterables import sliding_window
from utils.parse import read_lines


def find_first_unique_window(data: Iterable[str], window_size: int) -> int:
    """Find the first set of n consecutive characters in data that are all unique."""
    for i, window in enumerate(sliding_window(data, window_size)):
        if len(set(window)) == window_size:
            return i + window_size
    raise Exception("No window found")


def run(file: TextIO) -> Result:
    """Solution for Day 06."""
    data = next(read_lines(file))

    return Result(find_first_unique_window(data, 4), find_first_unique_window(data, 14))
