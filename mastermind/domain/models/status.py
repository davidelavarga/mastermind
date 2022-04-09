from dataclasses import dataclass


@dataclass(frozen=True)
class GameStatus:
    solved: bool
    black_pegs: int
    white_pegs: int
    guess_code: str
