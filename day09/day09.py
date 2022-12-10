"""Day 09."""

from typing import TextIO

from result import Result
from utils.geometry import Point2D
from utils.parse import read_lines

DIRECTIONS = {
    "R": Point2D(1, 0),
    "U": Point2D(0, 1),
    "L": Point2D(-1, 0),
    "D": Point2D(0, -1),
}


def move_rope_tail(rope_tail: Point2D, rope_head: Point2D) -> Point2D:
    """Move the rope tail according to the rope head."""
    diff = rope_head - rope_tail
    if abs(diff.x) < 2 and abs(diff.y) < 2:
        return rope_tail
    return rope_tail + diff.unit()


def run(file: TextIO) -> Result:
    """Solution for Day 09."""
    rope_head = Point2D(0, 0)
    rope_knots = [Point2D(0, 0)] * 9

    knot_2_visits = set()
    tail_visits = set()

    for line in read_lines(file):
        direction, num = line.split()
        for _ in range(int(num)):
            rope_head += DIRECTIONS[direction]
            prev_knot = rope_head
            for i, rope_knot in enumerate(rope_knots):
                new_position = move_rope_tail(rope_knot, prev_knot)
                rope_knots[i] = new_position
                prev_knot = new_position
            knot_2_visits.add(rope_knots[0])
            tail_visits.add(rope_knots[-1])

    return Result(len(knot_2_visits), len(tail_visits))
