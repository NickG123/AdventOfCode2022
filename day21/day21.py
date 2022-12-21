"""Day 21."""
from __future__ import annotations

import operator
from abc import ABC, abstractmethod
from typing import Callable, TextIO

from result import Result
from utils.parse import read_lines

ROOT = "root"
HUMAN = "humn"

OPERATORS: dict[str, Callable[[int, int], int]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}


class Monkey(ABC):
    """A monkey."""

    def __init__(self, name: str, monkeys: dict[str, Monkey]) -> None:
        """Build a new monkey."""
        self.name = name
        self.monkeys = monkeys

    @abstractmethod
    def yell(self) -> int:
        """Yell a number."""

    @abstractmethod
    def contains_human(self) -> bool:
        """Determine if this monkey or any of it's descendants is human."""

    @abstractmethod
    def compute_human_number(self, target: int) -> int:
        """Find the number the human should yell."""

    @staticmethod
    def parse(s: str, monkey_dict: dict[str, Monkey]) -> Monkey:
        """Parse a monkey from a string."""
        name, action = s.split(": ")
        match action.split(" "):
            case left_monkey, op, right_monkey:
                return OperatorMonkey(name, left_monkey, right_monkey, op, monkey_dict)
            case (v,):
                return NumberMonkey(name, int(v), monkey_dict)
            case _:
                raise Exception(f"Unexpected input {s}")


class NumberMonkey(Monkey):
    """A monkey that yells a number."""

    def __init__(self, name: str, number: int, monkeys: dict[str, Monkey]) -> None:
        """Construct a Number Monkey."""
        self.number = number
        super().__init__(name, monkeys)

    def yell(self) -> int:
        """Yell a number."""
        return self.number

    def contains_human(self) -> bool:
        """Determine if this monkey is human."""
        return self.name == HUMAN

    def compute_human_number(self, target: int) -> int:
        """Find the number the human should yell.

        Should only ever be called on human NumberMonkey.
        """
        assert self.name == HUMAN
        return target


class OperatorMonkey(Monkey):
    """A monkey that performs an operation."""

    def __init__(
        self,
        name: str,
        left_monkey_name: str,
        right_monkey_name: str,
        op: str,
        monkeys: dict[str, Monkey],
    ) -> None:
        """Construct an operator monkey."""
        self.left_monkey_name = left_monkey_name
        self.right_monkey_name = right_monkey_name
        self.op = op
        self._contains_human: bool | None = None
        super().__init__(name, monkeys)

    @property
    def left_monkey(self) -> Monkey:
        """Get the left monkey."""
        return self.monkeys[self.left_monkey_name]

    @property
    def right_monkey(self) -> Monkey:
        """Get the right monkey."""
        return self.monkeys[self.right_monkey_name]

    def yell(self) -> int:
        """Compute an yell a number."""
        return OPERATORS[self.op](self.left_monkey.yell(), self.right_monkey.yell())

    def contains_human(self) -> bool:
        """Check if the human is in the left side of the tree."""
        if self._contains_human is None:
            self._contains_human = (
                self.left_monkey.contains_human() or self.right_monkey.contains_human()
            )
        return self._contains_human

    def compute_human_number(self, target: int) -> int:
        """Find the number the human should yell."""
        if self.left_monkey.contains_human():
            other_monkey_value = self.right_monkey.yell()
            human_monkey_branch = self.left_monkey
            right = True
        else:
            other_monkey_value = self.left_monkey.yell()
            human_monkey_branch = self.right_monkey
            right = False

        match self.op:
            case "+":
                new_target = target - other_monkey_value
            case "-":
                new_target = (
                    (target + other_monkey_value)
                    if right
                    else (other_monkey_value - target)
                )
            case "*":
                new_target = target // other_monkey_value
            case "/":
                new_target = (
                    (target * other_monkey_value)
                    if right
                    else (other_monkey_value // target)
                )
            case "_":
                raise Exception("Invalid op")
        return human_monkey_branch.compute_human_number(new_target)


def run(file: TextIO) -> Result:
    """Solution for Day 21."""
    monkeys_by_name: dict[str, Monkey] = {}
    for line in read_lines(file):
        monkey = Monkey.parse(line, monkeys_by_name)
        monkeys_by_name[monkey.name] = monkey

    root = monkeys_by_name[ROOT]
    p1 = root.yell()

    assert isinstance(root, OperatorMonkey)
    new_root = OperatorMonkey(
        "root", root.left_monkey_name, root.right_monkey_name, "-", monkeys_by_name
    )
    p2 = new_root.compute_human_number(0)

    return Result(p1, p2)
