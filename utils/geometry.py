"""Helper utilities related to geometry."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


def unit(num: int) -> int:
    """Return 1 for positive, 0 for 0, or -1 for negative."""
    return -1 if num < 0 else (1 if num > 0 else 0)


@dataclass(frozen=True)
class Point2D:
    """Represents a point in 2d cartesian space."""

    x: int
    y: int

    @staticmethod
    def parse(s: str, separator: str = ",") -> Point2D:
        """Parse a point from a string."""
        x, y = s.split(separator)
        return Point2D(int(x), int(y))

    def __add__(self, other: Point2D) -> Point2D:
        """Add this point to another."""
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point2D) -> Point2D:
        """Subtract another point from this one."""
        return Point2D(self.x - other.x, self.y - other.y)

    def unit(self) -> Point2D:
        """Return a unit vector from this point."""
        return Point2D(unit(self.x), unit(self.y))

    def neighbours(self) -> Iterable[Point2D]:
        """Return the cardinal neighbours of this point."""
        for direction in DIRECTIONS:
            yield self + direction

    def points_between(self, other: Point2D) -> Iterable[Point2D]:
        """Return the points between this point and another in a line."""
        if self.x == other.x:
            return [
                Point2D(self.x, y)
                for y in range(min(self.y, other.y), max(self.y, other.y) + 1)
            ]
        if self.y == other.y:
            return [
                Point2D(x, self.y)
                for x in range(min(self.x, other.x), max(self.x, other.x) + 1)
            ]
        raise Exception("Points do not share a coordinate")

    def manhattan_distance(self, other: Point2D) -> int:
        """Compute the manhattan distance between two points."""
        return abs(self.x - other.x) + abs(self.y - other.y)


DIRECTIONS = [Point2D(0, 1), Point2D(1, 0), Point2D(0, -1), Point2D(-1, 0)]
