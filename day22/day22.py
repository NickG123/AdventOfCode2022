"""Day 22."""

from enum import Enum
from typing import Iterable, TextIO

from result import Result
from utils.geometry import Point2D
from utils.iterables import read_iter_until
from utils.parse import read_lines


class Facing(Enum):
    """Direction being faced."""

    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


EdgesType = dict[tuple[int, Facing], tuple[Point2D, Facing]]

MOVEMENT = {
    Facing.RIGHT: Point2D(1, 0),
    Facing.DOWN: Point2D(0, 1),
    Facing.LEFT: Point2D(-1, 0),
    Facing.UP: Point2D(0, -1),
}


class Position:
    """A class representing current position."""

    def __init__(
        self,
        start: Point2D,
        grid: dict[Point2D, bool],
        edges: EdgesType,
        facing: Facing = Facing.RIGHT,
    ) -> None:
        """Construct a new position."""
        self.grid = grid
        self.edges = edges
        self.facing = facing
        self.position = start

    def move(self, distance: int) -> None:
        """Move forward."""
        for _ in range(distance):
            new_position = self.position + MOVEMENT[self.facing]
            new_facing = self.facing
            if new_position not in self.grid:
                if self.facing in {Facing.LEFT, Facing.RIGHT}:
                    new_position, new_facing = self.edges[(new_position.y, self.facing)]
                else:
                    new_position, new_facing = self.edges[(new_position.x, self.facing)]
            new_cell = self.grid[new_position]
            if not new_cell:
                break
            self.position = new_position
            self.facing = new_facing

    def turn(self, direction: str) -> None:
        """Turn."""
        match direction:
            case "R":
                self.facing = Facing((self.facing.value + 1) % len(Facing))
            case "L":
                self.facing = Facing((self.facing.value - 1) % len(Facing))

    def password(self) -> int:
        """Compute the password."""
        return 1000 * self.position.y + 4 * self.position.x + self.facing.value


def parse_actions(data: str) -> Iterable[int | str]:
    """Parse the actions from the list of actions."""
    data_it = iter(data)
    for char in data_it:
        if char.isdigit():
            remainder, terminator = read_iter_until(
                data_it, pred=lambda x: not x.isdigit()
            )
            yield int(char + "".join(remainder))
            if terminator is not None:
                yield terminator
        else:
            yield char


def compute_part1_edges(grid: dict[Point2D, bool]) -> EdgesType:
    """Compute the transition edges for part 1."""
    edges: dict[tuple[int, Facing], Point2D] = {}
    for p in grid:
        if p.x <= edges.get((p.y, Facing.RIGHT), p).x:
            edges[(p.y, Facing.RIGHT)] = p
        if p.x >= edges.get((p.y, Facing.LEFT), p).x:
            edges[(p.y, Facing.LEFT)] = p
        if p.y <= edges.get((p.x, Facing.DOWN), p).y:
            edges[(p.x, Facing.DOWN)] = p
        if p.y >= edges.get((p.x, Facing.UP), p).y:
            edges[(p.x, Facing.UP)] = p
    return {(c, facing): (p, facing) for (c, facing), p in edges.items()}


def compute_part2_edges() -> EdgesType:
    """'Compute' (hard-code) the transition edges for part 2.

    I'm sure someone smarter than me could do this automatically.
    """
    edges: EdgesType = {}

    # Upwards and Downwards facings
    for x in range(1, 51):
        edges[(x, Facing.UP)] = (Point2D(51, x + 50), Facing.RIGHT)
        edges[(x, Facing.DOWN)] = (Point2D(x + 100, 1), Facing.DOWN)
    for x in range(51, 101):
        edges[(x, Facing.UP)] = (Point2D(1, x + 100), Facing.RIGHT)
        edges[(x, Facing.DOWN)] = (Point2D(50, x + 100), Facing.LEFT)
    for x in range(101, 151):
        edges[(x, Facing.UP)] = (Point2D(x - 100, 200), Facing.UP)
        edges[(x, Facing.DOWN)] = (Point2D(100, x - 50), Facing.LEFT)
    # Leftwards and Rightwards facings
    for y in range(1, 51):
        edges[(y, Facing.LEFT)] = (Point2D(1, 151 - y), Facing.RIGHT)
        edges[(y, Facing.RIGHT)] = (Point2D(100, 151 - y), Facing.LEFT)
    for y in range(51, 101):
        edges[(y, Facing.LEFT)] = (Point2D(y - 50, 101), Facing.DOWN)
        edges[(y, Facing.RIGHT)] = (Point2D(y + 50, 50), Facing.UP)
    for y in range(101, 151):
        edges[(y, Facing.LEFT)] = (Point2D(51, 151 - y), Facing.RIGHT)
        edges[(y, Facing.RIGHT)] = (Point2D(150, 151 - y), Facing.LEFT)
    for y in range(151, 201):
        edges[(y, Facing.LEFT)] = (Point2D(y - 100, 1), Facing.DOWN)
        edges[(y, Facing.RIGHT)] = (Point2D(y - 100, 150), Facing.UP)

    return edges


def run(file: TextIO) -> Result:
    """Solution for Day 22."""
    lines = read_lines(file)

    grid = {}

    for y, line in enumerate(lines, start=1):
        if not line:
            break
        for x, cell in enumerate(line, start=1):
            p = Point2D(x, y)
            match cell:
                case ".":
                    grid[p] = True
                case "#":
                    grid[p] = False
                case _:
                    continue

    p1_edges = compute_part1_edges(grid)
    p2_edges = compute_part2_edges()

    start, _ = p1_edges[(1, Facing.RIGHT)]
    p1_position = Position(start, grid, p1_edges)
    p2_position = Position(start, grid, p2_edges)
    for action in parse_actions(next(lines)):
        match action:
            case int(action):
                p1_position.move(action)
                p2_position.move(action)
            case str(action):
                p1_position.turn(action)
                p2_position.turn(action)

    return Result(p1_position.password(), p2_position.password())
