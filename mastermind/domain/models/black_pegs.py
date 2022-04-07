from dataclasses import dataclass

from mastermind.domain.models.code import Code


@dataclass(frozen=True)
class BlackPegs:
    code: Code
    guess: Code

    def count(self) -> int:
        black_pegs = 0
        for color, position in self.code.pegs.items():
            guess_color = self.guess.pegs.get(color, [])
            black_pegs += len(set(position) & set(guess_color))
        return black_pegs
