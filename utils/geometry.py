"""Helper utilities related to geometry."""
from __future__ import annotations

from dataclasses import dataclass


def unit(num: int) -> int:
    """Return 1 for positive, 0 for 0, or -1 for negative."""
    return -1 if num < 0 else (1 if num > 0 else 0)


@dataclass(frozen=True)
class Point2D:
    """Represents a point in 2d cartesian space."""

    x: int
    y: int

    def __add__(self, other: Point2D) -> Point2D:
        """Add this point to another."""
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point2D) -> Point2D:
        """Subtract another point from this one."""
        return Point2D(self.x - other.x, self.y - other.y)

    def unit(self) -> Point2D:
        """Return a unit vector from this point."""
        return Point2D(unit(self.x), unit(self.y))
