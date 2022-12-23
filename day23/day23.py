"""Day 23."""

from collections import Counter, deque
from itertools import count
from typing import Iterable, TextIO

from result import Result
from utils.geometry import ALL_DIRECTIONS, Point2D
from utils.parse import read_lines

MOVEMENTS = (
    ((Point2D(-1, -1), Point2D(0, -1), Point2D(1, -1)), Point2D(0, -1)),
    ((Point2D(-1, 1), Point2D(0, 1), Point2D(1, 1)), Point2D(0, 1)),
    ((Point2D(-1, -1), Point2D(-1, 0), Point2D(-1, 1)), Point2D(-1, 0)),
    ((Point2D(1, -1), Point2D(1, 0), Point2D(1, 1)), Point2D(1, 0)),
)


def occupied(positions: Iterable[Point2D], elves: set[Point2D]) -> bool:
    """Check whether any spot in a list of positions are occupied."""
    return any(position in elves for position in positions)


def move(
    movement_options: Iterable[tuple[tuple[Point2D, ...], Point2D]],
    elves: set[Point2D],
    possibly_moving_elves: set[Point2D],
) -> tuple[set[Point2D], set[Point2D]]:
    """Move the elves once."""
    considered_positions: Counter[Point2D] = Counter()
    new_positions = {}
    for position in possibly_moving_elves:
        if not occupied([position + dir for dir in ALL_DIRECTIONS], elves):
            new_positions[position] = position
            continue
        for required_empty_spaces, movement in movement_options:
            if not occupied([s + position for s in required_empty_spaces], elves):
                considered_positions[position + movement] += 1
                new_positions[position] = position + movement
                break
        else:
            new_positions[position] = position

    result = set()
    new_possibly_moving_elves = set()
    for position in possibly_moving_elves:
        if considered_positions[new_positions[position]] > 1:
            new_possibly_moving_elves.add(position)
            result.add(position)
        else:
            new_possibly_moving_elves.add(new_positions[position])
            result.add(new_positions[position])
    result.update(elf for elf in elves if elf not in possibly_moving_elves)
    for elf in new_possibly_moving_elves:
        new_possibly_moving_elves.update(
            elf + dir for dir in ALL_DIRECTIONS if elf + dir in result
        )
    return result, new_possibly_moving_elves


def compute_empty_tiles(elves: set[Point2D]) -> int:
    """Compute the number of empty tiles in the bounding box of the elves."""
    min_y = min([e.y for e in elves])
    min_x = min([e.x for e in elves])
    max_y = max([e.y for e in elves])
    max_x = max([e.x for e in elves])

    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)


def run(file: TextIO) -> Result:
    """Solution for Day 23."""
    elves = set()
    for y, line in enumerate(read_lines(file)):
        for x, cell in enumerate(line):
            if cell == "#":
                elves.add(Point2D(x, y))

    possibly_moving_elves = set(elves)
    movements = deque(MOVEMENTS)
    for i in count(1):
        new_elves, possibly_moving_elves = move(movements, elves, possibly_moving_elves)
        if elves == new_elves:
            break
        elves = new_elves
        movements.rotate(-1)
        if i == 10:
            part1 = compute_empty_tiles(elves)

    return Result(part1, i)
