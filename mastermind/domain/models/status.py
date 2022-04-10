from dataclasses import dataclass


@dataclass(frozen=True)
class GameStatus:
    solved: bool
    black_pegs: int = 0
    white_pegs: int = 0
    guess_code: str = ""
