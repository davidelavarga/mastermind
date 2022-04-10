from dataclasses import dataclass


@dataclass(frozen=True)
class Guess:
    id: int
    code: str
    black_pegs: int
    white_pegs: int
