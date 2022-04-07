from dataclasses import dataclass
from typing import Dict, Set


@dataclass(frozen=True)
class Code:
    pegs: Dict[str, Set[int]]


class CodeBuilder:
    def __init__(self, code: str) -> None:
        self.code = code
        self._check_colors()

    def _check_colors(self):
        pass

    def _find(self, code, ch):
        return {i for i, ltr in enumerate(code) if ltr == ch}

    def __call__(self):
        pegs = {color: self._find(self.code, color) for color in self.code}
        return Code(pegs=pegs)
