"""Day 14."""

from enum import Enum
from itertools import count, pairwise
from typing import Optional, TextIO

from result import Result
from utils.geometry import Point2D
from utils.parse import read_lines


class Cell(Enum):
    """The value in a cell."""

    ROCK = "#"
    EMPTY = "."
    SAND = "O"


MOVEMENT_CHOICES = [Point2D(0, 1), Point2D(-1, 1), Point2D(1, 1)]
ENTRY_POINT = Point2D(500, 0)


def format_grid(grid: dict[Point2D, Cell]) -> str:
    """String format the grid."""
    min_x = min(grid.keys(), key=lambda p: p.x).x
    max_x = max(grid.keys(), key=lambda p: p.x).x
    min_y = 0
    max_y = max(grid.keys(), key=lambda p: p.y).y

    result = []
    for y in range(min_y, max_y + 1):
        result.append(
            "".join(
                grid.get(Point2D(x, y), Cell.EMPTY).value
                for x in range(min_x, max_x + 1)
            )
        )
    return "\n".join(result)


def drop_sand(
    grid: dict[Point2D, Cell],
    abyss_point: Optional[int] = None,
    floor: Optional[int] = None,
) -> bool:
    """Drop sand in the grid.  Return True if it falls into the abyss or reaches 500, 0."""
    p = ENTRY_POINT
    while True:
        if abyss_point is not None and p.y >= abyss_point:
            return True
        for offset in MOVEMENT_CHOICES:
            if grid.get(p + offset) is None and (floor is None or p.y < floor):
                p += offset
                break
        else:
            break
    grid[p] = Cell.SAND
    if p == ENTRY_POINT:
        return True
    return False


def run(file: TextIO) -> Result:
    """Solution for Day 14."""
    grid = {}
    for line in read_lines(file):
        for start, end in pairwise(Point2D.parse(x) for x in line.split(" -> ")):
            for p in start.points_between(end):
                grid[p] = Cell.ROCK
    abyss_point = max(grid.keys(), key=lambda p: p.y).y
    print(format_grid(grid))
    for part1 in count():
        if drop_sand(grid, abyss_point):
            break
    for part2 in count(part1 + 1):
        if drop_sand(grid, floor=abyss_point + 1):
            break
    print(format_grid(grid))

    return Result(part1, part2)
