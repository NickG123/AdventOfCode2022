"""Day 02."""

from pathlib import Path


def run() -> None:
    """Solution for Day 02."""
    with Path("input").open(encoding="utf-8") as fin:
        score1 = 0
        score2 = 0
        for line in fin:
            opponent, move = line.strip().split(" ")

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

    print(score1)
    print(score2)


if __name__ == "__main__":
    run()
