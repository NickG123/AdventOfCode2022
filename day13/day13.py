"""Day 13."""
from __future__ import annotations

from functools import total_ordering
from itertools import chain, zip_longest
from typing import Iterator, TextIO

from result import Result
from utils.iterables import read_iter_until
from utils.parse import read_groups, read_lines


@total_ordering
class Packet:
    """A packet."""

    def __init__(self, contents: list[int | Packet]) -> None:
        """Create a new packet."""
        self.contents = contents

    def __str__(self) -> str:
        """Convert to string."""
        return f"[{','.join(str(x) for x in self.contents)}]"

    def __eq__(self, other: object) -> bool:
        """Determine if two packets are equal."""
        if not isinstance(other, Packet):
            return False
        for left, right in zip_longest(self.contents, other.contents):
            if left != right:
                return False
        return True

    def __lt__(self, other: Packet) -> bool:
        """Determine if a packet is less than another."""
        if self == other:
            return False

        for left, right in zip_longest(self.contents, other.contents):
            if left is None:
                return True
            if right is None:
                return False
            if isinstance(left, int) and isinstance(right, Packet):
                left = Packet([left])
            elif isinstance(left, Packet) and isinstance(right, int):
                right = Packet([right])

            if left < right:
                return True
            if left > right:
                return False
        return True

    @staticmethod
    def parse(data: Iterator[str]) -> Packet:
        """Parse a packet from string."""
        contents: list[Packet | int] = []
        assert next(data) == "["
        while True:
            match (next(data)):
                case ",":
                    continue
                case "]":
                    return Packet(contents)
                case "[":
                    contents.append(Packet.parse(chain("[", data)))
                case digit:
                    remainder, terminator = read_iter_until(data, {",", "]"})
                    contents.append(int(digit + "".join(remainder)))
                    if terminator == "]":
                        return Packet(contents)


def run(file: TextIO) -> Result:
    """Solution for Day 13."""
    part1 = 0
    divider_packet_1 = Packet.parse(iter("[[2]]"))
    divider_packet_2 = Packet.parse(iter("[[6]]"))
    all_packets = [divider_packet_1, divider_packet_2]
    for i, (left, right) in enumerate(
        read_groups(read_lines(file), "", lambda x: Packet.parse(iter(x))), start=1
    ):
        if left < right:
            part1 += i
        all_packets.append(left)
        all_packets.append(right)

    all_packets.sort()
    part2 = (all_packets.index(divider_packet_1) + 1) * (
        all_packets.index(divider_packet_2) + 1
    )

    return Result(part1, part2)
