"""Day 25."""

from itertools import count
from typing import TextIO

from result import Result
from utils.parse import read_lines


def snafu_to_decimal(val: str) -> int:
    """Convert a SNAFU to decimal."""
    result = 0
    for power, digit in enumerate(reversed(val)):
        match digit:
            case "-":
                numeric = -1
            case "=":
                numeric = -2
            case _:
                numeric = int(digit)
        result += numeric * (5**power)
    return result


def decimal_to_snafu(val: int) -> str:
    """Convert a decimal to SNAFU."""
    result = []
    for power in count():
        modulus = 5 ** (power + 1)
        remainder = val % modulus
        remainder_count = remainder // (5**power)
        if remainder_count <= 2:
            result.append(str(remainder_count))
            val -= remainder
        else:
            result.append("=" if remainder_count == 3 else "-")
            val += modulus - remainder
        if val == 0:
            break
    return "".join(reversed(result))


def run(file: TextIO) -> Result:
    """Solution for Day 25."""
    values = [snafu_to_decimal(s) for s in read_lines(file)]
    decimal_result = sum(values)
    part1 = decimal_to_snafu(decimal_result)

    return Result(part1, None)
