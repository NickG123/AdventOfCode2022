"""Day 24."""
from collections import deque
from dataclasses import dataclass
from typing import TextIO

from result import Result
from utils.geometry import DIRECTIONS, Point2D
from utils.parse import read_lines

MOVE_OPTIONS = DIRECTIONS + [Point2D(0, 0)]


@dataclass
class Blizzard:
    """A blizzard."""

    position: Point2D
    direction: Point2D

    def at_turn(self, turn: int, max_x: int, max_y: int) -> Point2D:
        """Compute where this blizzard will be on a given turn."""
        return Point2D(
            ((self.position.x + self.direction.x * turn - 1) % (max_x - 2)) + 1,
            ((self.position.y + self.direction.y * turn - 1) % (max_y - 2)) + 1,
        )


def compute_occupied_spaces(
    blizzards: list[Blizzard], max_x: int, max_y: int, turn_count: int
) -> dict[int, set[Point2D]]:
    """Compute the spaces that are occupied by a set of blizzards for a each turn."""
    return {
        turn: {b.at_turn(turn, max_x, max_y) for b in blizzards}
        for turn in range(turn_count)
    }


class Navigator:
    """A class that can navigate blizzards."""

    def __init__(
        self,
        horizontal_blizzards: dict[int, set[Point2D]],
        vertical_blizzards: dict[int, set[Point2D]],
        max_x: int,
        max_y: int,
    ) -> None:
        """Construct a new navigator."""
        self.horizontal_blizzards = horizontal_blizzards
        self.vertical_blizzards = vertical_blizzards
        self.max_x = max_x
        self.max_y = max_y

    def position_is_valid(self, position: Point2D, turn_num: int) -> bool:
        """Determine if a position is valid on a particular turn."""
        return (
            0 < position.x < self.max_x - 1
            and 0 < position.y < self.max_y - 1
            and position not in self.horizontal_blizzards[turn_num % (self.max_x - 2)]
            and position not in self.vertical_blizzards[turn_num % (self.max_y - 2)]
        )

    def navigate(
        self, start_position: Point2D, end_position: Point2D, start_turn: int
    ) -> int:
        """Find a path from start to end."""
        queue = deque([(start_position, start_turn)])
        visited = set()
        while True:
            current_position, turn_num = queue.popleft()
            memo_key = (
                current_position,
                turn_num % (self.max_x - 2),
                turn_num % (self.max_y - 2),
            )
            if memo_key in visited:
                continue
            visited.add(memo_key)
            for option in MOVE_OPTIONS:
                new_position = current_position + option
                if new_position == end_position:
                    return turn_num + 1
                if (
                    self.position_is_valid(new_position, turn_num + 1)
                    or new_position == start_position
                ):
                    queue.append((new_position, turn_num + 1))


def run(file: TextIO) -> Result:
    """Solution for Day 24."""
    blizzards = []
    for y, line in enumerate(read_lines(file)):
        max_x = len(line)
        for x, cell in enumerate(line):
            p = Point2D(x, y)
            match cell:
                case ">":
                    blizzards.append(Blizzard(p, Point2D(1, 0)))
                case "<":
                    blizzards.append(Blizzard(p, Point2D(-1, 0)))
                case "^":
                    blizzards.append(Blizzard(p, Point2D(0, -1)))
                case "v":
                    blizzards.append(Blizzard(p, Point2D(0, 1)))
    max_y = y + 1
    horizontal_blizzard_spaces = compute_occupied_spaces(
        [b for b in blizzards if b.direction.y == 0], max_x, max_y, max_x - 2
    )
    vertical_blizzard_spaces = compute_occupied_spaces(
        [b for b in blizzards if b.direction.x == 0], max_x, max_y, max_y - 2
    )

    start_position = Point2D(1, 0)
    end_position = Point2D(max_x - 2, max_y - 1)

    navigator = Navigator(
        horizontal_blizzard_spaces, vertical_blizzard_spaces, max_x, max_y
    )

    part1 = navigator.navigate(start_position, end_position, 0)
    return_home = navigator.navigate(end_position, start_position, part1)
    part2 = navigator.navigate(start_position, end_position, return_home)

    return Result(part1, part2)
