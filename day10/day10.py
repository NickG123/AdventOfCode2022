"""Day 10."""

from itertools import islice, tee
from typing import Iterable, TextIO

from result import Result
from utils.parse import read_lines


def run_cpu(data: Iterable[str]) -> Iterable[int]:
    """Run a CPU application."""
    register_x = 1
    for line in data:
        match line.split():
            case ("addx", num):
                yield register_x
                yield register_x
                register_x += int(num)
            case ("noop",):
                yield register_x
            case _:
                raise Exception(f"Unknown command {line}")


def run_crt(cpu: Iterable[int]) -> Iterable[str]:
    """Run the CRT based on the CPU."""
    for i, cycle in enumerate(cpu):
        horizontal_position = i % 40
        if horizontal_position == 0:
            yield "\n"
        if abs(horizontal_position - cycle) <= 1:
            yield "#"
        else:
            yield " "  # Space is so much more readable than .


def run(file: TextIO) -> Result:
    """Solution for Day 10."""
    p1_cpu, p2_cpu = tee(run_cpu(read_lines(file)))
    part1 = sum(
        i * register_value
        for i, register_value in islice(enumerate(p1_cpu, start=1), 19, 220, 40)
    )
    part2 = "".join(run_crt(p2_cpu))

    return Result(part1, part2)
