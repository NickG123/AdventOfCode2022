"""Day 03."""

from typing import TextIO

from result import Result
from utils.iterables import grouper
from utils.parse import read_lines


def priority(c: str) -> int:
    """Get the priority of a rucksack item"""
    return (ord(c) - ord("a") + 1) if c.islower() else (ord(c) - ord("A") + 27)


def run(file: TextIO) -> Result:
    """Solution for Day 03."""
    part1 = 0
    part2 = 0
    for group in grouper(read_lines(file), 3):
        for backpack in group:
            compartment1 = set(backpack[: len(backpack) // 2])
            compartment2 = set(backpack[len(backpack) // 2 :])
            part1 += sum(priority(x) for x in compartment1 & compartment2)
        badge_set = set.intersection(*(set(s) for s in group))
        part2 += priority(badge_set.pop())

    return Result(part1, part2)
