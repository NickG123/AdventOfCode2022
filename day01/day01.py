"""Day 01."""
from heapq import nlargest
from typing import TextIO

from result import Result
from utils.parse import read_groups, read_lines


def run(file: TextIO) -> Result:
    """Solution for Day 01."""
    groups = read_groups(read_lines(file), "", int)
    result = nlargest(3, [sum(x) for x in groups])
    return Result(result[0], sum(result))
