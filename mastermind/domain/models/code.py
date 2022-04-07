from dataclasses import dataclass
from typing import Dict, Set

from mastermind.domain.models.exceptions import ColorNotSupportedError


@dataclass(frozen=True)
class Code:
    pegs: Dict[str, Set[int]]
    raw: str

    def __str__(self) -> str:
        return self.raw


class CodeBuilder:
    def __init__(self, code: str) -> None:
        self.code = code.upper()
        self.supported_colors = "RBYGWO"
        self._check_colors()

    def _check_colors(self):
        for c in self.code:
            if c not in self.supported_colors:
                raise ColorNotSupportedError()

    def _find(self, code, ch):
        return {i for i, ltr in enumerate(code) if ltr == ch}

    def __call__(self):
        pegs = {color: self._find(self.code, color) for color in self.code}
        return Code(pegs=pegs, raw=self.code)
