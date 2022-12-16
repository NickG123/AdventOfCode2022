"""Day 15."""
from __future__ import annotations

import re
from typing import Optional, TextIO

from result import Result
from utils.geometry import Point2D
from utils.parse import read_lines

regex = re.compile(
    r"Sensor at x=(-?\d*), y=(-?\d*): closest beacon is at x=(-?\d*), y=(-?\d*)"
)


class Sensor:
    """A class representing a sensor."""

    def __init__(self, position: Point2D, beacon_position: Point2D) -> None:
        """Create a new sensor."""
        self.position = position
        self.beacon_position = beacon_position
        self.manhattan_radius = position.manhattan_distance(beacon_position)

    @staticmethod
    def from_string(s: str) -> Sensor:
        """Parse a sensor from input."""
        match = regex.match(s)
        assert match is not None
        point_data = match.groups()
        return Sensor(
            Point2D(int(point_data[0]), int(point_data[1])),
            Point2D(int(point_data[2]), int(point_data[3])),
        )

    def coverage_on_line(self, y: int) -> Optional[tuple[int, int]]:
        """Compute the start and and point that this sensor covers on a line."""
        height = abs(y - self.position.y)
        if height > self.manhattan_radius:
            return None
        width = self.manhattan_radius - height
        return (self.position.x - width, self.position.x + width)


def collapse_coverage(sensors: list[Sensor], line: int) -> list[tuple[int, int]]:
    """Collapse the coverage down to a minimum set of intervals."""
    coverage = [sensor.coverage_on_line(line) for sensor in sensors]
    sorted_coverage = sorted(c for c in coverage if c is not None)
    if len(sorted_coverage) == 0:
        return []
    collapsed = [sorted_coverage[0]]
    for start, end in sorted_coverage[1:]:
        existing_start, existing_end = collapsed[-1]
        if start > existing_end + 1:
            collapsed.append((start, end))
        else:
            collapsed[-1] = (existing_start, max(existing_end, end))
    return collapsed


def coverage_on_line(sensors: list[Sensor], line: int) -> int:
    """Compute total line coverage."""
    collapsed = collapse_coverage(sensors, line)

    unique_beacons_on_line = {
        sensor.beacon_position.x
        for sensor in sensors
        if sensor.beacon_position.y == line
    }
    beacons_covered = len(
        [
            x
            for x in unique_beacons_on_line
            if any(start <= x <= end for (start, end) in collapsed)
        ]
    )
    return sum(end - start + 1 for start, end in collapsed) - beacons_covered


def find_space(sensors: list[Sensor], max_coord: int) -> Point2D:
    """Find the beacon."""
    for y in range(max_coord + 1):
        coverage = collapse_coverage(sensors, y)
        if len(coverage) != 1:
            return Point2D(coverage[0][1] + 1, y)
    raise Exception("Beacon not found")


def run(file: TextIO) -> Result:
    """Solution for Day 15."""
    sensors = [Sensor.from_string(line) for line in read_lines(file)]
    p2 = find_space(sensors, 4000000)

    return Result(coverage_on_line(sensors, 2000000), 4000000 * p2.x + p2.y)
