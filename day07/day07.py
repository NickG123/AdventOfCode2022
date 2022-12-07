"""Day 07."""

from typing import Iterable, TextIO

from result import Result
from utils.parse import read_lines


def traverse_directories(line_it: Iterable[str]) -> list[int]:
    """Traverse a directory, finding size of the current folder and all it's subfolders.

    Current size of the outermost directory is on the end of the list.

    Assumes that we only enter each directory a single time
    """
    dir_size = 0
    all_subdir_sizes = []
    for line in line_it:
        match line.split(" "):
            case ["$", "cd", ".."]:
                break
            case ["$", "cd", _]:
                subdir_sizes = traverse_directories(line_it)
                dir_size += subdir_sizes[-1]
                all_subdir_sizes.extend(subdir_sizes)
            case ["$", "ls"]:
                pass
            case ["dir", _]:
                pass
            case [file_size, _]:
                dir_size += int(file_size)
            case _:
                raise Exception(f"Unexpected command {line}")
    return all_subdir_sizes + [dir_size]


def run(file: TextIO) -> Result:
    """Solution for Day 07."""
    subdir_sizes = traverse_directories(read_lines(file))
    part1 = sum(x for x in subdir_sizes if x < 100000)
    space_available = 70000000 - subdir_sizes[-1]
    space_required = 30000000 - space_available
    part2 = min(x for x in subdir_sizes if x > space_required)

    return Result(part1, part2)
