"""Day 19."""
from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum
from functools import partial
from multiprocessing import Pool
from typing import TextIO

from result import Result
from utils.parse import read_lines

regex = re.compile(r"Each (?P<resource>\w*) robot costs (?P<costs>.*?)\.")


class Resource(Enum):
    """A resource."""

    ORE = "ore"
    CLAY = "clay"
    OBSIDIAN = "obsidian"
    GEODE = "geode"


@dataclass
class Turn:
    """A turn in a blueprint evaluation."""

    robots: Counter[Resource]
    resources: Counter[Resource]


class Blueprint:
    """A blueprint."""

    def __init__(self, robot_costs: dict[Resource, Counter[Resource]]) -> None:
        """Construct a new blueprint."""
        self.robot_costs = robot_costs
        self.max_cost_per_resource = {
            resource: max(cost[resource] for cost in robot_costs.values())
            for resource in Resource
        }

    def options(
        self, resources: Counter[Resource], robots: Counter[Resource]
    ) -> set[tuple[Resource, int]]:
        """Gety the options that can be built and the time it takes to build them."""
        result = set()
        for output_robot, cost in self.robot_costs.items():
            if not all(resource in robots for resource in cost):
                continue  # We aren't producing a required material
            if (
                robots[output_robot] >= self.max_cost_per_resource[output_robot]
                and output_robot != Resource.GEODE
            ):
                continue  # We already have the maximum number of this robot that we want

            turns_needed = 1 + max(
                max(
                    # Int ceiling division -(a // -b)
                    -((required_amount - resources[resource]) // -robots[resource])
                    for resource, required_amount in cost.items()
                ),
                0,
            )

            result.add((output_robot, turns_needed))
        return result

    @staticmethod
    def from_string(line: str) -> Blueprint:
        """Parse a blueprint from a string."""
        blueprint_costs = {}
        for robot in regex.finditer(line):
            robot_costs: Counter[Resource] = Counter()
            for cost in robot.group("costs").split(" and "):
                count, resource = cost.split(" ")
                robot_costs[Resource(resource)] = int(count)
            blueprint_costs[Resource(robot.group("resource"))] = robot_costs
        return Blueprint(blueprint_costs)


def theoretical_max(turn: Turn, time_left: int) -> int:
    """Compute the theoretical maximum number of geodes possible."""
    return (
        turn.resources[Resource.GEODE]
        + turn.robots[Resource.GEODE] * time_left
        + time_left * (time_left + 1) // 2  # If we built one geode robot per turn
    )


def prune(robots_and_resources: list[Turn], best: int, time_left: int) -> list[Turn]:
    """Prune branches that aren't relevant."""
    if not robots_and_resources or best == 0:
        return robots_and_resources
    return [
        turn
        for turn in robots_and_resources
        if theoretical_max(turn, time_left) >= best
    ]


def crack_geodes(
    blueprint: Blueprint,
    starting_robots: Counter[Resource],
    starting_resources: Counter[Resource],
    total_time: int,
) -> int:
    """Figure out how many geodes can be cracked by a blueprint."""
    turns = defaultdict(list, {0: [Turn(starting_robots, starting_resources)]})
    max_geodes_at_end = 0
    for turn_num in range(total_time):
        time_left = total_time - turn_num
        turns[turn_num] = prune(turns[turn_num], max_geodes_at_end, time_left)
        for turn in turns[turn_num]:
            options = blueprint.options(turn.resources, turn.robots)
            for option, turns_required in options:
                if turns_required > time_left:
                    continue
                new_robots = turn.robots + Counter({option: 1})
                new_resources = (
                    turn.resources
                    + Counter({k: v * turns_required for k, v in turn.robots.items()})
                    - blueprint.robot_costs[option]
                )
                turns[turn_num + turns_required].append(Turn(new_robots, new_resources))
                max_geodes_at_end = max(
                    max_geodes_at_end,
                    turn.robots[Resource.GEODE] * time_left
                    + turn.resources[Resource.GEODE],
                )

    return max_geodes_at_end


def run(file: TextIO) -> Result:
    """Solution for Day 19."""
    pool = Pool()
    blueprints = [Blueprint.from_string(line) for line in read_lines(file)]
    robots = Counter({Resource.ORE: 1})
    resources: Counter[Resource] = Counter()
    p1 = pool.map(
        partial(
            crack_geodes,
            starting_robots=robots,
            starting_resources=resources,
            total_time=24,
        ),
        blueprints,
    )
    p2 = pool.map(
        partial(
            crack_geodes,
            starting_robots=robots,
            starting_resources=resources,
            total_time=32,
        ),
        blueprints[:3],
    )

    return Result(sum(i * p for i, p in enumerate(p1, start=1)), math.prod(p2))
