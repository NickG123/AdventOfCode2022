"""Day 05."""

from collections import defaultdict, deque
from typing import TextIO

from result import Result
from utils.parse import read_lines


def read_top(stacks: dict[int, deque[str]]) -> str:
    """Read the value of the top crate on each stack."""
    return "".join(stacks[n + 1][-1] for n in range(max(stacks)))


def run(file: TextIO) -> Result:
    """Solution for Day 05."""
    data_it = read_lines(file)

    cargo_stacks: dict[int, deque[str]] = defaultdict(deque)
    for line in data_it:
        if line == "":
            break
        for i, column in enumerate(line[1::4]):
            if column != " ":
                cargo_stacks[i + 1].appendleft(column)

    cargo_stacks_part_2 = {k: deque(v) for k, v in cargo_stacks.items()}

    for line in data_it:
        _, num, _, from_stack, _, to_stack = line.split(" ")

        tmp_stack: deque[str] = deque()
        for _ in range(int(num)):
            cargo_stacks[int(to_stack)].append(cargo_stacks[int(from_stack)].pop())
            tmp_stack.appendleft(cargo_stacks_part_2[int(from_stack)].pop())
        cargo_stacks_part_2[int(to_stack)].extend(tmp_stack)

    return Result(read_top(cargo_stacks), read_top(cargo_stacks_part_2))
