"""Day 12."""

from collections import deque
from typing import Optional, TextIO

from result import Result
from utils.geometry import Point2D
from utils.parse import read_lines


def climb(
    start_pos: Point2D,
    end_pos: Point2D,
    height_map: dict[Point2D, int],
    distances: dict[Point2D, int],
) -> Optional[int]:
    """Climb to the highest point."""
    queue = deque([start_pos])
    distances[start_pos] = 0

    while queue:
        curr_pos = queue.popleft()
        curr_height = height_map[curr_pos]
        curr_distance = distances[curr_pos]
        for neighbour in curr_pos.neighbours():
            height = height_map.get(neighbour)
            if (
                height is not None
                and height <= curr_height + 1
                and (
                    neighbour not in distances
                    or distances[neighbour] > curr_distance + 1
                )
            ):
                queue.append(neighbour)
                distances[neighbour] = curr_distance + 1
                if neighbour == end_pos:
                    return curr_distance + 1
    # No path
    return None


def run(file: TextIO) -> Result:
    """Solution for Day 12."""
    height_map = {}

    for y, row in enumerate(read_lines(file)):
        for x, c in enumerate(row):
            pos = Point2D(x, y)
            match c:
                case "S":
                    height = ord("a")
                    start_pos = pos
                case "E":
                    height = ord("z")
                    end_pos = pos
                case v:
                    height = ord(v)
            height_map[pos] = height

    distances: dict[Point2D, int] = {}
    part1 = climb(start_pos, end_pos, height_map, distances)
    p2_start_points = [pos for pos, height in height_map.items() if height == ord("a")]
    p2_climbs = [climb(pos, end_pos, height_map, distances) for pos in p2_start_points]
    part2 = min(p for p in p2_climbs if p is not None)

    return Result(part1, part2)
