"""Day 18."""

from typing import TextIO

from result import Result
from utils.geometry import Point3D
from utils.parse import read_lines


def find_air_pockets(points: set[Point3D]) -> set[Point3D]:
    """Find the air pockets that are enclosed in lava."""
    min_x = min(p.x for p in points)
    min_y = min(p.y for p in points)
    min_z = min(p.z for p in points)
    max_x = max(p.x for p in points)
    max_y = max(p.y for p in points)
    max_z = max(p.z for p in points)

    outside = set()
    pocket = set()

    for p in points:
        for neighbour in p.neighbours():
            visited = set()
            to_visit = [neighbour]
            while to_visit:
                n = to_visit.pop()
                if n in points or n in pocket:
                    continue
                visited.add(n)
                if n in outside or not (
                    min_x <= n.x <= max_x
                    and min_y <= n.y <= max_y
                    and min_z <= n.z <= max_z
                ):
                    outside.update(visited)
                    break
                to_visit.extend(
                    new_neightbour
                    for new_neightbour in n.neighbours()
                    if new_neightbour not in visited
                )
            else:
                pocket.update(visited)

    return pocket


def run(file: TextIO) -> Result:
    """Solution for Day 18."""
    points = {Point3D.parse(line) for line in read_lines(file)}
    part1 = sum(n not in points for p in points for n in p.neighbours())

    air_pockets = find_air_pockets(points)

    part2 = sum(n not in points | air_pockets for p in points for n in p.neighbours())

    return Result(part1, part2)
