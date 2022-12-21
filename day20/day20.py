"""Day 20."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import pairwise
from typing import Optional, TextIO

from result import Result
from utils.parse import read_lines


@dataclass
class Node:
    """Triply-linked list."""

    value: int
    next: Node
    previous: Node
    original_next: Optional[Node]

    def get_offset(self, offset: int) -> Node:
        """Get an node at a certain offset."""
        node = self
        for _ in range(abs(offset)):
            if offset > 0:
                node = node.next
            else:
                node = node.previous
        return node

    def set_next(self, other: Node) -> None:
        """Set the next node."""
        other.previous = self
        self.next = other

    def move(self, offset: int) -> None:
        """Move this node by a certain offset."""
        if offset == 0:
            return
        self.previous.set_next(self.next)

        comes_after = self.get_offset(offset if offset > 0 else offset - 1)
        self.set_next(comes_after.next)
        comes_after.set_next(self)

    def mix(self, length: int) -> None:
        """Mix the list."""
        node: Optional[Node] = self
        while node is not None:
            mod_offset = (
                (node.value % length) if node.value > 0 else (node.value % -length)
            )
            node.move(mod_offset)
            node = node.original_next

    def find(self, value: int) -> Node:
        """Find a particular node by value."""
        node = self
        while True:
            if node.value == value:
                return node
            node = node.next
            if node == self:
                raise Exception("Could not find value")

    @staticmethod
    def from_list(data: list[int]) -> Node:
        """Build from list."""
        # just gonna cheat on the typing here cuz it makes the typing way nicer elsewhere.
        nodes = [Node(val, None, None, None) for val in data]  # type: ignore
        for node, next_node in pairwise(nodes):
            node.next = next_node
            node.original_next = next_node
            next_node.previous = node
        nodes[0].previous = nodes[-1]
        nodes[-1].next = nodes[0]
        return nodes[0]

    def compute_grove_coords(self) -> int:
        """Compute the Grove coordinates."""
        node = self.find(0)
        result = 0
        for _ in range(3):
            node = node.get_offset(1000)
            result += node.value

        return result


def mix(data: list[int], rounds: int = 1) -> list[int]:
    """Mix a list of numbers."""
    mixed = list(enumerate(data))
    for _ in range(rounds):
        for step in range(len(mixed)):
            item_index = next(
                i for i, (step_num, _) in enumerate(mixed) if step_num == step
            )
            (step_num, val) = mixed.pop(item_index)
            new_position = (item_index + val) % len(mixed)
            mixed.insert(new_position, (step_num, val))
    return [val for _, val in mixed]


def compute_grove_coords(data: list[int]) -> int:
    """Compute the grove coordinates."""
    zero_index = data.index(0)
    return sum(data[(i + zero_index) % len(data)] for i in range(1000, 3001, 1000))


def run(file: TextIO) -> Result:
    """Solution for Day 20."""
    data = [int(x) for x in read_lines(file)]

    # I did it twice...
    # Turns out the triply-linked list is only marginally faster than brute force :(
    p1 = Node.from_list(data)
    p1.mix(len(data) - 1)
    p2 = Node.from_list([x * 811589153 for x in data])
    for _ in range(10):
        p2.mix(len(data) - 1)

    mixed = mix(data)
    p2_data = [val * 811589153 for val in data]
    p2_mixed = mix(p2_data, 10)

    assert compute_grove_coords(mixed) == p1.compute_grove_coords()
    assert compute_grove_coords(p2_mixed) == p2.compute_grove_coords()

    return Result(p1.compute_grove_coords(), p2.compute_grove_coords())
