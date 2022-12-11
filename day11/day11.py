"""Day 11."""
from __future__ import annotations

import math
from dataclasses import dataclass
from heapq import nlargest
from typing import Any, Callable, Iterable, Iterator, Optional, TextIO

from result import Result
from utils.parse import read_lines


def int_suffix(s: str, strip: str = "") -> int:
    """Parse an int from the last word on the line."""
    return int(s.rsplit(maxsplit=1)[-1].strip(strip))


@dataclass
class Throw:
    """An item being thrown."""

    value: int
    destination: int


@dataclass
class Monkey:
    """It's a monkey."""

    monkey_id: int
    items: list[int]
    divisibility_test: int
    destination: dict[bool, int]
    operation: Callable[[int], int]
    total_inspections: int = 0
    stress_reduction: int = 3
    stress_modulus: Optional[int] = None

    @staticmethod
    def from_text(text: Iterator[str]) -> Monkey:
        """Construct a new monkey from a text description."""
        monkey_id = int_suffix(next(text), ":")
        starting_items = [int(x) for x in next(text).split(": ")[-1].split(", ")]
        operation_text = next(text).split("new = ")[-1]
        divisibility_test = int_suffix(next(text))
        true_destination = int_suffix(next(text))
        false_destination = int_suffix(next(text))

        return Monkey(
            monkey_id=monkey_id,
            items=starting_items,
            divisibility_test=divisibility_test,
            destination={True: true_destination, False: false_destination},
            operation=Monkey.get_operation(operation_text),
        )

    @staticmethod
    def get_operation(operation_text: str) -> Callable[[int], int]:
        """Convert text of an operation to an actual function."""
        match operation_text.split():
            case "old", "*", "old":
                return lambda x: x**2
            case "old", "*", num:
                return lambda x: x * int(num)
            case "old", "+", num:
                return lambda x: x + int(num)
            case _:
                raise Exception(f"Unrecognized operation {operation_text}")

    def take_turn(self) -> Iterable[Throw]:
        """Take a single turn."""
        self.total_inspections += len(self.items)
        for item in self.items:
            new_level = self.operation(item) // self.stress_reduction
            if self.stress_modulus is not None:
                new_level %= self.stress_modulus
            destination = self.destination[new_level % self.divisibility_test == 0]
            yield Throw(new_level, destination)
        self.items = []

    def clone(self, **overrides: Any) -> Monkey:
        """Clone a monkey."""
        return Monkey(
            monkey_id=self.monkey_id,
            items=self.items[:],
            divisibility_test=self.divisibility_test,
            destination=self.destination,
            operation=self.operation,
            total_inspections=self.total_inspections,
            **overrides,
        )


def run_rounds(monkeys: list[Monkey], rounds: int) -> int:
    """Run the rounds of monkeys passing."""
    for _ in range(rounds):
        for monkey in monkeys:
            for throw in monkey.take_turn():
                monkeys[throw.destination].items.append(throw.value)
    return math.prod(nlargest(2, [monkey.total_inspections for monkey in monkeys]))


def run(file: TextIO) -> Result:
    """Solution for Day 11."""
    lines_it = read_lines(file)
    monkeys = []
    while True:
        monkey = Monkey.from_text(lines_it)
        monkeys.append(monkey)
        if next(lines_it, None) is None:
            break

    stress_modulus = math.prod([monkey.divisibility_test for monkey in monkeys])
    p2_monkeys = [
        monkey.clone(stress_reduction=1, stress_modulus=stress_modulus)
        for monkey in monkeys
    ]

    return Result(
        run_rounds(monkeys, 20),
        run_rounds(p2_monkeys, 10000),
    )
