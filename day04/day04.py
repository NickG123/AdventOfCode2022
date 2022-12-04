"""Day 04."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TextIO

from result import Result


@dataclass
class IntRange:
    """A range of integers."""

    left: int
    right: int

    @staticmethod
    def from_string(s: str) -> IntRange:
        """Parse from a string in format left-right."""
        left, right = s.split("-")
        return IntRange(int(left), int(right))

    def contains(self, other: IntRange) -> bool:
        """Check if this range fully contains another."""
        return self.left <= other.left and self.right >= other.right

    def overlaps(self, other: IntRange) -> bool:
        """Check if this range overlaps with the other at all."""
        return not (self.right < other.left or self.left > other.right)


def run(file: TextIO) -> Result:
    """Solution for Day 04."""
    contains_count = 0
    overlaps_count = 0
    for line in file:
        elf1, elf2 = [IntRange.from_string(s) for s in line.split(",")]
        if elf1.contains(elf2) or elf2.contains(elf1):
            contains_count += 1
        if elf1.overlaps(elf2):
            overlaps_count += 1

    return Result(contains_count, overlaps_count)
