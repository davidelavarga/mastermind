from dataclasses import dataclass
from functools import reduce
from typing import Dict

from mastermind.domain.models.code import Code


@dataclass(frozen=True)
class BlackPegs:
    code: Code
    guess: Code

    def _black_peg_condition(self, color_data: Dict):
        color, position = color_data
        guess_pos = self.guess.pegs.get(color, set())
        return len(position & guess_pos)

    def count(self) -> int:
        return reduce(
            lambda x, y: x + y, map(self._black_peg_condition, self.code.pegs.items())
        )
