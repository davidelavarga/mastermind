from dataclasses import dataclass
from functools import reduce
from typing import Dict

from mastermind.domain.models.code import Code


@dataclass(frozen=True)
class WhitePegs:
    code: Code
    guess: Code

    def _white_peg_condition(self, color_data: Dict):
        color, position = color_data
        guess_pos = self.guess.pegs.get(color, set())
        max_white_pegs = guess_pos - position
        candidates = position - guess_pos
        return min(len(max_white_pegs), len(candidates))

    def count(self) -> int:
        return reduce(
            lambda x, y: x + y, map(self._white_peg_condition, self.code.pegs.items())
        )
