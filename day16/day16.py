"""Day 16."""

import re
from collections import deque
from typing import TextIO

from result import Result
from utils.parse import read_lines

regex = re.compile(
    r"Valve (?P<valve>\S*) .* rate=(?P<rate>\d*); .* valve(s)? (?P<neighbours>.*)"
)


class Grid:
    """A grid class to handle connections."""

    def __init__(
        self, connections: dict[str, dict[str, int]], rates: dict[str, int]
    ) -> None:
        """Construct a grid."""
        self.connections = connections
        self.rates = rates

    def release_pressure(
        self,
        current_node: str,
        time_left: int,
        pressure_released: int,
        released: frozenset[str],
    ) -> dict[frozenset[str], int]:
        """Find all possible pressure releases."""
        if time_left <= 0:
            return {}
        pressure_released += self.rates[current_node] * time_left

        new_released = released | {current_node}
        result = {new_released: pressure_released}

        for new_node, cost in self.connections[current_node].items():
            if new_node in new_released:
                continue
            for key, value in self.release_pressure(
                new_node, time_left - cost - 1, pressure_released, new_released
            ).items():
                result[key] = max(result.get(key, 0), value)

        return result


def compute_relevant_connections(
    start: str, connections: dict[str, list[str]], rates: dict[str, int]
) -> dict[str, int]:
    """Compute the distance to nodes of interest."""
    interesting_nodes = {}
    visited = {start}
    to_visit = deque([(node, 1) for node in connections[start]])
    while to_visit:
        current_node, distance = to_visit.popleft()
        visited.add(current_node)
        if rates[current_node] > 0:
            interesting_nodes[current_node] = distance
        to_visit.extend(
            [
                (node, distance + 1)
                for node in connections[current_node]
                if node not in visited
            ]
        )
    return interesting_nodes


def run(file: TextIO) -> Result:
    """Solution for Day 16."""
    neighbours = {}
    rates = {}
    for line in read_lines(file):
        match = regex.match(line)
        assert match is not None

        valve, rate = match.group("valve", "rate")
        rates[valve] = int(rate)
        neighbours[valve] = match.group("neighbours").split(", ")

    connections = {
        node: compute_relevant_connections(node, neighbours, rates)
        for node in neighbours
    }

    grid = Grid(connections, rates)
    pressure_release_values = grid.release_pressure("AA", 30, 0, frozenset())
    pressure_release_values_part2 = grid.release_pressure("AA", 26, 0, frozenset())

    part1 = max(pressure_release_values.values())
    part2 = max(
        v1 + v2
        for k1, v1 in pressure_release_values_part2.items()
        for k2, v2 in pressure_release_values_part2.items()
        if k1.intersection(k2) == frozenset(["AA"])
    )
    return Result(part1, part2)
