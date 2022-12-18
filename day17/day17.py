"""Day 17."""
from __future__ import annotations

from itertools import cycle
from typing import Optional, TextIO

from result import Result
from utils.geometry import Point2D

HORZONTAL_LINE_SHAPE = {Point2D(0, 0), Point2D(1, 0), Point2D(2, 0), Point2D(3, 0)}
PLUS_SHAPE = {Point2D(1, 0), Point2D(0, 1), Point2D(1, 1), Point2D(2, 1), Point2D(1, 2)}
L_SHAPE = {Point2D(0, 0), Point2D(1, 0), Point2D(2, 0), Point2D(2, 1), Point2D(2, 2)}
VERTICAL_LINE_SHAPE = {Point2D(0, 0), Point2D(0, 1), Point2D(0, 2), Point2D(0, 3)}
BOX_SHAPE = {Point2D(0, 0), Point2D(1, 0), Point2D(0, 1), Point2D(1, 1)}

CHAMBER_WIDTH = 7

SHAPES = [HORZONTAL_LINE_SHAPE, PLUS_SHAPE, L_SHAPE, VERTICAL_LINE_SHAPE, BOX_SHAPE]


class Rock:
    """A falling rock."""

    def __init__(self, initial_height: int, shape: set[Point2D]) -> None:
        """Construct a new rock."""
        self.position = {p + Point2D(2, initial_height) for p in shape}

    def move(
        self,
        movement: Point2D,
        occupied_positions: set[Point2D],
    ) -> bool:
        """Move the rock."""
        new_position = {p + movement for p in self.position}
        if any(p.x < 0 or p.x >= CHAMBER_WIDTH or p.y < 0 for p in new_position):
            return False
        if not new_position.isdisjoint(occupied_positions):
            return False
        self.position = new_position
        return True


class CycleDetector:
    """Detects cycles in the rock drop."""

    def __init__(self) -> None:
        """Create a cycle detector."""
        self.recordings: dict[tuple[frozenset[Point2D], int, int], tuple[int, int]] = {}

    def check_cycle(
        self,
        occupied_spaces: set[Point2D],
        jet_offset: int,
        rock_offset: int,
        rock_number: int,
        height: int,
    ) -> Optional[tuple[int, int]]:
        """Check for a cycle."""
        min_occupied_space = min(p.y for p in occupied_spaces)
        occupied_spaces_shifted = frozenset(
            {p - Point2D(0, min_occupied_space) for p in occupied_spaces}
        )
        key = (occupied_spaces_shifted, jet_offset, rock_offset)

        if key in self.recordings:
            old_height, old_rock_number = self.recordings[key]
            return rock_number - old_rock_number, height - old_height
        self.recordings[key] = (height, rock_number)
        return None


def drop_rocks(jet_pattern: str, number: int) -> int:
    """Drop rocks and return the height reached."""
    jet_patterns = cycle(enumerate(jet_pattern))
    rock_shapes = cycle(enumerate(SHAPES))
    occupied_positions: set[Point2D] = set()
    cycle_detector = CycleDetector()
    rock_number = 0
    height = 0

    while True:
        rock_offset, shape = next(rock_shapes)
        rock = Rock(height + 3, shape)
        while True:
            jet_offset, jet_char = next(jet_patterns)
            match jet_char:
                case ">":
                    rock.move(Point2D(1, 0), occupied_positions)
                case "<":
                    rock.move(Point2D(-1, 0), occupied_positions)
                case other:
                    raise Exception(f"Invalid jet pattern {other}")
            can_move = rock.move(Point2D(0, -1), occupied_positions)
            if not can_move:
                occupied_positions.update(rock.position)
                height = max(height, max(p.y for p in rock.position) + 1)
                # Arbitrarily cut off everything but the top 100 rows
                # We could do something smarter here... but this works.
                occupied_positions = {
                    p for p in occupied_positions if height - p.y < 100
                }
                rock_cycle = cycle_detector.check_cycle(
                    occupied_positions,
                    jet_offset,
                    rock_offset,
                    rock_number,
                    height,
                )
                if rock_cycle is not None:
                    rock_delta, height_delta = rock_cycle
                    skips = (number - rock_number) // rock_delta
                    rock_number += skips * rock_delta
                    height += skips * height_delta
                    occupied_positions = {
                        p + Point2D(0, skips * height_delta) for p in occupied_positions
                    }
                rock_number += 1
                if rock_number == number:
                    return height
                break


def run(file: TextIO) -> Result:
    """Solution for Day 17."""
    line = next(file).strip()

    part1 = drop_rocks(line, 2022)
    part2 = drop_rocks(line, 1000000000000)

    return Result(part1, part2)
