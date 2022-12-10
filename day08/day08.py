"""Day 08."""
from __future__ import annotations

import math
from typing import TextIO

from result import Result
from utils.geometry import Point2D
from utils.parse import read_lines

DIRECTIONS = [Point2D(0, 1), Point2D(1, 0), Point2D(0, -1), Point2D(-1, 0)]


class Tree:
    """A tree in the grid."""

    def __init__(
        self, grid: dict[Point2D, Tree], position: Point2D, height: int
    ) -> None:
        """Construct a new tree."""
        self.height = height
        self.position = position
        self.grid = grid
        self._visibility_memo: dict[Point2D, int] = {}

    def max_height_in_direction(self, direction: Point2D) -> int:
        """Get the height of the tallest tree in a given direction."""
        if direction not in self._visibility_memo:
            adjacent_tree = self.grid.get(self.position + direction)
            if adjacent_tree is None:
                self._visibility_memo[direction] = -1
            else:
                self._visibility_memo[direction] = max(
                    adjacent_tree.height,
                    adjacent_tree.max_height_in_direction(direction),
                )

        return self._visibility_memo[direction]

    def is_visible(self) -> bool:
        """Determine if this tree is visible from outside the grid."""
        return self.height > min(
            self.max_height_in_direction(dir) for dir in DIRECTIONS
        )

    def viewable_trees_in_direction(self, direction: Point2D) -> int:
        """Determine viewable trees in a given direction."""
        pos = self.position
        total = 0
        while True:
            pos += direction
            next_tree = self.grid.get(pos)
            if next_tree is None:
                break
            total += 1
            if next_tree.height >= self.height:
                break
        return total

    def scenic_score(self) -> int:
        """Compute the scenic score of a tree."""
        return math.prod(self.viewable_trees_in_direction(dir) for dir in DIRECTIONS)


def run(file: TextIO) -> Result:
    """Solution for Day 08."""
    grid: dict[Point2D, Tree] = {}
    for y, row in enumerate(read_lines(file)):
        for x, height in enumerate(row):
            pos = Point2D(x, y)
            tree = Tree(grid, pos, int(height))
            grid[pos] = tree

    part1 = sum(t.is_visible() for t in grid.values())
    part2 = max(t.scenic_score() for t in grid.values())

    return Result(part1, part2)
