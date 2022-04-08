from dataclasses import dataclass
from functools import reduce
from typing import Dict

from mastermind.domain.models.code import Code


@dataclass(frozen=True)
class WhitePegs:
    code: Code
    guess: Code

    def count(self) -> int:
        white_pegs = 0
        for color, position in self.code.pegs.items():
            guess_pos = self.guess.pegs.get(color, set())
            max_white_pegs = guess_pos - position
            candidates = position - guess_pos
            white_pegs += min(len(max_white_pegs), len(candidates))
        return white_pegs
