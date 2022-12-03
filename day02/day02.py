"""Day 02."""

from io import FileIO

from result import Result
from utils.parse import read_lines


def run(file: FileIO) -> None:
    """Solution for Day 02."""
    score1 = 0
    score2 = 0
    for line in read_lines(file):
        opponent, move = line.split(" ")

        # 0 for rock, 1 for paper, 2 for scissors
        opponent_numeric = ord(opponent) - ord("A")
        move_numeric = ord(move) - ord("X")
        expected_move = (ord(move) - ord("Y") + opponent_numeric) % 3

        # Score for move used
        score1 += move_numeric + 1
        score2 += expected_move + 1

        # Score for result
        score1 += ((move_numeric - opponent_numeric + 1) % 3) * 3
        score2 += (ord(move) - ord("X")) * 3

    return Result(score1, score2)


if __name__ == "__main__":
    run()
